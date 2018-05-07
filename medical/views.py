from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import test_category, ratings, has_test, diagnostic_test, hospital, package, package_item, feedback
from accounts.models import patient, shipping
from order_billing.models import Test_order, Package_order, Test_billing, Package_billing
from django.views import View
from django.views.generic import ListView
from .forms import has_testModel, feedbackForm, RatingForm, authorizeTestAdd, authorizePackageAdd, \
    authorizePackageItemAdd, AuthorTestOrderUpdateForm, AuthorPackageOrderUpdateForm
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
class index(View):
    template_name = 'index.html'

    def get(self, request):
        h = hospital.objects.all()[:6]
        t = diagnostic_test.objects.all().count()
        p = package.objects.all().count()
        return render(request, self.template_name, {"hospital": h, "test": t, "package": p})


class getTests(ListView):
    template_name = 'all_tests.html'
    model = diagnostic_test


class getSingleTest(View):
    template_name = "single_test.html"

    def get(self, request, id):
        try:
            single_test = get_object_or_404(diagnostic_test, pk=id)
        except:
            return render(request, '404.html', {"code": "404"})
        test = has_test.objects.filter(name=id)
        related_test = diagnostic_test.objects.filter(category__name=single_test.category.name)
        context = {"single_test": single_test, "test": test, "related": related_test}
        return render(request, self.template_name, context)


class testDetails(View):
    template_name = 'test_details.html'

    def get(self, request, has_test_id):
        form = has_testModel
        rform = RatingForm
        get_ratings = ratings.objects.filter(test=has_test_id, aprove=True)
        orderId = None
        is_bought = False
        try:
            test = get_object_or_404(has_test, id=has_test_id)
        except:
            return render(request, '404.html', {"code": "404"})
        if request.user.is_authenticated:
            try:
                order = get_object_or_404(Test_order, test__id=has_test_id, user=request.user.id, status='Processing')
                is_bought = True
                orderId = order.pk
            except:
                is_bought = False
        context = {"test": test, "form": form, "is_bought": is_bought,
                   "orderId": orderId, "rform": rform, "rating": get_ratings}
        return render(request, self.template_name, context)

    def post(self, request, has_test_id):
        test = has_test_id
        try:
            p = get_object_or_404(patient, name=request.user.id)
        except:
            raise Http404("Sorry you are not logged in as patient")

        if 'buy' in request.POST:
            form = has_testModel(request.POST or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = p
                instance.save()
                return redirect('medical:test_details', has_test_id=test)
            else:
                return redirect('medical:test_details', has_test_id=test)
        if 'ratingbutton' in request.POST:
            post = get_object_or_404(has_test, id=has_test_id)
            form = RatingForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = p
                instance.test = post
                instance.save()
                return redirect('medical:test_details', has_test_id=test)
            else:
                return redirect('medical:test_details', has_test_id=test)


class testPackages(View):
    template_name = "all_packages.html"
    def get(self, request):
        pack=package.objects.all().order_by('id')
        paginator = Paginator(pack, 12)
        page = request.GET.get('page')
        p = paginator.get_page(page)
        return render(request, self.template_name, {"package":p, "r":range(1,p.paginator.num_pages+1)})


class singlePackage(View):
    template_name = "single_package.html"

    def get(self, request, id):
        try:
            single_package = get_object_or_404(package, pk=id)
        except:
            return render(request, '404.html', {"code": "404"})
        item = package_item.objects.filter(package_name=single_package.id)
        order = None
        orderId = None
        if request.user.is_authenticated:
            try:
                person = get_object_or_404(patient, name=request.user.id)
                order = Package_order.objects.filter(user=person)
            except:
                order = None
        is_bought = False
        if order:
            for ord in order:
                if ord.package_name.id is single_package.id:
                    is_bought = True
                    orderId = ord.pk
                else:
                    is_bought = False
        context = {"package": single_package, "items": item, "is_bought": is_bought, "orderId": orderId}
        return render(request, self.template_name, context)

    def post(self, request, id):
        usr = get_object_or_404(patient, name=request.user.id)
        test = get_object_or_404(package, id=id)
        cr = Package_order.objects.create(user=usr, package_name=test)
        cr.save()
        return redirect('medical:package_details', id=id)


class getHospitals(View):
    template_name = 'all_hospitals.html'

    def get(self, request):
        hosp = hospital.objects.all().order_by('id')
        paginator = Paginator(hosp, 12)
        page = request.GET.get('page')
        h = paginator.get_page(page)
        return render(request, self.template_name, {"hospital":h, "r":range(1,h.paginator.num_pages+1)})


class singleHospital(View):
    template_name = 'single_hospital.html'
    form = feedbackForm

    def get(self, request, id):
        try:
            medical = get_object_or_404(hospital, pk=id)
        except:
            return render(request, '404.html', {"code": "404"})
        test = has_test.objects.filter(hospital=medical.id)
        pack = package.objects.filter(hospital=medical.id)
        feedbacks = feedback.objects.filter(hospital=id)
        context = {"hospital": medical, "tests": test, "package": pack, "form": self.form, "feedbacks": feedbacks}
        return render(request, self.template_name, context)

    def post(self, request, id):
        form = feedbackForm(request.POST or None)
        user = get_object_or_404(User, username=request.user.username)
        u = get_object_or_404(patient, name=user.id)
        m = get_object_or_404(hospital, id=id)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = u
            instance.hospital = m
            instance.save()
            return redirect("medical:hospital_details", id=m.id)
        else:
            return redirect("medical:hospital_details", id=m.id)


class search(View):
    template_name = "search.html"

    def get(self, request):
        s = request.GET.get('q')
        t = request.GET.get('type')
        if s:
            string = diagnostic_test.objects.all()
            string = string.filter(
                Q(name__icontains=s) |
                Q(category__details__icontains=s)
            )
            pack = package.objects.all()
            pack = pack.filter(
                Q(name__icontains=s) |
                Q(hospital__name__first_name__icontains=s) |
                Q(hospital__name__last_name__icontains=s) |
                Q(details__icontains=s)
            )
            hosp = hospital.objects.all()
            hosp = hosp.filter(
                Q(name__first_name__icontains=s) |
                Q(name__last_name__icontains=s) |
                Q(name__email__icontains=s) |
                Q(type__icontains=s) |
                Q(email__icontains=s) |
                Q(phone__icontains=s) |
                Q(address__icontains=s) |
                Q(zip_code__icontains=s) |
                Q(division__icontains=s)
            )
            if t:
                if t == 'package':
                    pack = package.objects.all()
                    pack = pack.filter(
                        Q(name__icontains=s) |
                        Q(hospital__name__first_name__icontains=s) |
                        Q(hospital__name__last_name__icontains=s) |
                        Q(details__icontains=s)
                    )
                    return render(request, self.template_name, {"package": pack})
                elif t == 'hospital':
                    hosp = hospital.objects.all()
                    hosp = hosp.filter(
                        Q(name__first_name__icontains=s) |
                        Q(name__last_name__icontains=s) |
                        Q(name__email__icontains=s) |
                        Q(type__icontains=s) |
                        Q(email__icontains=s) |
                        Q(phone__icontains=s) |
                        Q(address__icontains=s) |
                        Q(zip_code__icontains=s) |
                        Q(division__icontains=s)
                    )
                    return render(request, self.template_name, {"hospital": hosp})
                elif t == 'test':
                    string = diagnostic_test.objects.all()
                    string = string.filter(
                        Q(name__icontains=s) |
                        Q(category__details__icontains=s)
                    )
                    return render(request, self.template_name, {"result": string})
            return render(request, self.template_name, {"test": string, "pack": pack, "hosp": hosp})
        else:
            return redirect("medical:index")


class getLoggedHospital(View):
    template = "dashboard/dashboard.html"

    def get(self, request):
        if request.user.is_authenticated:
            if request.session['hospital'] is not None:
                if request.session['hospital'] in request.user.username:
                    m = get_object_or_404(hospital, name=request.user.id)
                    test = has_test.objects.filter(hospital__name=request.user.id)
                    test_number = has_test.objects.filter(hospital__name=request.user.id).count()
                    pack = package.objects.filter(hospital__name=request.user.id)
                    total_pack = package.objects.filter(hospital__name=request.user.id).count()
                    total_feedback = feedback.objects.filter(hospital__name=request.user.id).count()
                    total_order = Test_order.objects.filter(test__hospital__name=request.user.id).count()

                    context = {
                        "hospital": m,
                        "test": test,
                        "package": pack,
                        "test_number": test_number,
                        "total_pack": total_pack,
                        "total_feedback": total_feedback,
                        "total_order": total_order
                    }
                    return render(request, self.template, context)
                else:
                    return render(request, '404.html', {"code": "403"})
                    # raise Http404("Sorry! You are not authorize to access this page")
            else:
                return render(request, '404.html', {"code": "403"})
                # raise Http404("Sorry! You are not authorize to access this page")
        else:
            return redirect('accounts:login')


class ViewTestByHospital(View):
    template_name = "dashboard/viewt_test.html"

    def get(self, request):
        if request.user.is_authenticated:
            test = has_test.objects.filter(hospital__name=request.user.id)
            context = {
                "tests": test
            }
            return render(request, self.template_name, context)
        else:
            return redirect('accounts:login')

    def post(self, request):
        username = request.user.username
        password = request.POST.get('password')
        checkpass = authenticate(request, username=username, password=password)
        if checkpass is not None:
            test_id = request.POST.get('test')
            huser = get_object_or_404(hospital, name=request.user.id)
            dtest = get_object_or_404(has_test, hospital=huser.id, id=test_id)
            dtest.delete()
            messages.error(request, "Test is deleted")
            return redirect("medical:authorize_tests")
        else:
            messages.warning(request, "Sorry! Test is not deleted")
            return redirect("medical:authorize_tests")


class AuthorTestAdd(View):
    def get(self, request):
        form = authorizeTestAdd
        context = {
            "title": "Add a new test",
            "btnTxt": "Add",
            "form": form
        }
        return render(request, "dashboard/form.html", context)

    def post(self, request):
        name = request.POST.get('name')
        try:
            get_object_or_404(has_test, name=name, hospital__name=request.user.id)
            messages.warning(request, 'Test is already added')
            return redirect('medical:authorize_test_add')
        except:
            author = get_object_or_404(hospital, name=request.user.id)
            form = authorizeTestAdd(request.POST or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.hospital = author
                instance.save()
                messages.success(request, "Test is added successfully")
                return redirect("medical:authorize_tests")
            else:
                return redirect("medical:authorize_test_add")


def AuthorTestUpdate(request, id):
    if request.user.is_authenticated:
        h = get_object_or_404(hospital, name=request.user.id)
    else:
        return redirect('accounts:login')
    test = get_object_or_404(has_test, id=id, hospital=h.id)
    form = authorizeTestAdd(request.POST or None, instance=test)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.info(request, "Test is updated successfully")
        return redirect('medical:authorize_tests')
    else:
        return render(request, "dashboard/form.html", {"form": form, "btnTxt": "Save changes", "title": "Update test"})


class AuthorViewPackage(View):
    template_name = "dashboard/view_package.html"

    def get(self, request):
        items = None
        packid = None
        if request.user.is_authenticated:
            p = request.GET.get('p')
            if p is not None:
                single_package = get_object_or_404(package, id=p)
                items = package_item.objects.filter(package_name=single_package.id)
                packid = single_package.id
            pack = package.objects.filter(hospital__name=request.user.id)
            context = {
                "package": pack,
                "items": items,
                "packid": packid
            }
            return render(request, self.template_name, context)
        else:
            return redirect('accounts:login')

    def post(self, request):
        username = request.user.username
        password = request.POST.get('password')
        auth = authenticate(request, username=username, password=password)
        if auth is not None:
            pack_id = request.POST.get('package')
            huser = get_object_or_404(hospital, name=request.user.id)
            dtest = get_object_or_404(package, hospital=huser.id, id=pack_id)
            dtest.delete()
            messages.error(request, "Package is deleted successfully!")
            return redirect("medical:authorize_package_view")
        messages.warning(request, "Package is not deleted successfully!")
        return redirect("medical:authorize_package_view")


class AuthorAddPackage(View):
    template = "dashboard/form.html"

    def get(self, request):
        form = authorizePackageAdd
        context = {
            "form": form,
            "btnTxt": "Add",
            "title": "Add new package"
        }
        return render(request, self.template, context)

    def post(self, request):
        author = get_object_or_404(hospital, name=request.user.id)
        form = authorizePackageAdd(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.hospital = author
            instance.save()
            messages.success(request, "Package is added successfully!")
            return redirect('medical:authorize_package_view')


def AuthorPackageUpdate(request, id):
    if request.user.is_authenticated:
        h = get_object_or_404(hospital, name=request.user.id)
    else:
        return redirect('accounts:login')
    pack = get_object_or_404(package, id=id, hospital=h.id)
    form = authorizePackageAdd(request.POST or None, instance=pack)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "package is updated successfully")
        return redirect('medical:authorize_package_view')
    else:
        return render(request, "dashboard/form.html",
                      {"form": form, "btnTxt": "Save changes", "title": "Update package"})


class AuthorPackItemAdd(View):
    def get(self, request, id):
        pack = get_object_or_404(package, id=id)
        form = authorizePackageItemAdd(request.POST or None, instance=pack)
        context = {
            "form": form,
            "btnTxt": "Add item",
            "title": "Add package item"
        }
        return render(request, "dashboard/form.html", context)

    def post(self, request, id):
        form = authorizePackageItemAdd(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Package items added")
            return redirect("medical:authorize_package_view")


def AuthorPackItemEdit(request, id):
    instance = get_object_or_404(package_item, package_name=id)
    form = authorizePackageItemAdd(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.info(request, "Package items is updated")
        return redirect('medical:authorize_package_view')
    else:
        context = {
            "btnTxt": "Save changes",
            "title": "Update package items",
            "form": form
        }
        return render(request, "dashboard/form.html", context)


class AuthorTestOrder(View):
    def get(self, request):
        getorder = Test_order.objects.filter(test__hospital__name=request.user.id).order_by('-id')
        context = {"orders": getorder, "type": "test"}
        return render(request, "dashboard/view_orders.html", context)


class AuthorPackageOrder(View):
    def get(self, request):
        getorder = Package_order.objects.filter(package_name__hospital__name=request.user.id).order_by('-id')
        context = {"orders": getorder, "type": "package"}
        return render(request, "dashboard/view_orders.html", context)


class AuthorTestSingleOrder(View):
    def get(self, request, id):
        try:
            ord = get_object_or_404(Test_order, id=id)
        except:
            return render(request, '404.html', {"code": "404"})
        try:
            ship = get_object_or_404(shipping, patient=ord.user.name.id)
        except:
            ship = None
        try:
            billing = get_object_or_404(Test_billing, order__id=id)
        except:
            billing = None
        context = {
            "order": ord,
            "type": "test",
            "billing": billing,
            "shipping": ship
        }
        return render(request, "dashboard/view_order_details.html", context)


class AuthorPackageSingleOrder(View):
    def get(self, request, id):
        try:
            ord = get_object_or_404(Package_order, id=id)
        except:
            return render(request, '404.html', {"code": "404"})
        try:
            ship = get_object_or_404(shipping, patient=ord.user.name.id)
        except:
            ship = None
        try:
            billing = get_object_or_404(Package_billing, order__id=id)
        except:
            billing = None
        context = {
            "order": ord,
            "type": "package",
            "billing": billing,
            "shipping": ship
        }
        return render(request, "dashboard/view_order_details.html", context)


def AuthorTestOrderUpdate(request, id):
    try:
        orderId = get_object_or_404(Test_order, id=id)
    except:
        return render(request, '404.html', {"code": "404"})
    form = AuthorTestOrderUpdateForm(request.POST or None, instance=orderId)
    if form.is_valid():
        form.save()
        messages.success(request, "Order info is updated successfully!")
        return redirect('medical:authorize_single_order', id=id)
    else:
        context = {
            "form": form,
            "btnTxt": "Update info",
            "title": "Update test order informations"
        }
        return render(request, "dashboard/form.html", context)


def AuthorPackageOrderUpdate(request, id):
    try:
        orderId = get_object_or_404(Package_order, id=id)
    except:
        return render(request, '404.html', {"code": "404"})
    form = AuthorPackageOrderUpdateForm(request.POST or None, instance=orderId)
    if form.is_valid():
        form.save()
        messages.success(request, "Package order is updated successfully!")
        return redirect('medical:authorize_package_single_order', id=id)
    else:
        context = {
            "form": form,
            "btnTxt": "Update info",
            "title": "Update package order informations"
        }
        return render(request, "dashboard/form.html", context)


class AuthorTestOrderArchived(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.session['hospital']:
                orders = Test_order.objects.filter(test__hospital__name=request.user.id, status__icontains='archived')
                return render(request, 'dashboard/archive.html', {"order": orders, "type": "test"})
            else:
                return render(request, '404.html', {"code": "403"})
        else:
            return redirect('accounts:login')


class AuthorPackageOrderArchived(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.session['hospital']:
                orders = Package_order.objects.filter(package_name__hospital__name=request.user.id,
                                                      status__icontains='archived')
                return render(request, 'dashboard/archive.html', {"order": orders, "type": "package"})
            else:
                return render(request, '404.html', {"code": "403"})
        else:
            return redirect('accounts:login')


class AuthorFeedback(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.session['hospital']:
                s = request.GET.get('s')
                feed = feedback.objects.filter(hospital__name__username=request.user.username).order_by('-date')
                if s:
                    feed = feed.filter(
                        Q(user__name__first_name__icontains=s) |
                        Q(user__name__email__contains=s) |
                        Q(comment__icontains=s)
                    )
                context = {
                    "type": "feedback",
                    "lists": feed
                }
                return render(request, 'dashboard/feedback_review.html', context)
            else:
                return render(request, '404.html', {"code": "403"})
        else:
            return redirect('accounts:login')


class AuthorReview(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.session['hospital']:
                s = request.GET.get('s')
                f = request.GET.get('rating')
                feed = ratings.objects.filter(test__hospital__name=request.user.id).order_by('-date')
                if s:
                    feed = feed.filter(
                        Q(user__name__first_name__icontains=s) |
                        Q(user__name__email__contains=s) |
                        Q(comments__icontains=s) |
                        Q(test__name__name__icontains=s) |
                        Q(rating__icontains=s)
                    )
                if f:
                    feed = feed.filter(Q(rating__icontains=f))
                context = {
                    "type": "review",
                    "lists": feed
                }
                return render(request, 'dashboard/feedback_review.html', context)
            else:
                return render(request, '404.html', {"code": "403"})
        else:
            return redirect('accounts:login')
