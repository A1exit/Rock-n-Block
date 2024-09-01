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
    token_unique_hash = generate_random_alphanumeric_string(20)

    if isinstance(request.data, QueryDict):
        request.data._mutable = True
        request.data["unique_hash"] = token_unique_hash

    serializer = TokenSerializer(data=request.data)

    if serializer.is_valid():
        try:
            with transaction.atomic():
                serializer.save()

                try:
                    web3_instance = create_web3_connection()
                    smart_contract_abi = load_smart_contract_abi(os.path.join(settings.BASE_DIR, "api/abi.json"))
                    smart_contract = get_smart_contract(web3_instance, settings.CONTRACT_ADDRESS, smart_contract_abi)
                    transaction_hash = send_mint_transaction(
                        web3_instance,
                        smart_contract,
                        request.data.get("owner"),
                        token_unique_hash,
                        request.data.get("media_url"),
                    )
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                token = Token.objects.get(unique_hash=token_unique_hash)
                updated_token_data = {"tx_hash": transaction_hash}
                serializer = TokenSerializer(token, data=updated_token_data, partial=True)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
        web3_instance = create_web3_connection()
        smart_contract_abi = load_smart_contract_abi(os.path.join(settings.BASE_DIR, "api/abi.json"))
        smart_contract = get_smart_contract(web3_instance, settings.CONTRACT_ADDRESS, smart_contract_abi)

        total_token_supply = smart_contract.functions.totalSupply().call()
        return JsonResponse({"result": total_token_supply}, status=status.HTTP_200_OK)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
