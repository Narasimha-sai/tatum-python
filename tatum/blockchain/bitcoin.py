import http.client
import json
import validator.blockchain as blockchain_validator
import requests
import os
from dotenv import load_dotenv
load_dotenv()

conn = http.client.HTTPSConnection(os.environ['API_URL'])
API_KEY = os.environ['API_KEY']

def headers(for_post = False):
    if for_post:
        return {
            'content-type': "application/json",
            'x-api-key': API_KEY
            }
    else:
        return {
            'x-api-key': API_KEY
            }

def generate_bitcoin_wallet(query_params={}):
    if blockchain_validator.generate_wallet(query_params):
        if query_params != {}:
            conn.request("GET", "/v3/bitcoin/wallet?mnemonic={}".format(query_params['mnemonic']), headers=headers())
        else:
            conn.request("GET", "/v3/bitcoin/wallet", headers=headers())
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

def generate_bitcoin_deposit_address_from_extended_public_key(path_params):
    if blockchain_validator.generate_deposit_address_from_extended_public_key(path_params):
        conn.request("GET", "/v3/bitcoin/address/{}/{}".format(path_params['xpub'], path_params['index']), headers=headers())
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

def generate_bitcoin_private_key(body_params):
    if blockchain_validator.generate_private_key(body_params):
        body_params = json.dumps(body_params)
        conn.request("POST", "/v3/bitcoin/wallet/priv", body_params, headers=headers(for_post=True))
        res = conn.getresponse()
        data = res.read()


def get_blockchain_information():
    conn.request("GET", "/v3/bitcoin/info", headers=headers())
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

def get_block_hash(path_params):
    if blockchain_validator.get_block_hash(path_params):
        conn.request("GET", "/v3/bitcoin/block/hash/{}".format(path_params['i']), headers=headers())
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

def get_block_by_hash_or_height(path_params):
    if blockchain_validator.get_block_by_hash_or_height(path_params):
        conn.request("GET", "/v3/bitcoin/block/{}".format(path_params['hash']), headers=headers())
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

def get_transaction_by_hash(path_params):
    if blockchain_validator.get_block_by_hash_or_height(path_params):
        conn.request("GET", "/v3/bitcoin/transaction/{}".format(path_params['hash']), headers=headers())
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

def get_transaction_by_address(path_params, query_params):
    if blockchain_validator.get_transaction_by_address(path_params, query_params):
        if len(query_params) != 1:
            conn.request("GET", "/v3/bitcoin/transaction/address/{}?pageSize={}&offset={}".format(path_params['address'], query_params['pageSize'], query_params['offset']), headers=headers())
        else:
            conn.request("GET", "/v3/bitcoin/transaction/address/{}?pageSize={}".format(path_params['address'], query_params['pageSize']), headers=headers())
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

def get_utxo_of_transaction(path_params):
    if blockchain_validator.get_utxo_of_transaction(path_params):
        conn.request("GET", "/v3/bitcoin/utxo/{}/{}".format(path_params['hash'], path_params['index']), headers=headers())
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

def send_bitcoin_to_blockchain_addresses(body_params):
    if blockchain_validator.send_bitcoin_to_blockchain_addresses(body_params):
        body_params = json.dumps(body_params)
        conn.request("POST", "/v3/bitcoin/transaction", body_params, headers=headers(for_post=True))
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

def broadcast_signed_bitcoin_transaction(body_params):
    if blockchain_validator.broadcast_signed_transaction(body_params):
        body_params = json.dumps(body_params)
        conn.request("POST", "/v3/bitcoin/broadcast", body_params, headers=headers(for_post=True))
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")