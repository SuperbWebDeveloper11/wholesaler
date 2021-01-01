from decimal import Decimal
from django.conf import settings
from product.models import Product


class Cart(object):

    def __init__(self, request):
        """ Initialize the cart """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """ Iterate over the items in the cart and get the products from the database """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

    def __len__(self):
        """ Count all items in the cart """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity):
        """ Add a product to the cart or update its quantity """
        product_id = str(product.id)
        self.cart[product_id] = {'quantity': quantity}
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
