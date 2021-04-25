import json

from django.conf import settings
from django.shortcuts import redirect

from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework_tracking.mixins import LoggingErrorsMixin

from .serializers import PaymentConfigSerializer

from zeep import Client

from apps.accounts.permissions import ProfileComplete
from apps.team.permissions import HasTeam

from .models import PaymentRequest, PaymentConfig


class PaymentRequestAPIView(LoggingErrorsMixin, GenericAPIView):
    permission_classes = (IsAuthenticated, ProfileComplete, HasTeam)

    def post(self, request):
        client = Client(settings.ZARRIN_PAL_CLIENT)

        amount = PaymentConfig.objects.last().amount

        if self.request.user.team.is_finalist and \
                self.request.user.team.level_one_payed:
            amount -= 160000

        payment_request = PaymentRequest.objects.create(
            user=request.user,
            amount=amount,
            team_name=request.user.team.name
        )

        if amount <= 0:
            self.request.user.profile.payed = True
            self.request.user.profile.save()

            return Response(status=status.HTTP_201_CREATED)

        result = client.service.PaymentRequest(
            settings.MERCHANT_ID,
            payment_request.amount,
            payment_request.description,
            payment_request.user.email,
            payment_request.user.profile.phone_number,
            payment_request.callback_url
        )

        if result.Status == 100:
            payment_request.authority = str(result.Authority)
            if len(payment_request.authority) != 36:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            payment_request.save()
            url = settings.ZARRIN_PAL_START_PAY.format(
                payment_request.authority)

            return Response(data={'url': url},
                            status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class PaymentVerifyAPIView(LoggingErrorsMixin, GenericAPIView):

    def get(self, request):
        client = Client(settings.ZARRIN_PAL_CLIENT)

        if request.GET.get('Status') == 'OK':
            authority = request.GET['Authority']
            payment_request = get_object_or_404(PaymentRequest,
                                                authority=authority)
            result = client.service.PaymentVerification(
                settings.MERCHANT_ID,
                authority,
                payment_request.amount
            )
            if result.Status == 100:
                payment_request.ref_id = str(result.RefID)
                payment_request.save()
                team = payment_request.get_team()

                # team.level_one_payed = True
                team.final_payed = True
                team.save()

                return redirect(
                    f'https://aichallenge.ir/dashboard/payment'
                    f'?ref_id={payment_request.ref_id}'
                    f'&status=100&desc=با موفقیت پرداخت شد')
            if result.Status == 101:
                return redirect(
                    f'https://aichallenge.ir/dashboard/payment'
                    f'?status={str(result.Status)}&desc=تراکنش ثبت شد'
                )
            return redirect(
                f'https://aichallenge.ir/dashboard/payment'
                f'?status={str(result.Status)}&desc=تراکنش ناموفق'
            )

        return redirect(
            f'https://aichallenge.ir/dashboard/payment'
            f'?status=-1&desc=تراکنش ناوفق بود و یا توسط کاربر لغو شد'
        )


class PaymentConfigAPIView(LoggingErrorsMixin, GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PaymentConfigSerializer

    def get(self, request):
        config = PaymentConfig.objects.all().last()

        amount = config.amount

        return Response(
            data={'config': {
                'amount': amount,
                'description': config.description,
            }},
            status=status.HTTP_200_OK)
