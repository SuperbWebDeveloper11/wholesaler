from decimal import Decimal
from django.conf import settings
from announce.models import Announce


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and get the announces 
        from the database.
        """
        announce_ids = self.cart.keys()
        # get the announce objects and add them to the cart
        announces = Announce.objects.filter(id__in=announce_ids)

        cart = self.cart.copy()
        for announce in announces:
            cart[str(announce.id)]['announce'] = announce

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, announce, quantity=1, update_quantity=False):
        """
        Add a announce to the cart or update its quantity.
        """
        announce_id = str(announce.id)
        if announce_id not in self.cart:
            self.cart[announce_id] = {'quantity': 0, 'price': str(announce.price)}
        if update_quantity:
            self.cart[announce_id]['quantity'] = quantity
        else:
            self.cart[announce_id]['quantity'] += quantity
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, announce):
        """
        Remove a announce from the cart.
        """
        announce_id = str(announce.id)
        if announce_id in self.cart:
            del self.cart[announce_id]
            self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
