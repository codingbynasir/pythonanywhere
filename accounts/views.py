from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from .forms import SignUpForm, patientForm, deleteForm, ShippingForm
from accounts.models import shipping
from .models import patient, verifyAccount
from order_billing.models import Test_order, Package_order, Test_billing, Package_billing
from medical.models import hospital

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
class getRegister(View):
    template_name = "form.html"
    form = SignUpForm

    def get(self, request):
        context = {"form": self.form, "btn": "Register", "title": "Register for a free account"}
        return render(request, self.template_name, context)

    def post(self, request):
        form = SignUpForm(request.POST or None)
        type = request.POST.get('register_as')
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_active = False
            instance.save()
            current_site = get_current_site(request)
            mail_subject = 'VMA: Activate your account.'
            message = render_to_string('mail_confirm_message.html', {
                'user': instance,
                'domain': current_site.domain,
                'uid': instance.pk,
                'token': account_activation_token.make_token(instance)
            })
            to_email = form.cleaned_data.get('email')
            to_list = [to_email]
            from_email = settings.EMAIL_HOST_USER
            usr = get_object_or_404(User, id=instance.id)
            obj = verifyAccount.objects.create(user=usr, hash_code=message, is_verify=False)
            obj.save()
            send_mail(mail_subject, message, from_email, to_list, fail_silently=True)
            return HttpResponse('<h3>A confirmation mail was sent. Please check inbox and confirm your account to '
                                'login</h3>')
        else:
            messages.warning(request, 'something went wrong')
            return redirect('account:register')


class getAccountCreate(View):
    template_name = 'account_create.html'
    form = patientForm

    def get(self, request):
        if request.user.is_authenticated:
            context = {"form": self.form, "btntext": "Create", "title": "Create patient account"}
            return render(request, self.template_name, context)
        else:
            return redirect('accounts:login')

    def post(self, request):
        user = get_object_or_404(User, username=request.user.username)
        form = patientForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.name = user
            instance.save()
            return redirect("account:patient", username=request.user.username)


class CreateShipping(View):
    def get(self, request):
        form = ShippingForm
        context = {
            "form": form,
            "btn": "Create shipping",
            "title": "Create shipping location"
        }
        return render(request, "form.html", context)

    def post(self, request):
        user = get_object_or_404(patient, name__id=request.user.id)
        form = ShippingForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.patient = user
            instance.save()
            return redirect('accounts:patient', username=request.user.username)
        else:
            return redirect('accounts:shipping_create')


def updateShipping(request):
    usr = get_object_or_404(shipping, patient=request.user.id)
    form = ShippingForm(request.POST or None, instance=usr)
    if form.is_valid():
        form.save()
        messages.success(request, 'Shipping informations is updated')
        return redirect('accounts:patient', username=request.user.username)
    else:
        context = {
            "form": form,
            "btn": "Update Shipping",
            'title': "Update shipping location"
        }
        return render(request, 'form.html', context)


class getLogin(View):
    n = None
    template_name = "login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, self.template_name)

    def post(self, request):
        if request.GET.get('next') is not None:
            self.n = request.GET.get('next')
        username = request.POST.get('username')
        password = request.POST.get('password')
        auth = authenticate(request, username=username, password=password)
        if auth is not None:
            login(request, auth)

            # If logged in user is a hospital
            usr = hospital.objects.filter(name=request.user.id)
            if usr:
                request.session['hospital'] = request.user.username
                return redirect('medical:logged_hospital')
            else:
                request.session['hospital'] = None

            if self.n is None:
                return redirect('account:patient', username=request.user.username)
            else:
                return redirect(self.n)
        else:
            msg = "Username or password is mismatched"
            return render(request, self.template_name, {"msg": msg})


class getPatient(View):
    template_name = "patient.html"

    def get(self, request, username):
        if request.user.is_authenticated:
            try:
                user = get_object_or_404(User, username=request.user.username)
            except:
                raise Http404('You are not logged in as' + username)
            account = patient.objects.filter(name=user.id)
            if account:
                p = get_object_or_404(patient, name=user.id)
                test = Test_order.objects.filter(user=p.id)
                package = Package_order.objects.filter(user=p.id)
                shippinglocation = shipping.objects.filter(patient__name=request.user.id)
                return render(request, self.template_name,
                              {"user": user, "patient": p, "tests": test, "package": package,
                               "shipping": shippinglocation})
            else:
                return redirect("account:account_create")
        else:
            return redirect('accounts:login')


class changePass(View):
    template_name = "change_pass.html"

    def get(self, request):
        form = PasswordChangeForm(request.user, request.POST or None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password is changed successfully!", extra_tags="alert")
            return redirect('accounts:patient', username=request.user.username)
        else:
            messages.error(request, "Old password is error", extra_tags="alert")
            return redirect('account:changepass')


class getUpdate(View):
    template_name = 'account_create.html'

    def get(self, request):
        if request.user.is_authenticated is None:
            return redirect('accounts:login')
        u = get_object_or_404(patient, name=request.user.id)
        form = patientForm(request.POST or None, instance=u)
        return render(request, self.template_name,
                      {"form": form, "btntext": "Update", "title": "Update your information"})

    def post(self, request):
        u = get_object_or_404(patient, name=request.user.id)
        form = patientForm(request.POST or None, request.FILES or None, instance=u)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, "Profile informations is updated!", extra_tags="alert")
            return redirect('accounts:patient', username=request.user.username)


class deleteAccount(View):
    template_name = "delete_account_confirmation.html"
    form = deleteForm

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_name, {"form": self.form})
        else:
            return redirect('accounts:login')

    def post(self, request):
        form = deleteForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            user = get_object_or_404(User, username=request.user.username)
            instance.user = user
            uid = get_object_or_404(patient, name=request.user.id)
            user.is_active = False
            instance.save()
            user.save()
            uid.delete()
            return redirect("medical:index")


def getLogout(request):
    try:
        del request.session['hospital']
    except:
        pass
    try:
        del request.session['donor']
    except:
        pass
    logout(request)
    return redirect('medical:index')


def activate(request, uidb64, token):
    try:
        user = User.objects.get(pk=uidb64)
        verify = verifyAccount.objects.get(user_id=uidb64)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        verify.is_verify = True
        verify.save()
        return HttpResponse(
            'Thank you for your email confirmation. Now you can <a href="/login" %}">login</a> your account.')
    else:
        return HttpResponse('Activation link is invalid!')
