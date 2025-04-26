from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv(override=True)

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "persona_bot"
COLLECTION_NAME = "user_profiles"
CHAT_COLLECTION_NAME = "chat_history"
AWAY_COLLECTION_NAME = "away_logs"
STORY_NFT_COLLECTION_NAME = "story_nft"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]
chat_collection = db[CHAT_COLLECTION_NAME]
away_collection = db[AWAY_COLLECTION_NAME]
story_nft_collection = db[STORY_NFT_COLLECTION_NAME]

def get_default_profile_data():
    return {
        "name": "",
        "bio": "",
        "location": "",
        "age": None,
        "mode": "fun",
        "away": False,
        "communication_style": {
            "tone": "",
            "favorite_phrases": [],
            "humor_preference": ""
        },
        "professional": {
            "job_title": "",
            "skills": [],
            "experience": "",
            "projects": [],
            "linkedin": "",
            "github": "",
            "website": ""
        },
        "personal": {
            "interests": [],
            "hobbies": [],
            "favorite_movies": [],
            "favorite_music": [],
            "favorite_books": []
        },
    }


def save_user_auth(user_id: str, hashed_password: str): 
    collection.update_one(
        {"user_id": user_id},
        {"$set": {"user_id": user_id, "password": hashed_password,"plan":"Basic", "analytics": {"emails": 0, "switches": 0, "commands": 0}}},
        upsert=True
    )

def get_user_auth(user_id: str):
    doc = collection.find_one({"user_id": user_id})
    return doc.get("password") if doc else None

def save_user_profile(user_id: str, profile_data: dict, type: str):
    if( type == "register"):
        collection.update_one(
            {"user_id": user_id},
            {"$set": {
                "password": profile_data,
                "plan": "Basic",
                "analytics": {"emails": 0, "switches": 0, "commands": 0},
                "profile": get_default_profile_data()
            }},
            upsert=True
        )
    else:
        collection.update_one(
            {"user_id": user_id},
            {"$set": {"profile": profile_data}},
            upsert=True
        )

def get_user_profile(user_id: str):
    doc = collection.find_one({"user_id": user_id}, {"_id": 0})
    return doc.get("profile") if doc else None

def update_user_field(user_id: str, updates: dict):
    return collection.update_one(
        {"user_id": user_id},
        {"$set": {"profile": updates}},
    )

def delete_user_profile(user_id: str):
    return collection.delete_one({"user_id": user_id})

def set_mode_mongo(user_id: str, mode: str):
    collection.update_one(
        {"user_id": user_id},
        {"$set": {"profile.mode": mode}}
    )
    return collection.update_one({"user_id": user_id}, {"$set": {"mode": mode}})

def set_away_mongo(user_id: str, away: bool):
    if away:
        start_away_session(user_id)
    else:
        end_away_session(user_id)
    return collection.update_one(
        {"user_id": user_id},
        {"$set": {"profile.away": away}}
    )

def set_chat(user_id: str, user_input: str, response: str):
    chat_collection.update_one(
        {"user_id": user_id},
        {"$push": {"chat": {
            "sender": "user",
            "content": user_input,
            "timestamp": datetime.now().isoformat()
        }}},
        upsert=True
    )

    chat_collection.update_one(
        {"user_id": user_id},
        {"$push": {"chat": {
            "sender": "bot",
            "content": response,
            "timestamp": datetime.now().isoformat()
        }}},
        upsert=True
    )

def get_chat(user_id: str):
    doc = chat_collection.find_one({"user_id": user_id}, {"_id": 0})
    return doc.get("chat") if doc else None


def increment_email_count(user_id: str):
    return collection.update_one(
        {"user_id": user_id},
        {"$inc": {"analytics.emails": 1, "chat_count": 1}},
        upsert=True
    )

def increment_switch_count(user_id: str):
    return collection.update_one(
        {"user_id": user_id},
        {"$inc": {"analytics.switches": 1,}},
        upsert=True
    )

def increment_command_count(user_id: str):
    return collection.update_one(
        {"user_id": user_id},
        {"$inc": {"analytics.commands": 1, "chat_count": 1}},
        upsert=True
    )

def get_analytics(user_id: str):
    doc = collection.find_one({"user_id": user_id}, {"_id": 0, "analytics": 1, "plan" : 1})
    plan = doc.get("plan")

    return {
        "analytics": doc.get("analytics") if doc else None,
        "plan": plan,
    }

def start_away_session(user_id: str):
    away_collection.insert_one({
        "user_id": user_id,
        "start_time": datetime.utcnow(),
        "end_time": None,
        "messages": []
    })

def end_away_session(user_id: str):
    return away_collection.update_one(
        {"user_id": user_id, "end_time": None},
        {"$set": {"end_time": datetime.utcnow()}}
    )

def log_away_message(user_id: str, sender_id: int, sender_name: str, content: str):
    log = {
        "sender_id": sender_id,
        "sender_name": sender_name,
        "content": content,
        "timestamp": datetime.utcnow()
    }

    return away_collection.update_one(
        {"user_id": user_id},
        {"$push": {"messages": log}},
        upsert=True
    )

def get_away_logs(user_id: str):
    logs = away_collection.find({
        "user_id": user_id,
    })

    sessions = []
    for log in logs:
        session_messages = []
        for msg in log.get("messages", []):
            session_messages.append(f"{msg['sender_name']}: {msg['content']}")  # include sender
        sessions.append({
            "start_time": log["start_time"],
            "end_time": log["end_time"],
            "messages": session_messages
        })

    return sessions


def save_story_nft(user_id: str, result: dict):
    story_nft_collection.update_one(
        {"user_id": user_id},
        {"$push": {"story_nfts": result}},
        upsert=True
    )

def get_story_nfts(user_id: str):
    doc = story_nft_collection.find_one({"user_id": user_id}, {"_id": 0})
    return doc.get("story_nfts") if doc else None

def set_plan(user_id: str, plan: str, tx_hash: str, subscribed_at: datetime):
    valid_plans = ["Basic", "Premium", "Pro"]
    if plan not in valid_plans:
        raise ValueError(f"Invalid plan: {plan}. Must be one of {valid_plans}.")
    
    return collection.update_one(
        {"user_id": user_id},
        {"$set": {"plan": plan, "tx_hash": tx_hash, "subscribed_at": subscribed_at} },
        upsert=True
    )

def get_plan(user_id: str):
    doc = collection.find_one({"user_id": user_id})
    return doc.get("plan") if doc else None