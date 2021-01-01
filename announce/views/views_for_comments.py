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
from ..models import Announce, Comment
from ..forms import CommentForm



class RenderListTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        data['form_is_valid'] = True
        current_announce = get_object_or_404(Announce, pk=kwargs['pk'])
        comment_list = Comment.objects.filter(announce=current_announce)
        context = {'comment_list': comment_list}
        data['temp'] = render_to_string('announce/comment/comment_list.html', context, request=request)
        return JsonResponse(data)
 

class RenderCreateTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        comment_create_temp = 'announce/comment/comment_create.html'
        if self.badform:
            comment_form = self.badform
        comment_form = CommentForm()
        context = {'form': comment_form, 'announce_pk': kwargs['pk']}
        data['temp'] = render_to_string(comment_create_temp, context, request=request)
        return JsonResponse(data)


class RenderUpdateTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        comment_instance = get_object_or_404(Comment, pk=kwargs['comment_pk'])
        if self.badform:
            comment_form = self.badform
        comment_form = CommentForm(instance=comment_instance)
        context = {'form': comment_form, 'announce_pk': kwargs['pk']}
        data['temp'] = render_to_string('announce/comment/comment_update.html', context, request=request)
        return JsonResponse(data)


class RenderDeleteTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        comment_instance = get_object_or_404(Comment, pk=kwargs['comment_pk'])
        comment_form = CommentForm(instance=comment_instance)
        context = {'form': comment_form, 'announce_pk': kwargs['pk']}
        data['temp'] = render_to_string('announce/comment/comment_delete.html', context, request=request)
        return JsonResponse(data)


################## comments crud views ################## 

class CommentList(RenderListTempMixin, View):
    pass
    

class CommentCreate(LoginRequiredMixin, RenderCreateTempMixin, RenderListTempMixin, View):
    badform = None
    
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid(): 
            current_announce = get_object_or_404(Announce, pk=kwargs['pk'])
            form.instance.announce = current_announce
            form.instance.owner = request.user
            form.save()
            return RenderListTempMixin().get(request, *args, **kwargs)
        else:
            self.badform = form
            return super().get(request, *args, **kwargs)


class CommentUpdate(LoginRequiredMixin, RenderUpdateTempMixin, RenderListTempMixin, View):
    badform = None

    def post(self, request, *args, **kwargs):
        current_announce = get_object_or_404(Announce, pk=kwargs['pk'])
        comment_instance = Comment.objects.get(announce=current_announce, pk=kwargs['comment_pk'])
        form = CommentForm(request.POST, instance=comment_instance)
        if form.is_valid():
            if not request.user == comment_instance.owner:
                return HttpResponse('You can not edit this comment')
            form.save()
            return RenderListTempMixin().get(request, *args, **kwargs)
        else:
            self.badform = form
            return super().get(request, *args, **kwargs)


class CommentDelete(LoginRequiredMixin, RenderDeleteTempMixin, RenderListTempMixin, View):

    def post(self, request, *args, **kwargs):
        comment_instance = get_object_or_404(Comment, pk=kwargs['comment_pk'])
        if not request.user == comment_instance.owner:
            return HttpResponse('You can not delete this comment')
        comment_instance.delete()
        return RenderListTempMixin().get(request, *args, **kwargs)

