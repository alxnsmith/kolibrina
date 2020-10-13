from django.views import View
from django.http import JsonResponse, HttpResponse


class PaymentAPI(View):
    @staticmethod
    def get(request):
        print(request.GET)
        return JsonResponse({'status': 'OK'})

    @staticmethod
    def post(request):
        print(request.POST)
        return JsonResponse({'status': 'OK'})
