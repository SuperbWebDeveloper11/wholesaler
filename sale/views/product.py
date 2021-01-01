from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
# messages framework
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
# class-based generic views
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
# import models
from django.contrib.auth.models import User
from ..models import Store, Product


class ProductList(ListView): 
    model = Product
    template_name = 'sale/product/product_list.html'
    context_object_name = 'product_list'
    paginate_by = 5

    def get_queryset(self):
        store = get_object_or_404(Store, pk=self.kwargs['store_pk'])
        return Product.objects.filter(store=store)

class ProductDetail(DetailView): 
    model = Product
    template_name = 'sale/product/product_detail.html'
    context_object_name = 'product'

    def get_object(self):
        store = get_object_or_404(Store, pk=self.kwargs['store_pk'])
        product = get_object_or_404(Product, store=store, pk=self.kwargs['pk'])
        return product

class ProductCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'sale/product/product_form_create.html' 
    fields = ['code', 'name', 'price', 'mark', 'available', 'image']
    success_message = "product was created successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        store = get_object_or_404(Store, pk=self.kwargs['store_pk'])
        context['store_pk'] = store.pk
        return context

    def form_valid(self, form):
        store = get_object_or_404(Store, pk=self.kwargs['store_pk'])
        form.instance.store = store 
        form.instance.created_by = self.request.user 
        return super().form_valid(form)


class ProductUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'sale/product/product_form_update.html' 
    fields = ['code', 'name', 'price', 'mark', 'available', 'image']
    success_message = "product was updated successfully"

    def get_queryset(self):
        store = get_object_or_404(Store, pk=self.kwargs['store_pk'])
        return Product.objects.filter(store=store)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        store = get_object_or_404(Store, pk=self.kwargs['store_pk'])
        context['store_pk'] = store.pk
        return context

    def form_valid(self, form):
        if form.instance.created_by == self.request.user:
            return super().form_valid(form)
        else:
            return HttpResponse("you don't have permissions")

class ProductDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'sale/product/product_confirm_delete.html' 
    success_message = "product was deleted successfully"

    def get_queryset(self):
        store = get_object_or_404(Store, pk=self.kwargs['store_pk'])
        return Product.objects.filter(store=store)

    def get_success_url(self):
        return reverse('sale:product_list', kwargs={'store_pk': self.object.store.pk})
    
    def form_valid(self, form):
        if form.instance.created_by == self.request.user:
            return super().form_valid(form)
        else:
            return HttpResponse("you don't have permissions")


