import json
import random
import string
from typing import Dict

from django.conf import settings
from web3 import Web3
from web3.contract import Contract


def create_web3_connection() -> Web3:
    """
    Initialize and return a Web3 instance connected to the Ethereum node.
    Returns:
        Web3: An instance of Web3 connected to the specified Ethereum node.
    """
    ethereum_node_url = settings.INFURA_ETH_NODE_URL.format(infura_key=settings.INFURA_API_KEY)
    return Web3(Web3.HTTPProvider(ethereum_node_url))


def load_smart_contract_abi(filepath: str) -> Dict:
    """
    Load and return the ABI of a smart contract.
    Args:
        filepath (str): Path to the JSON file containing the ABI.
    Returns:
        dict: The ABI of the smart contract as a dictionary.
    """
    with open(filepath) as f:
        return json.load(f)


def get_smart_contract(web3_instance: Web3, contract_address: str, abi: Dict) -> Contract:
    """
    Create and return a smart contract instance using Web3.
    Args:
        web3_instance (Web3): An instance of Web3 connected to the Ethereum node.
        contract_address (str): The address of the smart contract on the blockchain.
        abi (dict): The ABI of the smart contract.
    Returns:
        Contract: A Web3 contract instance to interact with the smart contract.
    """
    return web3_instance.eth.contract(address=contract_address, abi=abi)


def generate_random_alphanumeric_string(length: int) -> str:
    """
    Generate a random alphanumeric string of specified length.
    Args:
        length (int): The length of the random string to generate.
    Returns:
        str: A random alphanumeric string.
    """
    characters = string.ascii_letters + string.digits
    return "".join(random.sample(characters, length))


def send_mint_transaction(w3, contract, owner, unique_hash, media_url):
    """
    Builds, signs, and sends a mint transaction to the Ethereum blockchain.

    Args:
        w3 (Web3): The Web3 instance connected to the Ethereum network.
        contract (Contract): The smart contract instance.
        owner (str): The Ethereum address of the token owner.
        unique_hash (str): The unique identifier for the token.
        media_url (str): The media URL associated with the token.

    Returns:
        str: The transaction hash of the sent transaction.
    """
    nonce = w3.eth.get_transaction_count(settings.INFURA_API_KEY)
    mint_txn = contract.functions.mint(
        owner,
        unique_hash,
        media_url,
    ).buildTransaction(
        {
            "chainId": w3.eth.chain_id,
            "gas": settings.GAS_LIMIT,
            "gasPrice": w3.toWei(settings.GAS_PRICE_GWEI, "gwei"),
            "nonce": nonce,
        }
    )
    signed_txn = w3.eth.account.sign_transaction(mint_txn, private_key=settings.SENDER_PRIVATE_KEY)
    tx_hash = w3.toHex(w3.keccak(signed_txn.rawTransaction))
    w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return tx_hash
