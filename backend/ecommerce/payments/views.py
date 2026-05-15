import razorpay
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from .models import Payment
from order.models import Order

client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


# =========================
# 1. INIT PAYMENT
# =========================
class PaymentInitView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        order_id = request.data.get("order_id")

        # validate order
        order = get_object_or_404(
            Order,
            id=order_id,
            user=request.user,
            status="PENDING"
        )

        # prevent duplicate payment
        if Payment.objects.filter(order=order).exists():
            return Response(
                {"error": "Payment already initiated for this order"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # create razorpay order
        razorpay_order = client.order.create({
            "amount": int(order.total_price * 100),  # paise
            "currency": "INR",
            "payment_capture": 1
        })

        # save payment in DB
        payment = Payment.objects.create(
            order=order,
            razorpay_order_id=razorpay_order["id"],
            amount=order.total_price,
            status="CREATED"
        )

        return Response({
            "razorpay_order_id": razorpay_order["id"],
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "amount": razorpay_order["amount"],
            "currency": "INR"
        }, status=status.HTTP_200_OK)


# =========================
# 2. VERIFY PAYMENT
# =========================
class PaymentVerifyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data

        # get payment
        payment = get_object_or_404(
            Payment,
            razorpay_order_id=data.get("razorpay_order_id")
        )

        # verify signature
        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": data["razorpay_order_id"],
                "razorpay_payment_id": data["razorpay_payment_id"],
                "razorpay_signature": data["razorpay_signature"],
            })

        except razorpay.errors.SignatureVerificationError:
            payment.status = "FAILED"
            payment.save()

            return Response(
                {"error": "Payment verification failed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # update payment
        payment.razorpay_payment_id = data["razorpay_payment_id"]
        payment.razorpay_signature = data["razorpay_signature"]
        payment.status = "PAID"
        payment.save()

        # update order
        order = payment.order
        order.status = "PAID"
        order.save()

        # OPTIONAL: reduce stock
        for item in order.items.all():
            product = item.product
            product.stock -= item.quantity
            product.save()

        return Response({
            "message": "Payment successful",
            "order_id": order.id,
            "status": order.status
        }, status=status.HTTP_200_OK)