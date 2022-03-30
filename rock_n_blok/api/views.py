import random
import string

from django.http import QueryDict
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Token
from .serializers import TokenSerializer


def generate_alphanum_random_string(length):
    """ Returns a random alphanumeric string """
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.sample(letters_and_digits, length))


@api_view(['POST'])
def create(request):
    """ creates a token object """
    unique_hash = generate_alphanum_random_string(20)
    if isinstance(request.data, QueryDict):
        request.data._mutable = True
        request.data['unique_hash'] = unique_hash
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list(request):
    """ Returns token objects """
    tokens = Token.objects.all()
    serializer = TokenSerializer(tokens, many=True)
    return Response(serializer.data)
