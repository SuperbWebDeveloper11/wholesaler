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
from cart.forms import CartAddAnnounceForm


################## announces crud views ################## 
class AnnounceList(ListView): # retrieve all announces
    model = Announce
    template_name = 'announce/announce/announce_list.html'
    context_object_name = 'announce_list'
    paginate_by = 5


class AnnounceDetail(DetailView): # retrieve announce detail
    model = Announce
    template_name = 'announce/announce/announce_detail.html'
    context_object_name = 'announce'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['cart_announce_form'] = CartAddAnnounceForm()
        return context


class AnnounceCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView): # create announce 
    model = Announce
    template_name = 'announce/announce/announce_form_create.html' 
    fields = ['title', 'description', 'image', 'price', 'available', 'tags', 'category']
    success_message = "Announce was created successfully"

    def form_valid(self, form):
        form.instance.owner = self.request.user # add announce owner manually
        return super().form_valid(form)


class AnnounceUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView): # update announce 
    model = Announce
    template_name = 'announce/announce/announce_form_update.html' 
    fields = ['title', 'description', 'image', 'price', 'available', 'tags', 'category']
    success_message = "Announce was updated successfully"

    def form_valid(self, form):
        # user should be the announce owner 
        if form.instance.owner == self.request.user:
            return super().form_valid(form)
        else:
            return HttpResponse('You are not announce owner')

# delete announce 
class AnnounceDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Announce
    template_name = 'announce/announce/announce_confirm_delete.html' 
    success_message = "Announce was deleted successfully"
    success_url = reverse_lazy('announce:announce_list')

    def form_valid(self, form):
        # user should be the announce owner 
        if form.instance.owner == self.request.user:
            return super().form_valid(form)
        else:
            return HttpResponse('You are not announce owner')


