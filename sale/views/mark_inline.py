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
from ..models import Mark
from ..forms import MarkForm

"""
This view consist 4 classes and 4 mixins

    MarkList: # main view render mark_list.html 

    RenderListTempMixin: # mixin to render list_temp on get request
    RenderDetailTempMixin: # mixin to render detail_temp on get request
    RenderCreateTempMixin: # mixin to render create_temp on get request
    RenderUpdateTempMixin: # mixin to render update_temp on get request
    RenderDeleteTempMixin: # mixin to render delete_temp on get request

    MarkDetail: # render detail_temp on get request 
    MarkCreate: # render create_temp on get request , create new instance on post request
    MarkUpdate: # render update_temp on get request , update instance on post request
    MarkDelete: # render delete_temp on get request , delete instance on post request
"""


# main view render mark_list.html 
class MarkList(ListView): 
    model = Mark
    template_name = 'sale/mark_inline/mark_list.html'
    context_object_name = 'mark_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mark_form'] = MarkForm()
        return context


# mixin to render list_temp on get request
class RenderListTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        data['form_is_valid'] = True
        mark_list = Mark.objects.all()
        context = {'mark_list': mark_list}
        data['list_temp'] = render_to_string('sale/mark_inline/partial_mark_list.html', context, request=request)
        return JsonResponse(data)
 

# mixin to render create_temp on get request
class RenderCreateTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        if self.badform: # when the user submit a bad form we need to return it back with errors
            data['form_is_valid'] = False
            mark_form = self.badform
        mark_form = MarkForm()
        context = {'form': mark_form}
        data['create_temp'] = render_to_string('sale/mark_inline/partial_mark_create.html', context, request=request)
        return JsonResponse(data)


# mixin to render update_temp on get request
class RenderUpdateTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        mark_instance = get_object_or_404(Mark, pk=kwargs['pk'])
        if self.badform: # when the user submit a bad form we need to return it back with errors
            mark_form = self.badform
        mark_form = MarkForm(instance=mark_instance)
        context = {'form': mark_form}
        data['update_temp'] = render_to_string('sale/mark_inline/partial_mark_update.html', context, request=request)
        return JsonResponse(data)


# mixin to render delete_temp on get request
class RenderDeleteTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        mark_instance = get_object_or_404(Mark, pk=kwargs['pk'])
        mark_form = MarkForm(instance=mark_instance)
        context = {'form': mark_form}
        data['delete_temp'] = render_to_string('sale/mark_inline/partial_mark_delete.html', context, request=request)
        return JsonResponse(data)


# mixin to render detail_temp on get request
class RenderDetailTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        mark_instance = get_object_or_404(Mark, pk=kwargs['pk'])
        context = { 'mark': mark_instance }
        data['detail_temp'] = render_to_string(
                'sale/mark_inline/partial_mark_detail.html', context, request=request
                )
        return JsonResponse(data)


# render detail_temp on get request 
class MarkDetail(RenderDetailTempMixin, View):
    pass


# render create_temp on get request , create new instance on post request
class MarkCreate(LoginRequiredMixin, RenderCreateTempMixin, RenderListTempMixin, View):
    badform = None
    
    def post(self, request, *args, **kwargs):
        form = MarkForm(request.POST)
        if form.is_valid(): 
            form.instance.created_by = request.user
            form.save()
            return RenderListTempMixin().get(request, *args, **kwargs)
        else:
            self.badform = form
            return super().get(request, *args, **kwargs)


# render update_temp on get request , update instance on post request
class MarkUpdate(LoginRequiredMixin, RenderUpdateTempMixin, RenderListTempMixin, View):
    badform = None

    def post(self, request, *args, **kwargs):
        mark_instance = Mark.objects.get(pk=kwargs['pk'])
        form = MarkForm(request.POST, instance=mark_instance)
        if form.is_valid():
            if not request.user == mark_instance.created_by:
                return HttpResponse('You can not edit this mark')
            form.save()
            return RenderListTempMixin().get(request, *args, **kwargs)
        else:
            self.badform = form
            return super().get(request, *args, **kwargs)


# render delete_temp on get request , delete instance on post request
class MarkDelete(LoginRequiredMixin, RenderDeleteTempMixin, RenderListTempMixin, View):

    def post(self, request, *args, **kwargs):
        mark_instance = get_object_or_404(Mark, pk=kwargs['pk'])
        if not request.user == mark_instance.created_by:
            return HttpResponse('You can not delete this mark')
        mark_instance.delete()
        return RenderListTempMixin().get(request, *args, **kwargs)

