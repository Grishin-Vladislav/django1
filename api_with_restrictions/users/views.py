from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import SignUpSerializer


@api_view(http_method_names=['POST'])
def register(request):
    input_serializer = SignUpSerializer(data=request.data)
    input_serializer.is_valid(raise_exception=True)
    input_serializer.save()
    return Response(input_serializer.data, status=status.HTTP_201_CREATED)

