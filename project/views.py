# from django.core import serializers
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from pipe.models import Pipe, Record
#
#
# class APITestView(APIView):
#
#     def get(self, request, format=None, **kwargs):
#
#         parts = serializers.serialize('json', list(Pipe.objects.all()))
#         record = serializers.serialize('json', list(Record.objects.all()))
#
#         data = {
#             "Part Data": parts,
#             "Pipe Record": record,
#         }
#         return Response(data)