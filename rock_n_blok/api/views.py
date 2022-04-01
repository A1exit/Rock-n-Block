import random
import string
import web3
import os
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
import json

from django.http import QueryDict
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse

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


@api_view(['GET'])
def total_supply(request):
    infura_key = os.getenv('INFURA_KEY')
    w3 = Web3(Web3.HTTPProvider(f'https://rinkeby.infura.io/v3/{infura_key}'))
    with open('api/abi.json') as f:
        contract_abi = json.load(f)
    my_contract = w3.eth.contract(address=os.getenv('CONTRACT_ADDRESS'),
                                  abi=contract_abi)
    return HttpResponse('result:'
                        f'{my_contract.functions.totalSupply().call()}')
