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


class MarkList(ListView): 
    model = Mark
    template_name = 'sale/mark/mark_list.html'
    context_object_name = 'mark_list'
    paginate_by = 5


class MarkDetail(DetailView): 
    model = Mark
    template_name = 'sale/mark/mark_detail.html'
    context_object_name = 'mark'


class MarkCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Mark
    template_name = 'sale/mark/mark_form_create.html' 
    fields = ['name', 'country']
    success_message = "mark was created successfully"

    def form_valid(self, form):
        form.instance.created_by = self.request.user 
        return super().form_valid(form)


class MarkUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Mark
    template_name = 'sale/mark/mark_form_update.html' 
    fields = ['name', 'country']
    success_message = "mark was updated successfully"

    def form_valid(self, form):
        if form.instance.created_by == self.request.user:
            return super().form_valid(form)
        else:
            return HttpResponse("you don't have permissions")

class MarkDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Mark
    template_name = 'sale/mark/mark_confirm_delete.html' 
    success_message = "mark was deleted successfully"
    success_url = reverse_lazy('sale:mark_list')

    def form_valid(self, form):
        if form.instance.created_by == self.request.user:
            return super().form_valid(form)
        else:
            return HttpResponse("you don't have permissions")


