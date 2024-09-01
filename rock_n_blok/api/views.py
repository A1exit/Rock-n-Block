import os

from django.db import transaction
from django.http import QueryDict, JsonResponse
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings

from .models import Token
from .pagination import StandardResultsSetPagination
from .serializers import TokenSerializer
from .services import (
    create_web3_connection,
    load_smart_contract_abi,
    get_smart_contract,
    generate_random_alphanumeric_string,
    send_mint_transaction,
)


@api_view(("POST",))
def create_token(request):
    """
    Create a new token and mint it on the Ethereum blockchain.
    Returns:
        Response: JSON with the token data or an error message.
    """
    unique_hash = generate_random_alphanumeric_string(20)

    if isinstance(request.data, QueryDict):
        request.data._mutable = True
        request.data["unique_hash"] = unique_hash

    serializer = TokenSerializer(data=request.data)

    if serializer.is_valid():
        try:
            with transaction.atomic():
                serializer.save()

                try:
                    w3 = create_web3_connection()
                    contract_abi = load_smart_contract_abi(os.path.join(settings.BASE_DIR, "api/abi.json"))
                    contract = get_smart_contract(w3, settings.CONTRACT_ADDRESS, contract_abi)
                    tx_hash = send_mint_transaction(
                        w3, contract, request.data.get("owner"), unique_hash, request.data.get("media_url")
                    )
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                token = Token.objects.get(unique_hash=unique_hash)
                data = {"tx_hash": tx_hash}
                serializer = TokenSerializer(token, data=data, partial=True)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenListAPIView(generics.ListAPIView):
    """
    list of all Token objects stored in the database.
    """

    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    pagination_class = StandardResultsSetPagination
    http_method_names = ("get",)


@api_view(["GET"])
def get_total_supply(request):
    """
    Retrieve the total supply of tokens from the Ethereum blockchain.
    Returns:
        JsonResponse: JSON with the total supply or an error message.
    """
    try:
        w3 = create_web3_connection()
        contract_abi = load_smart_contract_abi(os.path.join(settings.BASE_DIR, "api/abi.json"))
        contract = get_smart_contract(w3, settings.CONTRACT_ADDRESS, contract_abi)

        total_supply_value = contract.functions.totalSupply().call()
        return JsonResponse({"result": total_supply_value}, status=status.HTTP_200_OK)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
