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
from ..models import Category
from ..forms import CategoryForm

"""
This view consist 4 classes and 4 mixins

    CategoryList: # main view render category_list.html 

    RenderListTempMixin: # mixin to render list_temp on get request
    RenderDetailTempMixin: # mixin to render detail_temp on get request
    RenderCreateTempMixin: # mixin to render create_temp on get request
    RenderUpdateTempMixin: # mixin to render update_temp on get request
    RenderDeleteTempMixin: # mixin to render delete_temp on get request

    CategoryDetail: # render detail_temp on get request 
    CategoryCreate: # render create_temp on get request , create new instance on post request
    CategoryUpdate: # render update_temp on get request , update instance on post request
    CategoryDelete: # render delete_temp on get request , delete instance on post request
"""


# main view render category_list.html 
class CategoryList(ListView): 
    model = Category
    template_name = 'sale/category_inline/category_list.html'
    context_object_name = 'category_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_form'] = CategoryForm()
        return context


# mixin to render list_temp on get request
class RenderListTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        data['form_is_valid'] = True
        category_list = Category.objects.all()
        context = {'category_list': category_list}
        data['list_temp'] = render_to_string('sale/category_inline/partial_category_list.html', context, request=request)
        return JsonResponse(data)
 

# mixin to render create_temp on get request
class RenderCreateTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        if self.badform: # when the user submit a bad form we need to return it back with errors
            data['form_is_valid'] = False
            category_form = self.badform
        category_form = CategoryForm()
        context = {'form': category_form}
        data['create_temp'] = render_to_string('sale/category_inline/partial_category_create.html', context, request=request)
        return JsonResponse(data)


# mixin to render update_temp on get request
class RenderUpdateTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        category_instance = get_object_or_404(Category, pk=kwargs['pk'])
        if self.badform: # when the user submit a bad form we need to return it back with errors
            category_form = self.badform
        category_form = CategoryForm(instance=category_instance)
        context = {'form': category_form}
        data['update_temp'] = render_to_string('sale/category_inline/partial_category_update.html', context, request=request)
        return JsonResponse(data)


# mixin to render delete_temp on get request
class RenderDeleteTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        category_instance = get_object_or_404(Category, pk=kwargs['pk'])
        category_form = CategoryForm(instance=category_instance)
        context = {'form': category_form}
        data['delete_temp'] = render_to_string('sale/category_inline/partial_category_delete.html', context, request=request)
        return JsonResponse(data)


# mixin to render detail_temp on get request
class RenderDetailTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        category_instance = get_object_or_404(Category, pk=kwargs['pk'])
        context = { 'category': category_instance }
        data['detail_temp'] = render_to_string(
                'sale/category_inline/partial_category_detail.html', context, request=request
                )
        return JsonResponse(data)


# render detail_temp on get request 
class CategoryDetail(RenderDetailTempMixin, View):
    pass


# render create_temp on get request , create new instance on post request
class CategoryCreate(LoginRequiredMixin, RenderCreateTempMixin, RenderListTempMixin, View):
    badform = None
    
    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST)
        if form.is_valid(): 
            form.instance.created_by = request.user
            form.save()
            return RenderListTempMixin().get(request, *args, **kwargs)
        else:
            self.badform = form
            return super().get(request, *args, **kwargs)


# render update_temp on get request , update instance on post request
class CategoryUpdate(LoginRequiredMixin, RenderUpdateTempMixin, RenderListTempMixin, View):
    badform = None

    def post(self, request, *args, **kwargs):
        category_instance = Category.objects.get(pk=kwargs['pk'])
        form = CategoryForm(request.POST, instance=category_instance)
        if form.is_valid():
            if not request.user == category_instance.created_by:
                return HttpResponse('You can not edit this category')
            form.save()
            return RenderListTempMixin().get(request, *args, **kwargs)
        else:
            self.badform = form
            return super().get(request, *args, **kwargs)


# render delete_temp on get request , delete instance on post request
class CategoryDelete(LoginRequiredMixin, RenderDeleteTempMixin, RenderListTempMixin, View):

    def post(self, request, *args, **kwargs):
        category_instance = get_object_or_404(Category, pk=kwargs['pk'])
        if not request.user == category_instance.created_by:
            return HttpResponse('You can not delete this category')
        category_instance.delete()
        return RenderListTempMixin().get(request, *args, **kwargs)

