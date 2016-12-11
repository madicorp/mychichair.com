from payments import RedirectNeeded
from payments.core import BasicProvider

from mychichair.cash.forms import CashPaymentForm


class CashPaymentProvider(BasicProvider):
    def get_form(self, payment, data=None):
        if payment.status == 'waiting':
            payment.change_status('input')
        form = CashPaymentForm(self.get_hidden_fields(payment), self.get_action(payment), self._method)
        if form.is_valid():
            payment.change_status('preauth')
            raise RedirectNeeded(payment.get_success_url())
        return form

    def get_token_from_request(self, payment, request):
        pass

    def capture(self, payment, amount=None):
        if amount is None:
            amount = payment.total
        payment.change_status('confirmed')
        return amount

    def get_hidden_fields(self, payment):
        pass

    def refund(self, payment, amount=None):
        return amount or 0

    def release(self, payment):
        return None

    def process_data(self, payment, request):
        pass
