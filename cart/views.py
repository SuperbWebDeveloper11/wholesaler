from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views import View
from weasyprint import HTML
from announce.models import Announce
from .cart import Cart
from .forms import CartAddAnnounceForm


class CartAdd(View):
    def post(self, request, *args, **kwargs):
        # add new announce to the cart session
        cart = Cart(request)
        announce = get_object_or_404(Announce, id=kwargs['announce_id'])
        form = CartAddAnnounceForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(announce=announce, quantity=cd['quantity'], update_quantity=cd['update'])
        return redirect('cart:cart_detail')


class CartRemove(View):
    def get(self, request, *args, **kwargs):
        # add an announce from the cart session
        cart = Cart(request)
        announce = get_object_or_404(Announce, id=kwargs['announce_id'])
        cart.remove(announce)
        return redirect('cart:cart_detail')


class CartDetail(View):
    # display cart elements 
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        for item in cart:
                item['update_quantity_form'] = CartAddAnnounceForm(initial={'quantity': item['quantity'], 'update': True})
        return render(request, 'cart/detail.html', {'cart': cart})


# download cart elements with weasyprint
class CartDownload(View):
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        for item in cart:
                item['update_quantity_form'] = CartAddAnnounceForm(initial={'quantity': item['quantity'], 'update': True})
        html_string = render_to_string('cart/pdf_cart.html', {'cart': cart})

        html = HTML(string=html_string)
        html.write_pdf(target='/tmp/mypdf.pdf');

        fs = FileSystemStorage('/tmp')
        with fs.open('mypdf.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'
            return response
