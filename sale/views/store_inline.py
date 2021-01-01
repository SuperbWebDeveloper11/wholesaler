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
from ..models import Store
from ..forms import StoreForm

"""
This view consist 4 classes and 4 mixins

    StoreList: # main view render store_list.html 

    RenderListTempMixin: # mixin to render list_temp on get request
    RenderDetailTempMixin: # mixin to render detail_temp on get request
    RenderCreateTempMixin: # mixin to render create_temp on get request
    RenderUpdateTempMixin: # mixin to render update_temp on get request
    RenderDeleteTempMixin: # mixin to render delete_temp on get request

    StoreDetail: # render detail_temp on get request 
    StoreCreate: # render create_temp on get request , create new instance on post request
    StoreUpdate: # render update_temp on get request , update instance on post request
    StoreDelete: # render delete_temp on get request , delete instance on post request
"""


# main view render store_list.html 
class StoreList(ListView): 
    model = Store
    template_name = 'sale/store_inline/store_list.html'
    context_object_name = 'store_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['store_form'] = StoreForm()
        return context


# mixin to render list_temp on get request
class RenderListTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        data['form_is_valid'] = True
        store_list = Store.objects.all()
        context = {'store_list': store_list}
        data['list_temp'] = render_to_string('sale/store_inline/partial_store_list.html', context, request=request)
        return JsonResponse(data)
 

# mixin to render create_temp on get request
class RenderCreateTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        if self.badform: # when the user submit a bad form we need to return it back with errors
            data['form_is_valid'] = False
            store_form = self.badform
        store_form = StoreForm()
        context = {'form': store_form}
        data['create_temp'] = render_to_string('sale/store_inline/partial_store_create.html', context, request=request)
        return JsonResponse(data)


# mixin to render update_temp on get request
class RenderUpdateTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        store_instance = get_object_or_404(Store, pk=kwargs['pk'])
        if self.badform: # when the user submit a bad form we need to return it back with errors
            store_form = self.badform
        store_form = StoreForm(instance=store_instance)
        context = {'form': store_form}
        data['update_temp'] = render_to_string('sale/store_inline/partial_store_update.html', context, request=request)
        return JsonResponse(data)


# mixin to render delete_temp on get request
class RenderDeleteTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        store_instance = get_object_or_404(Store, pk=kwargs['pk'])
        store_form = StoreForm(instance=store_instance)
        context = {'form': store_form}
        data['delete_temp'] = render_to_string('sale/store_inline/partial_store_delete.html', context, request=request)
        return JsonResponse(data)


# mixin to render detail_temp on get request
class RenderDetailTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        store_instance = get_object_or_404(Store, pk=kwargs['pk'])
        context = { 'store': store_instance }
        data['detail_temp'] = render_to_string(
                'sale/store_inline/partial_store_detail.html', context, request=request
                )
        return JsonResponse(data)


# render detail_temp on get request 
class StoreDetail(RenderDetailTempMixin, View):
    pass


# render create_temp on get request , create new instance on post request
class StoreCreate(LoginRequiredMixin, RenderCreateTempMixin, RenderListTempMixin, View):
    badform = None
    
    def post(self, request, *args, **kwargs):
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid(): 
            form.instance.created_by = request.user
            form.save()
            return RenderListTempMixin().get(request, *args, **kwargs)
        else:
            self.badform = form
            return super().get(request, *args, **kwargs)


# render update_temp on get request , update instance on post request
class StoreUpdate(LoginRequiredMixin, RenderUpdateTempMixin, RenderListTempMixin, View):
    badform = None

    def post(self, request, *args, **kwargs):
        store_instance = Store.objects.get(pk=kwargs['pk'])
        form = StoreForm(request.POST, instance=store_instance)
        if form.is_valid():
            if not request.user == store_instance.created_by:
                return HttpResponse('You can not edit this store')
            form.save()
            return RenderListTempMixin().get(request, *args, **kwargs)
        else:
            self.badform = form
            return super().get(request, *args, **kwargs)


# render delete_temp on get request , delete instance on post request
class StoreDelete(LoginRequiredMixin, RenderDeleteTempMixin, RenderListTempMixin, View):

    def post(self, request, *args, **kwargs):
        store_instance = get_object_or_404(Store, pk=kwargs['pk'])
        if not request.user == store_instance.created_by:
            return HttpResponse('You can not delete this store')
        store_instance.delete()
        return RenderListTempMixin().get(request, *args, **kwargs)

