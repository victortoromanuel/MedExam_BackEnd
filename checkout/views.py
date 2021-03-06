from django.http import JsonResponse
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from checkout.forms import PaymentNotificationForm
        

@method_decorator(csrf_exempt, name='dispatch')
class PaymentNotificationView(APIView):
    """
    If youre site is restricted with "basic access authentication" or similar, disable it for the confirmation url.
    The IP associated with the confirmation URL should be public; no access from intranet or localhost.
    If you're using https, you must make sure you have a valid certificate.
    Temporarily, do not use security certificates elliptic curve or those who have the suite of encryption
    TLS_ECDHE_ECDSA_WITH_RC4_128_SHA in your payment requests.
    PayU assumes that the confirmation page is reported correctly if the system receives the HTTP 200 code;
    otherwise, it will make a maximum of nine (9) attempts to send the confirmation page to your system.
    If, after these attempts, HTTP 200 code is received, the system sends an email alert.
    PayU reports the confirmation page once the transaction has a final status, ie, when approved, rejected or expired.
    If a transaction is in progress (waiting for payment or analysis), it will not report until it has a final status.
    """
    form_class = PaymentNotificationForm

    def post(self, request):

        post = request.data
        post['test'] = bool(int(post['test']))
        #post['INSTALLMENTS_NUMBER'] = post['INSTALLMENTS_NUMBER'] if post['INSTALLMENTS_NUMBER'] else 0
        print(post)
        form = self.form_class(post)
        if form.is_valid():
            print("hi")
            payment_notification = form.save(commit=False)
            payment_notification.raw = json.dumps(request.POST)
            payment_notification.save()
            return HttpResponse(status=200)
        return HttpResponse(status=400)