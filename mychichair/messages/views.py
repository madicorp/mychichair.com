import uuid

from django.conf import settings
from django.core import mail
from django.core.mail import EmailMessage
from django.http import BadHeaderError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


def __send_contact_email(user_email, user_name, user_subject, user_message, ref_num, connection):
    contact_mail_ref = '#{} : {} de {}'.format(ref_num, user_subject, user_name)
    EmailMessage(subject=contact_mail_ref, from_email=settings.CONTACT_EMAIL,
                 body=user_message, to=[settings.CONTACT_EMAIL],
                 reply_to=[user_email], headers={'Sender': user_email},
                 connection=connection).send()


def __send_confirmation_email(user_email, user_name, user_subject, user_message, ref_num, connection):
    confirmation_mail_ref = '#{} : {}'.format(ref_num, user_subject)
    confirmation_mail_body_p1 = 'Cher/Chère {},\n\nNous avons reçu votre demande #{}: {} et vous répondrons bientôt.\n' \
        .format(user_name, ref_num, user_subject)
    confirmation_mail_body_p2 = \
        'Votre demande :\n\n%s\n\nChiquement votre,\n\nMy Chic Hair' % user_message
    EmailMessage(subject=confirmation_mail_ref, from_email=settings.CONTACT_EMAIL,
                 body=(confirmation_mail_body_p1 + confirmation_mail_body_p2), to=[user_email],
                 connection=connection).send()


@api_view(['POST'])
def post_message(request):
    if 'POST' == request.method:
        data = request.data
        try:
            with mail.get_connection() as connection:
                ref_num = uuid.uuid4()
                user_name = data['name']
                user_subject = data['subject']
                user_message = data['message']
                user_email = data['email']
                __send_contact_email(user_email, user_name, user_subject, user_message, ref_num, connection)
                __send_confirmation_email(user_email, user_name, user_subject, user_message, ref_num, connection)
        except BadHeaderError:
            # Headers injection prevention
            # https://docs.djangoproject.com/fr/1.10/topics/email/#preventing-header-injection
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)
