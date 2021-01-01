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


class StoreList(ListView): 
    model = Store
    template_name = 'sale/store/store_list.html'
    context_object_name = 'store_list'
    paginate_by = 5


class StoreDetail(DetailView): 
    model = Store
    template_name = 'sale/store/store_detail.html'
    context_object_name = 'store'


class StoreCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Store
    template_name = 'sale/store/store_form_create.html' 
    fields = ['name', 'wilaya', 'address', 'image']

    success_message = "store was created successfully"

    def form_valid(self, form):
        form.instance.created_by = self.request.user 
        return super().form_valid(form)


class StoreUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Store
    template_name = 'sale/store/store_form_update.html' 
    fields = ['name', 'wilaya', 'address', 'image']
    success_message = "store was updated successfully"

    def form_valid(self, form):
        if form.instance.created_by == self.request.user:
            return super().form_valid(form)
        else:
            return HttpResponse("you don't have permissions")

class StoreDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Store
    template_name = 'sale/store/store_confirm_delete.html' 
    success_message = "store was deleted successfully"
    success_url = reverse_lazy('sale:store_list')

    def form_valid(self, form):
        if form.instance.created_by == self.request.user:
            return super().form_valid(form)
        else:
            return HttpResponse("you don't have permissions")


