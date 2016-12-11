from __future__ import unicode_literals

from mychichair.cart.forms import ReplaceCartLineForm
from mychichair.core.utils import to_local_currency
from .decorators import get_cart_from_request, get_or_empty_db_cart


def cart_counter(request):
    """ Return number of items from cart """
    cart = get_cart_from_request(request)
    return {'cart_counter': cart.quantity}


@get_or_empty_db_cart
def cart_lines(request, cart):
    discounts = request.discounts
    cart_line_list = []

    for line in cart:
        initial = {'quantity': line.get_quantity()}
        form = ReplaceCartLineForm(None, cart=cart, variant=line.variant,
                                   initial=initial, discounts=discounts)
        cart_line_list.append({
            'variant': line.variant,
            'quantity': line.get_quantity(),
            'get_price_per_item': line.get_price_per_item(discounts),
            'get_total': line.get_total(discounts=discounts),
            'form': form})

    cart_total = None
    local_cart_total = None
    if cart:
        cart_total = cart.get_total(discounts=discounts)
        local_cart_total = to_local_currency(cart_total, request.currency)

    return {
        'cart_lines': cart_line_list,
        'cart_total': cart_total,
        'local_cart_total': local_cart_total,
    }
