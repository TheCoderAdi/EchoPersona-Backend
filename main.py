from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from src.agents.persona_agent import PersonaAgent
from src.agents.memory import MemoryManager
from src.bot.manager import BotManager
from src.database.mongo_manager import(
    get_user_auth,
    save_user_profile,get_user_profile,
    update_user_field,
    set_away_mongo,set_mode_mongo,
    set_chat,get_chat,
    increment_email_count, increment_switch_count, increment_command_count,
    get_analytics,
    get_story_nfts,
    set_plan, get_plan,
    get_away_logs
)
from src.auth.jwt_handler import (
    get_password_hash, verify_password,
    create_access_token, decode_token,
    oauth2_scheme
)
from src.skills import maze_game_skill

from src.mint.story_nft_skill import handle_story_and_mint
from src.skills.shopping_assistant_skill import handle_shopping_flow
from fastapi import WebSocket, WebSocketDisconnect

import os
import asyncio
from dotenv import load_dotenv
from datetime import datetime
from typing import List, Dict

load_dotenv(override=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGIN"),
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

memory_manager = MemoryManager()
bot_manager = BotManager()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class ProfileSetupRequest(BaseModel):
    profile_data: dict

class ProfileUpdateRequest(BaseModel):
    user_id: str
    updates: dict

class ModeSwitchRequest(BaseModel):
    user_id: str
    mode: str

class ChatMimicRequest(BaseModel):
    user_id: str
    user_input: str

class DraftEmailRequest(BaseModel):
    user_id: str
    recipient: str
    subject: str
    context: str

class SetAwayRequest(BaseModel):
    user_id: str
    away: bool

class ReceiveMessageRequest(BaseModel):
    user_id: str
    message: str

class InitBotPayload(BaseModel):
    user_id: str
    bot_token: str

class AuthRequest(BaseModel):
    user_id: str
    password: str

class MintRequest(BaseModel):
    user_id: str
    prompt: str
    wallet: str

class ShoppingRequest(BaseModel):
    user_id: str
    prompt: str

class SubscriptionRequest(BaseModel):
    user_id: str
    plan: str  
    tx_hash: str

class SummerizeRequest(BaseModel):
    user_id: str

class SessionMessage(BaseModel):
    start_time: str
    end_time: str
    messages: List[str] 

class SummarizeRequest(BaseModel):
    user_id: str
    sessions: List[SessionMessage]

class PathRequest(BaseModel):
    path: List[str]
    user_id: str

class GuessRequest(BaseModel):
    duel_id: int
    path: List[str]

active_connections: Dict[int, list[WebSocket]] = {}

@app.websocket("/api/duel/ws/{duel_id}")
async def websocket_endpoint(websocket: WebSocket, duel_id: int):
    await websocket.accept()
    if duel_id not in active_connections:
        active_connections[duel_id] = []
    active_connections[duel_id].append(websocket)

    print(f"WebSocket connection established for duel {duel_id}. Total connections: {len(active_connections[duel_id])}")
    try:
        while True:
            await websocket.receive_text() 
    except WebSocketDisconnect:
        active_connections[duel_id].remove(websocket)

async def broadcast_winner(duel_id: int, winner: str):
    if duel_id in active_connections:
        for ws in active_connections[duel_id]:
            try:
                await ws.send_json({"winner": winner})
            except Exception:
                active_connections[duel_id].remove(ws)


@app.post("/register")
def register(req: AuthRequest):
    if get_user_auth(req.user_id):
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_pw = get_password_hash(req.password)
    save_user_profile(req.user_id, hashed_pw, "register")
    return {"message": "User registered successfully"}

@app.get("/analytics/{user_id}")
def get_user_analytics(user_id: str):
    try:
        data = get_analytics(user_id)

        analytics = data.get("analytics", {})
        plan = data.get("plan", "")

        return {
            "data": [
                {"name": "Chats", "count": analytics.get("commands", 0)},
                {"name": "Emails", "count": analytics.get("emails", 0)},
                {"name": "Switches", "count": analytics.get("switches", 0)},
            ],
            "plan" : plan
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/login")
def login(req: AuthRequest):
    password = get_user_auth(req.user_id)
    if not password or not verify_password(req.password, password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": req.user_id})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/current-user")
def current_user(token: str = Depends(oauth2_scheme)):
    user_id = decode_token(token)
    return {"user_id": user_id}

@app.post("/setup-profile")
def setup_profile(request: ProfileSetupRequest, token: str = Depends(oauth2_scheme)):
    """Stores user profile in memory."""
    user_id = decode_token(token)

    if not request.profile_data:
        raise HTTPException(status_code=400, detail="User ID and profile data are required.")
    
    save_user_profile(user_id, request.profile_data,"profile")
    memory_manager.save_user_profile(user_id, request.profile_data)
    return {"message": "Profile setup successful."}

@app.get("/get-profile/{user_id}")
def get_profile(user_id: str):
    """Retrieves user profile from memory."""
    profile = get_user_profile(user_id)
    if profile:
        return profile
    raise HTTPException(status_code=404, detail="Profile not found")

@app.put("/update-profile")
def update_profile(request: ProfileUpdateRequest):
    """Updates a specific user profile field."""
    profile = get_profile(request.user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    profile.update(request.updates)
    memory_manager.save_user_profile(request.user_id, profile)
    update_user_field(request.user_id, request.updates)
    return {"message": f"Updated Profile Successfully"}

@app.post("/switch-mode")
def switch_mode(request: ModeSwitchRequest):
    """Switches between 'professional' and 'fun' mode."""
    profile = get_user_profile(request.user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    if request.mode not in ["professional", "fun"]:
        raise HTTPException(status_code=400, detail="Invalid mode. Choose 'professional' or 'fun'.")
    
    set_mode_mongo(request.user_id, request.mode)

    increment_switch_count(request.user_id)

    return {"message": f"Mode switched to {request.mode.capitalize()} Mode 🎭"}

@app.post("/chat-with-mimic")
def chat_with_mimic(request: ChatMimicRequest):
    user_profile = get_user_profile(request.user_id)
    if not user_profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    plan = user_profile.get("plan", "Basic")
    chat_count = user_profile.get("chat_count", 0)

    if plan == "Basic" and chat_count >= 100:
        raise HTTPException(status_code=403, detail="You have reached your chat limit for the Basic plan.")

    if plan == "Premium" and chat_count >= 500:
        raise HTTPException(status_code=403, detail="You have reached your chat limit for the Premium plan.")

    agent = PersonaAgent(api_key=GROQ_API_KEY, user_profile=user_profile,user_id=request.user_id)
    async def streamer():
        response_text = ""
        async for chunk in agent.generate_response(request.user_input):
            response_text += chunk
            yield chunk.encode("utf-8")  

        set_chat(request.user_id, request.user_input, response_text)
        increment_command_count(request.user_id)

    return StreamingResponse(streamer(), media_type="text/plain")

@app.get("/get-chat/{user_id}")
def get_chats(user_id: str):
    """Retrieves the last chat with the user."""
    chat = get_chat(user_id)
    if not chat:
        raise HTTPException(status_code=404, detail="No chat found")
    
    return chat

@app.post("/draft-email")
def draft_email(request: DraftEmailRequest):
    """Generates a draft email based on the user's persona."""
    user_id = request.user_id

    user_profile = get_user_profile(user_id)
    plan = user_profile.get("plan", "Basic")
    email_count = user_profile.get("email_count", 0)

    if plan == "Basic" and email_count >= 10:
        raise HTTPException(status_code=403, detail="You have reached your email limit for the Basic plan.")

    if plan == "Premium" and email_count >= 100:
        raise HTTPException(status_code=403, detail="You have reached your email limit for the Premium plan.")

    if not user_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    agent = PersonaAgent(api_key=GROQ_API_KEY, user_profile=user_profile,user_id=user_id)

    prompt = f"""
    Draft a professional email to {request.recipient} with the subject '{request.subject}'. 
    The context of the email is: {request.context}.
    Keep the tone consistent with the user's professional persona.
    """
    draft = agent.draft_email(prompt)

    increment_email_count(user_id)

    return {
        "user_id": user_id,
        "recipient": request.recipient,
        "subject": request.subject,
        "draft": draft
    }

@app.post("/set-away")
def set_away(request: SetAwayRequest):
    """Sets the user's status to away or available."""
    user_profile = get_user_profile(request.user_id)
    if not user_profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    set_away_mongo(request.user_id, request.away)

    increment_switch_count(request.user_id)

    if not request.away:
        bot_manager.stop_bot(request.user_id)

    return {"message": f"User status set to {'away' if request.away else 'available'}."}

@app.post("/receive-message")
def receive_message(request: ReceiveMessageRequest):
    """Processes a message only if the user is set to away mode with a mimicked response style."""
    user_id = request.user_id

    user_profile = get_user_profile(user_id)
    if not user_profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    agent = PersonaAgent(api_key=GROQ_API_KEY, user_profile=user_profile,user_id=user_id)

    if not agent.user_profile.get("away", False):
        print("User is not in away mode.")
        raise HTTPException(status_code=403, detail="User is not in away mode.")

    auto_reply = agent.generate_mimic_response(request.message,type="discord")

    return {
        "user_id": user_id,
        "message": request.message,
        "auto_reply": auto_reply,
        "status": "Reply sent"
    }

@app.post("/initialize-bot")
def initialize_bot(request: InitBotPayload):
    result = bot_manager.initialize_bot(request.user_id, request.bot_token)
    return {"message": result}

@app.post("/stop-bot")
def stop_bot(request: InitBotPayload):
    result = bot_manager.stop_bot(request.user_id)
    return {"message": result}

@app.get("/bot-status/{user_id}")
def bot_status(user_id: str):
    """Checks if the bot is running for the user."""
    status = bot_manager.is_bot_running(user_id)
    return {"user_id": user_id, "bot_running": status}

@app.post("/story/mint")
def mint_story(request:MintRequest):
    try:
        result = handle_story_and_mint(request.user_id,request.prompt, request.wallet)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/shooping")
def shopping_assistant(req: ShoppingRequest):
    try:
        plan = get_plan(req.user_id)
        if not plan:
            raise HTTPException(status_code=404, detail="Profile or plan not found")
        if plan == "Basic":
            raise HTTPException(status_code=403, detail="Basic plan does not support shopping assistant.")
        result = handle_shopping_flow(req.prompt)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/story/nfts/{user_id}")
def get_story_nft(user_id: str):
    try:
        nfts = get_story_nfts(user_id)
        return {"status": "success", "data": nfts}
    except Exception as e:
        return {"status": "error", "message": str(e)}   

@app.post("/subscribe")
def buy_plan(request: SubscriptionRequest):
    user_id = request.user_id
    selected_plan = request.plan

    valid_plans = ["Basic", "Premium", "Pro"]
    if selected_plan not in valid_plans:
        raise HTTPException(status_code=400, detail=f"Invalid plan: {selected_plan}. Choose from {valid_plans}.")

    profile = get_user_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")    
    
    set_plan(user_id, selected_plan, tx_hash=request.tx_hash, subscribed_at=datetime.utcnow())

    return {"message": f"Subscription plan successfully updated to {selected_plan}."}

@app.get("/get-plan/{user_id}")
def get_plan_route(user_id: str):
    """Retrieves the user's current subscription plan."""
    plan = get_plan(user_id)

    if not plan:
        raise HTTPException(status_code=404, detail="Profile or plan not found")

    return {"user_id": user_id, "plan": plan}

@app.get("/away-messages/{user_id}")
def get_away_messages(user_id: str):
    """Retrieves the away messages for all users."""
    away_messages = get_away_logs(user_id)
    return {"away_messages": away_messages}


@app.post("/away-summary")
def summarize_away_sessions(data: SummarizeRequest):
    """
    Returns summarized away messages for the given user.
    """
    user_id = data.user_id
    sessions = [session.dict() for session in data.sessions]

    plan = get_plan(user_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Profile or plan not found")

    if plan == "Basic":
        raise HTTPException(status_code=403, detail="Basic plan does not support away message summarization.")

    user_profile = get_user_profile(user_id)

    agent = PersonaAgent(api_key=GROQ_API_KEY, user_profile=user_profile, user_id=user_id)
    summaries = agent.summarize_conversation(sessions)

    return {
        "original_sessions": sessions,
        "summaries": summaries
    }

@app.post("/api/duel/create")
def create_duel(req: PathRequest):
    try:
        plan = get_plan(req.user_id)
        if plan == "Basic":
            raise HTTPException(status_code=403, detail="Basic plan does not support duel creation.")
        duel_id = maze_game_skill.create_duel(req.path)
        return {"duel_id": duel_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/duel/submit")
def submit_guess(req: GuessRequest):
    try:
        tx_hash = maze_game_skill.submit_guess(req.duel_id, req.path)
        return {"tx_hash": tx_hash}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/duel/reveal")
async def reveal_maze(req: GuessRequest):
    try:
        tx_hash = maze_game_skill.reveal_maze(req.duel_id, req.path)
        winner =  maze_game_skill.get_winner(req.duel_id)
        if winner:
            await broadcast_winner(req.duel_id, winner)
        return {"tx_hash": tx_hash}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/duel/winner/{duel_id}")
async def get_duel_winner(duel_id: int):
    """Fetches the winner of a duel by duel ID."""
    try:
        winner = maze_game_skill.get_winner(duel_id)
        
        if winner is None:
            raise HTTPException(status_code=404, detail=f"No winner found for duel {duel_id}")
        
        await broadcast_winner(duel_id, winner)
        return {"winner": winner}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.on_event("startup")
async def start_bot_watchdog():
    asyncio.create_task(bot_manager.monitor_bots())