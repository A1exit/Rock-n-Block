import json
import os
import random
import string

from django.http import HttpResponse, QueryDict
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from web3 import Web3

from .models import Token
from .pagination import StandardResultsSetPagination
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
        infura_key = os.getenv('INFURA_KEY')
        w3 = Web3(
            Web3.HTTPProvider(f'https://rinkeby.infura.io/v3/{infura_key}'))
        with open('api/abi.json') as f:
            contract_abi = json.load(f)
        unicorns = w3.eth.contract(
            address=os.getenv('CONTRACT_ADDRESS'),
            abi=contract_abi)
        nonce = w3.eth.get_transaction_count(os.getenv('METAMASK_KEY'))
        unicorn_txn = unicorns.functions.mint(
            '0x3f43e8DdC847aD8bffeD22B1D2b8f667924C9641',
            unique_hash,
            request.data.get('media_url')).buildTransaction(
            {
                'chainId': 4,
                'gas': 200000,
                'gasPrice': w3.toWei('2', 'gwei'),
                'nonce': nonce
            })
        signed_txn = w3.eth.account.sign_transaction(unicorn_txn,
                                                     private_key=os.getenv(
                                                         'PRIVATE_KEY')
                                                     )
        w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_hash = w3.toHex(w3.keccak(signed_txn.rawTransaction))
        token = Token.objects.get(unique_hash=unique_hash)
        data = {'tx_hash': tx_hash}
        serializer = TokenSerializer(token, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


class ListTokensViewSet(viewsets.ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    pagination_class = StandardResultsSetPagination
    http_method_names = ["get"]


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
