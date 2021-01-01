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


################## announces crud views ################## 
class CategoryList(ListView): # retrieve all announces
    model = Category
    template_name = 'announce/categories/category_list.html'
    context_object_name = 'category_list'
    paginate_by = 5


class CategoryDetail(DetailView): # retrieve announce detail
    model = Category
    template_name = 'announce/categories/category_detail.html'
    context_object_name = 'category'


class CategoryCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView): # create announce 
    model = Category
    template_name = 'announce/categories/category_form_create.html' 
    fields = ['name']
    success_message = "Category was created successfully"

    def form_valid(self, form):
        form.instance.owner = self.request.user # add announce owner manually
        return super().form_valid(form)


class CategoryUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView): # update announce 
    model = Category
    template_name = 'announce/categories/category_form_update.html' 
    fields = ['name']
    success_message = "Category was updated successfully"

    def form_valid(self, form):
        # user should be the announce owner 
        if form.instance.owner == self.request.user:
            return super().form_valid(form)
        else:
            return HttpResponse('You are not category owner')

# delete announce 
class CategoryDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'announce/categories/category_confirm_delete.html' 
    success_message = "Category was deleted successfully"
    success_url = reverse_lazy('announce:category_list')

    def form_valid(self, form):
        # user should be the announce owner 
        if form.instance.owner == self.request.user:
            return super().form_valid(form)
        else:
            return HttpResponse('You are not category owner')


