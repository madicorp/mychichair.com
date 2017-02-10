from django.utils.translation import pgettext_lazy


class Status(object):
    NEW = 'new'
    CANCELLED = 'cancelled'
    SHIPPED = 'shipped'
    PAYMENT_PENDING = 'payment-pending'
    FULLY_PAID = 'fully-paid'

    CHOICES = [
        (NEW, pgettext_lazy('order status', 'En traitement')),
        (CANCELLED, pgettext_lazy('order status', 'Annulé')),
        (SHIPPED, pgettext_lazy('order status', 'Envoyé')),
        (PAYMENT_PENDING, pgettext_lazy('order status', 'Paiement en cours')),
        (FULLY_PAID, pgettext_lazy('order status', 'Payé complètement'))]
