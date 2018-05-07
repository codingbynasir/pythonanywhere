from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.views import View
from medical.models import package_item
from .models import Test_order, Test_billing, Package_billing, Package_order
from .form import TestBillingForm, PackageBillingForm
from django.contrib import messages
from django.http import HttpResponse
from .utils import render_to_pdf
import datetime


# Create your views here.

class getTestOrder(View):
    template_name = "order.html"

    def get(self, request, id=None):
        if request.user.is_authenticated:
            another_orders = Test_order.objects.filter(user__name=request.user.id)
            order = get_object_or_404(Test_order, id=id)
            is_completed = False
            try:
                p = get_object_or_404(Test_billing, order__id=id, order__user__name=request.user.id)
                if order.verify:
                    verify = True
                    if p.paid_amount == order.test.price:
                        if order.is_completed == "Yes":
                            is_completed = True
                        else:
                            is_completed = False
                    else:
                        verify = False
                else:
                    verify = False
            except:
                p = None
                verify = False
            context = {"order": order, "billing": p, "type": "test", "verify": verify, "is_completed": is_completed,
                       "another": another_orders}
            return render(request, self.template_name, context)
        else:
            return redirect('account:login')


class deleteTestOrder(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            oid = get_object_or_404(Test_order, pk=pk)
            if oid.user.name_id == request.user.id:
                oid.delete()
                messages.success(request, "Test is deleted successfully")
                return redirect('account:patient', username=request.user.username)
            raise Http404("BAD ACCESS")
        else:
            return redirect('account:login')


class testPayments(View):
    template = "form.html"
    form = TestBillingForm

    def get(self, request, id):
        if request.user.is_authenticated:
            order = get_object_or_404(Test_order, id=id)
            if order.user.name.id == request.user.id:
                context = {"form": self.form, "btn": "Pay now", "title": "Clear payment first"}
                return render(request, self.template, context)
            else:
                raise Http404("Bad Access")
        else:
            return redirect('accounts:login')

    def post(self, request, id):
        form = TestBillingForm(request.POST or None)
        if form.is_valid():
            ord = get_object_or_404(Test_order, id=id)
            instance = form.save(commit=False)
            instance.order = ord
            instance.save()
            return redirect("order_billing:order", id=id)


def updateTestPayment(request, id):
    if request.user.is_authenticated:
        order = get_object_or_404(Test_billing, order=id)
        form = TestBillingForm(request.POST or None, instance=order)
        if order.order.user.name.id == request.user.id:
            if form.is_valid():
                form.save()
                return redirect('order_billing:order', id=id)
            else:
                context = {"form": form, "btn": "Update Payment", "title": "Update payment first"}
                return render(request, "form.html", context)
        else:
            raise Http404("Bad Access")
    else:
        return redirect('accounts:login')


class generateTestForm(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            try:
                tst = get_object_or_404(Test_order, id=id, user__name=request.user.id)
                if tst:
                    bill = get_object_or_404(Test_billing, order=tst.id)
                else:
                    bill = None
            except:
                Http404('BAD ACCESS')
            data = {
                "test": tst,
                "bill": bill
            }
            pdf = render_to_pdf('PDF.html', data)
            return HttpResponse(pdf, content_type='application/pdf')
        else:
            return redirect('accounts:login')


# Package option
class getPackageOrder(View):
    template_name = "order.html"

    def get(self, request, id=None):
        if request.user.is_authenticated:
            try:
                order = get_object_or_404(Package_order, id=id)
            except:
                raise Http404('Sorry no package order found!')
            try:
                p_order = get_object_or_404(Package_billing, order__id=order.id, order__user__name=request.user.id)
                if p_order.order.verify:
                    verified=True
                else:
                    verified=False
            except:
                p_order=None
                verified=False
            item = package_item.objects.filter(package_name=order.package_name.id)
            context = {"order": order, "billing": p_order, "type": "package", "item": item, "verified":verified}
            return render(request, self.template_name, context)
        else:
            return redirect('account:login')


class deletePackageOrder(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            try:
                oid = get_object_or_404(Package_order, pk=id)
            except:
                raise Http404('Sorry no package order found!')
            if oid.user.name_id == request.user.id:
                oid.delete()
                messages.success(request, "Package is deleted successfully")
                return redirect('account:patient', username=request.user.username)
            raise Http404("BAD ACCESS")
        else:
            return redirect('account:login')


class packagePayments(View):
    template = "form.html"
    form = PackageBillingForm

    def get(self, request, id):
        if request.user.is_authenticated:
            order = get_object_or_404(Package_order, id=id)
            if order.user.name.id == request.user.id:
                context = {"form": self.form, "btn": "Pay now", "title": "Clear payment first"}
                return render(request, self.template, context)
            else:
                raise Http404("Bad Access")
        else:
            return redirect('accounts:login')

    def post(self, request, id):
        form = PackageBillingForm(request.POST or None)
        if form.is_valid():
            ord = get_object_or_404(Package_order, id=id)
            instance = form.save(commit=False)
            instance.order = ord
            instance.save()
            return redirect("order_billing:package_order", id=id)


def updatePackagePayment(request, id):
    if request.user.is_authenticated:
        order = get_object_or_404(Package_billing, order=id)
        form = PackageBillingForm(request.POST or None, instance=order)
        if order.order.user.name.id == request.user.id:
            if form.is_valid():
                form.save()
                return redirect('order_billing:package_order', id=id)
            else:
                context = {"form": form, "btn": "Update Payment", "title": "Update payment first"}
                return render(request, "form.html", context)
        else:
            raise Http404("Bad Access")
    else:
        return redirect('accounts:login')


class generatePackageForm(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            try:
                tst = get_object_or_404(Package_order, id=id, user__name=request.user.id)
                if tst:
                    bill = get_object_or_404(Package_billing, order=tst.id)
                else:
                    bill = None
            except:
                Http404('BAD ACCESS')
            data = {
                "type":"package",
                "test": tst,
                "bill": bill
            }
            pdf = render_to_pdf('PDF.html', data)
            return HttpResponse(pdf, content_type='application/pdf')
        else:
            return redirect('accounts:login')