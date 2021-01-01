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
from ..forms import ProductForm

"""
This view consist 4 classes and 4 mixins

    ProductList: # main view render product_list.html 

    RenderListTempMixin: # mixin to render list_temp on get request
    RenderDetailTempMixin: # mixin to render detail_temp on get request
    RenderCreateTempMixin: # mixin to render create_temp on get request
    RenderUpdateTempMixin: # mixin to render update_temp on get request
    RenderDeleteTempMixin: # mixin to render delete_temp on get request

    ProductDetail: # render detail_temp on get request 
    ProductCreate: # render create_temp on get request , create new instance on post request
    ProductUpdate: # render update_temp on get request , update instance on post request
    ProductDelete: # render delete_temp on get request , delete instance on post request
"""


# main view render product_list.html 
class ProductList(ListView): 
    model = Product
    template_name = 'sale/product_inline/product_list.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        self.store = get_object_or_404(Store, pk=self.kwargs['store_pk'])
        return Product.objects.filter(store=self.store)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['store'] = self.store
        context['product_form'] = ProductForm()
        return context


# mixin to render list_temp on get request
class RenderListTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        data['form_is_valid'] = True
        store = get_object_or_404(Store, pk=kwargs['store_pk'])
        product_list = Product.objects.filter(store=store)
        context = {'product_list': product_list, 'store': store }
        data['list_temp'] = render_to_string('sale/product_inline/partial_product_list.html', context, request=request)
        return JsonResponse(data)
 

# mixin to render create_temp on get request
class RenderCreateTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        if self.badform: # when the user submit a bad form we need to return it back with errors
            data['form_is_valid'] = False
            product_form = self.badform
        product_form = ProductForm()
        store = get_object_or_404(Store, pk=kwargs['store_pk'])
        context = {'form': product_form, 'store': store}
        data['create_temp'] = render_to_string('sale/product_inline/partial_product_create.html', context, request=request)
        return JsonResponse(data)


# mixin to render update_temp on get request
class RenderUpdateTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        store = get_object_or_404(Store, pk=kwargs['store_pk'])
        product_instance = get_object_or_404(Product, store=store, pk=kwargs['pk'])
        if self.badform: # when the user submit a bad form we need to return it back with errors
            product_form = self.badform
        product_form = ProductForm(instance=product_instance)
        context = {'form': product_form, 'store': store}
        data['update_temp'] = render_to_string('sale/product_inline/partial_product_update.html', context, request=request)
        return JsonResponse(data)


# mixin to render delete_temp on get request
class RenderDeleteTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        store = get_object_or_404(Store, pk=kwargs['store_pk'])
        product_instance = get_object_or_404(Product, store=store, pk=kwargs['pk'])
        product_form = ProductForm(instance=product_instance)
        context = {'form': product_form, 'store': store}
        data['delete_temp'] = render_to_string('sale/product_inline/partial_product_delete.html', context, request=request)
        return JsonResponse(data)


# mixin to render detail_temp on get request
class RenderDetailTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        store = get_object_or_404(Store, pk=kwargs['store_pk'])
        product_instance = get_object_or_404(Product, store=store, pk=kwargs['pk'])
        context = { 'product': product_instance }
        data['detail_temp'] = render_to_string(
                'sale/product_inline/partial_product_detail.html', context, request=request
                )
        return JsonResponse(data)


# render detail_temp on get request 
class ProductDetail(RenderDetailTempMixin, View):
    pass


# render create_temp on get request , create new instance on post request
class ProductCreate(LoginRequiredMixin, RenderCreateTempMixin, RenderListTempMixin, View):
    badform = None
    
    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid(): 
            store = get_object_or_404(Store, pk=kwargs['store_pk'])
            form.instance.store = store
            form.instance.created_by = request.user
            form.save()
            return RenderListTempMixin().get(request, *args, **kwargs)
        else:
            self.badform = form
            return super().get(request, *args, **kwargs)


# render update_temp on get request , update instance on post request
class ProductUpdate(LoginRequiredMixin, RenderUpdateTempMixin, RenderListTempMixin, View):
    badform = None

    def post(self, request, *args, **kwargs):
        store = get_object_or_404(Store, pk=kwargs['store_pk'])
        product_instance = get_object_or_404(Product, store=store, pk=kwargs['pk'])
        form = ProductForm(request.POST, request.FILES, instance=product_instance)
        if form.is_valid():
            if not request.user == product_instance.created_by:
                return HttpResponse('You can not edit this product')
            form.save()
            return RenderListTempMixin().get(request, *args, **kwargs)
        else:
            self.badform = form
            return super().get(request, *args, **kwargs)


# render delete_temp on get request , delete instance on post request
class ProductDelete(LoginRequiredMixin, RenderDeleteTempMixin, RenderListTempMixin, View):

    def post(self, request, *args, **kwargs):
        store = get_object_or_404(Store, pk=kwargs['store_pk'])
        product_instance = get_object_or_404(Product, store=store, pk=kwargs['pk'])
        if not request.user == product_instance.created_by:
            return HttpResponse('You can not delete this product')
        product_instance.delete()
        return RenderListTempMixin().get(request, *args, **kwargs)

