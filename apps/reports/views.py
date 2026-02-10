from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import sales_report, purchase_report, outstanding_payments

class SalesReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start = request.GET.get("start_date")
        end = request.GET.get("end_date")

        data = sales_report(start, end)
        return Response(data)


class PurchaseReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start = request.GET.get("start_date")
        end = request.GET.get("end_date")

        data = purchase_report(start, end)
        return Response(data)


class OutstandingPaymentReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = outstanding_payments()
        return Response(data)
