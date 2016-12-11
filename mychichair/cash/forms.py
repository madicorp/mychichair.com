from payments.forms import PaymentForm


class CashPaymentForm(PaymentForm):
    def __init__(self, data=None, action='', method='post', provider=None,
                 payment=None, hidden_inputs=True, autosubmit=True):
        super(PaymentForm, self).__init__(data, action, method, provider, payment, hidden_inputs, autosubmit)
