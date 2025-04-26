from web3 import Web3
from eth_account import Account
import os
import json
from dotenv import load_dotenv
import math

load_dotenv(override=True)

provider = Web3.HTTPProvider("https://testnet-rpc.monad.xyz")
w3 = Web3(provider)
PRIVATE_KEY = os.getenv("OWNER_PRIVATE_KEY")
ACCOUNT = Account.from_key(PRIVATE_KEY)
ADDRESS = ACCOUNT.address

with open("MazeGameABI.json", "r") as f:
    abi = json.load(f)

contract = w3.eth.contract(address=os.getenv("MAZE_CONTRACT_ADDRESS"), abi=abi)

def get_tx_params():
    block = w3.eth.get_block("latest")
    base_fee = block.get("baseFeePerGas", w3.to_wei("1", "gwei"))
    max_fee = math.ceil(base_fee * 1.25)
    priority_fee = w3.to_wei("2", "gwei")

    return {
        "from": ADDRESS,
        "nonce": w3.eth.get_transaction_count(ADDRESS),
        "gas": 500000,
        "maxFeePerGas": max_fee,
        "maxPriorityFeePerGas": priority_fee
    }

def get_path_hash_from_contract(path: list[str]) -> bytes:
    """
    Calls the contract's hashPath function with the string array path to get the keccak hash.
    """
    return contract.functions.hashPath(path).call()

def create_duel(path: list[str]) -> int:
    path_hash = get_path_hash_from_contract(path)
    tx_params = get_tx_params()

    txn = contract.functions.createDuel(path_hash).build_transaction(tx_params)
    signed = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed["raw_transaction"])
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    logs = contract.events.DuelCreated().process_receipt(receipt)
    return logs[0]['args']['duelId']

def submit_guess(duel_id: int, path: list[str]) -> str:
    tx_params = get_tx_params()
    txn = contract.functions.submitGuess(duel_id, path).build_transaction(tx_params)
    signed = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed["raw_transaction"])
    return tx_hash.hex()

def reveal_maze(duel_id: int, path: list[str]) -> str:
    tx_params = get_tx_params()
    txn = contract.functions.revealMaze(duel_id, path).build_transaction(tx_params)
    signed = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed["raw_transaction"])
    return tx_hash.hex()

def get_winner(duel_id: int) -> str:
    winner = contract.functions.getWinner(duel_id).call()
    return None if winner == "0x0000000000000000000000000000000000000000" else winner
