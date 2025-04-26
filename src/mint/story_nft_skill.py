import requests
import json
from datetime import datetime
from groq import Groq  
import os
from web3 import Web3
from dotenv import load_dotenv
from io import BytesIO
from requests_toolbelt import MultipartEncoder
from src.database.mongo_manager import (
    save_story_nft
)

load_dotenv()

MONAD_RPC = "https://testnet-rpc.monad.xyz"  
CONTRACT_ADDRESS = os.getenv("STORY_NFT_ADDRESS")
PRIVATE_KEY = os.getenv("OWNER_PRIVATE_KEY")  
OWNER_ADDRESS = os.getenv("OWNER_ADDRESS")

with open("StoryNFT_ABI.json", "r") as abi_file:
    CONTRACT_ABI = json.load(abi_file)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

def generate_story(prompt: str) -> str:
    story_prompt = (
        f"Create a short story (max 600 words) based on this idea: {prompt}. "
        f"The story should be vivid, imaginative, and self-contained. Focus on a clear setting, "
        f"a single character or pair of characters, a central conflict, and a meaningful or surprising resolution. "
        f"Write it in a tone that fits the idea, suitable for an NFT minting."
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role" : "user",
                "content" : story_prompt
            }
        ],
        model="llama-3.3-70b-versatile"
    )
    return chat_completion.choices[0].message.content.strip()


def upload_to_ipfs(content: str,filename: str = None) -> str:
    file_stream = BytesIO(content.encode("utf-8"))
    file_stream.name = filename or f"story_{datetime.utcnow().timestamp()}.txt"

    metadata = {
        "name": "StoryNFT",
        "keyvalues": {
            "type": "story",
            "uploaded": str(datetime.utcnow())
        }
    }

    options = {
        "network": "public"
    }

    m = MultipartEncoder(
        fields={
            "file": (file_stream.name, file_stream, "text/plain"),
            "metadata": (None, json.dumps(metadata), "application/json"),
            "options": (None, json.dumps(options), "application/json"),
            "network": "public"
        }
    )

    headers = {
        "Authorization": f"Bearer {os.getenv('PINATA_JWT')}",
        "Content-Type": m.content_type
    }

    response = requests.post("https://uploads.pinata.cloud/v3/files", headers=headers, data=m)

    if response.status_code == 200:
        ipfs_hash = response.json().get("data").get("cid")
        return f"https://amethyst-decent-stingray-48.mypinata.cloud/ipfs/{ipfs_hash}"
    else:
        raise Exception(f"[Pinata Upload Failed] {response.status_code} - {response.text}")

def mint_story_nft(ipfs_link: str, title: str, user_wallet: str) -> dict:
    w3 = Web3(Web3.HTTPProvider(MONAD_RPC))
    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    
    nonce = w3.eth.get_transaction_count(OWNER_ADDRESS)
    import math
    block = w3.eth.get_block("latest")
    base_fee = block.get("baseFeePerGas")

    max_fee_per_gas = math.ceil(base_fee * 1.251)
    priority_fee = w3.to_wei("2", "gwei") 

    txn = contract.functions.mint(user_wallet, ipfs_link).build_transaction({
        "from": OWNER_ADDRESS,
        "nonce": nonce,
        "gas": 500000,
        "maxFeePerGas": max_fee_per_gas,
        "maxPriorityFeePerGas": priority_fee
    })

    signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn["raw_transaction"])

    return {
        "status": "minted",
        "tx_hash": tx_hash.hex(),
        "network": "Monad",
        "title": title,
        "recipient": user_wallet,
        "token_uri": ipfs_link,
        "timestamp": str(datetime.utcnow())
    }


def handle_story_and_mint(user_id: str,prompt: str, user_wallet: str) -> dict:
    print("[📖] Generating story...")
    story = generate_story(prompt)
    
    print("[🌀] Uploading to IPFS...")
    ipfs_url = upload_to_ipfs(story)

    print("[🪙] Minting on Monad...")
    title = prompt.strip().split(" ")[0:6]
    result = mint_story_nft(ipfs_url, title=" ".join(title), user_wallet=user_wallet)

    saved_nft = {
        **result,
        "prompt": prompt,
        "story_preview": story[:300] + "...",
        "created_at": datetime.utcnow()
    }

    save_story_nft(user_id,saved_nft)

    return {
        "message": "Your story NFT has been minted!",
        "story_preview": story[:300] + "...",
        "ipfs_url": ipfs_url,
        "nft_metadata": result
    }
