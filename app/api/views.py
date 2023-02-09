import csv
import io
from copy import deepcopy
from itertools import groupby

from django.db import transaction
from django.core.cache import cache
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import parsers, response, status, views
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.models import Deal
from api.serializers import DealSerializer, UploadSerializer


class DealsView(views.APIView):
    """
    Deals class view.
    """
    parser_classes = (
        parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser
    )

    @swagger_auto_schema(
        operation_description='Get customers',
        operation_id='Get customers'
    )
    @method_decorator(cache_page(60 * 60 * 24))
    def get(self, request):
        deals = Deal.objects.order_by('customer')
        result = []
        for client, group in groupby(deals, key=lambda x: x.customer):
            group = list(group)
            result.append(
                {
                    'username': client,
                    'spent_money': sum(x.total for x in group),
                    'gems': list(set([x.item for x in group]))
                }
            )
        result = sorted(result, key=lambda x: x['spent_money'], reverse=True)[:5]
        copy_result = deepcopy(result)
        for index, client in enumerate(copy_result):
            for gem in client['gems']:
                matches = 0
                for other in copy_result:
                    if gem in other['gems']:
                        matches += 1
                if matches < 2:
                    result[index]['gems'].remove(gem)
        data = {'response': result}

        return JsonResponse(data, safe=False)

    @swagger_auto_schema(
        operation_description='Upload csv file',
        operation_id='Upload csv file',
        manual_parameters=[openapi.Parameter(
            name="file",
            in_=openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            required=True,
            description='Document'
        )],
        responses={400: 'Invalid data in uploaded file',
                   200: 'Success'},
    )
    def post(self, request):
        serializer = UploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = io.TextIOWrapper(
            serializer.validated_data['file'],
            encoding='utf-8'
        )
        reader = csv.DictReader(file)

        with transaction.atomic():
            for row in reader:
                try:
                    Deal.objects.create(
                        customer=row['customer'],
                        item=row['item'],
                        total=row['total'],
                        quantity=row['quantity'],
                        date=row['date']
                    )
                except Exception as e:
                    return response.Response(
                        {
                            'status': 'Error',
                            'detail': f'в процессе обработки файла произошла ошибка: {str(e)}'
                        },
                        status.HTTP_400_BAD_REQUEST
                    )

        cache.clear()
        return response.Response(
            {"status": "OK"},
            status.HTTP_201_CREATED
        )

