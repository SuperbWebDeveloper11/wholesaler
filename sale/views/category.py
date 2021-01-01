from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
# messages framework
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
# class-based generic views
from django.views.generic import TemplateView, ListView, DetailView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
# import models
from django.contrib.auth.models import User
from ..models import Category

class FormData(TemplateView): 
    template_name = 'sale/category/form_data.html'

class CategoryList(ListView): 
    model = Category
    template_name = 'sale/category/category_list.html'
    context_object_name = 'category_list'
    paginate_by = 5


class CategoryDetail(DetailView): 
    model = Category
    template_name = 'sale/category/category_detail.html'
    context_object_name = 'category'


class CategoryCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView): # create sale 
    model = Category
    template_name = 'sale/category/category_form_create.html' 
    fields = ['name']
    success_message = "category was created successfully"

    def form_valid(self, form):
        form.instance.created_by = self.request.user 
        return super().form_valid(form)


class CategoryUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView): # update sale 
    model = Category
    template_name = 'sale/category/category_form_update.html' 
    fields = ['name']
    success_message = "category was updated successfully"

    def form_valid(self, form):
        if form.instance.created_by == self.request.user:
            return super().form_valid(form)
        else:
            return HttpResponse("you don't have permissions")

# delete sale 
class CategoryDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'sale/category/category_confirm_delete.html' 
    success_message = "category was deleted successfully"
    success_url = reverse_lazy('sale:category_list')

    def form_valid(self, form):
        if form.instance.created_by == self.request.user:
            return super().form_valid(form)
        else:
            return HttpResponse("you don't have permissions")


