from langchain_groq import ChatGroq
from src.agents.memory import MemoryManager
from langchain_huggingface import HuggingFaceEmbeddings
from src.database.mongo_manager import (
    get_user_profile,
    save_user_profile,
    set_mode_mongo,
)

class PersonaAgent:
    def __init__(self, api_key, user_profile,user_id):
        self.llm = ChatGroq(groq_api_key=api_key, model="llama-3.1-8b-instant",streaming=True)  
        self.mode = "professional"
        self.memory = MemoryManager()
        self.user_id = user_id
        self.user_profile = user_profile
        self.embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        stored_profile = get_user_profile(self.user_id)
        if stored_profile:
            self.user_profile = stored_profile
            self.mode = stored_profile.get("mode", "professional")
        else:
            self.mode = "professional"
            self.user_profile["mode"] = self.mode
            save_user_profile(self.user_id, self.user_profile,"user")

    def switch_mode(self, new_mode):
        """Switches between 'professional' and 'fun' modes and saves it persistently."""
        if new_mode in ["professional", "fun"]:
            self.mode = new_mode
            self.user_profile["mode"] = new_mode  
            set_mode_mongo(self.user_id, new_mode)
            return f"Mode switched to {new_mode.capitalize()} Mode 🎭"
        return "Invalid mode! Choose 'professional' or 'fun'."

    async def generate_response(self, user_input):
        """Generate AI response based on the current mode and user details."""
        stored_profile = get_user_profile(self.user_id)
        if stored_profile:
            self.user_profile = stored_profile
            self.mode = stored_profile.get("mode", "professional") 

        past_conversations = self.memory.get_recent_conversations(self.user_id,user_input,10)

        if "discord" in user_input.lower():
            past_context = "\n".join([f"User: {u}\nAI: {r}" for u, r, t in past_conversations if t == "discord"])
        else:
            past_context = "\n".join([f"User: {u}\nAI: {r}" for u, r, t in past_conversations if t == "general"])

        system_prompt = self._get_system_prompt(past_context)

        full_response = ""
        async for chunk in self._call_ai_stream(system_prompt, user_input):
            full_response += chunk
            yield chunk

        
        self.memory.save_conversation(self.user_id, user_input, full_response)
        
        return 
    
    async def _call_ai_stream(self, system_prompt, user_input):
        full_prompt = f"{system_prompt}\nUser: {user_input}\nAI: "
        async for chunk in self.llm.astream(full_prompt):
            yield chunk.content if hasattr(chunk, "content") else str(chunk)


    def _get_system_prompt(self, past_context):
        """Builds a rich system prompt with detailed user context."""
        user_name = self.user_profile.get("name", "Unknown User")
        job_title = self.user_profile.get("professional", {}).get("job_title", "Not Specified")
        company = self.user_profile.get("professional", {}).get("company", "Unknown Company")
        skills = ", ".join(self.user_profile.get("professional", {}).get("skills", ["Not Specified"]))
        experience = self.user_profile.get("professional", {}).get("experience", "Not Specified")
        interests = ", ".join(self.user_profile.get("interests", ["Not Specified"]))
        away = self.user_profile.get("away", False)

        if self.mode == "fun":
            mode_prompt = (
                "Your tone should be playful and engaging. Use casual phrases, jokes, and emojis when appropriate. "
                "Avoid mentioning the user's company, job title, or professional skills."
            )
        else:
            mode_prompt = (
                "Maintain a professional and concise tone. Use clear and formal language. Avoid casual expressions."
            )

        away_behavior = (
            "The user is currently **away**. Respond on their behalf as a helpful assistant who can represent their voice and preferences."
            if away else
            "The user is **present**. Act as their second brain—supportive, context-aware,learn about him/her and insightful."
        )


        return f"""
        You are an AI assistant. Your response style must follow the selected mode.
        {away_behavior}

        ---
        **User Profile**:
        - **Name**: {user_name}
        - **Job Title**: {job_title}
        - **Company**: {company}
        - **Skills**: {skills}
        - **Experience**: {experience} years
        - **Interests**: {interests}

        **Mode**: {'Fun 🕺' if self.mode == 'fun' else 'Professional 💼'}
        ---

        **Conversation History**:
        {past_context}

        **Mode-Specific Instructions**:
        {mode_prompt}

        Now, generate a relevant and thoughtful response to the user's input and Do not use any Markdown formatting like **bold** or *italic* in your response.
        """
    
    def draft_email(self, prompt):
        """Drafts an email based on the user's professional persona."""
        # get the profile name
        stored_profile = get_user_profile(self.user_id)
        name = stored_profile.get("name", "The User") if stored_profile else "The User"

        system_prompt = f"""
        You are an AI assistant. Your task is to draft a professional email.
        The context of the email is: {prompt}
        You should **only** generate the email body content without any other headers like the recipient's name, subject, or other metadata.
        The email should be written in a formal tone, considering the context, and signed off with the user's name.
        The user's name is: {name}.
        The body should be clear and concise with no extra content such as headers or the subject line.
        """
        
        response = self._call_ai(system_prompt, prompt)
        
        return response

    def _call_ai(self, system_prompt, user_input):
        """Calls AI model to generate response based on prompt."""
        response = self.llm.invoke(f"{system_prompt}\nUser: {user_input}\nAI: ")
        
        return response.content.strip() if hasattr(response, "content") else str(response).strip()

    def generate_mimic_response(self, message: str,type: str = "general"):
        """Generate a mimic-style response while the user is away."""
        stored_profile = get_user_profile(self.user_id)
        if stored_profile:
            self.user_profile = stored_profile
            self.mode = stored_profile.get("mode", "professional")

        past_conversations = self.memory.get_recent_conversations(self.user_id, message, 5)
        past_context = "\n".join([f"User: {u}\nAI: {r}" for u, r,_ in past_conversations]) if past_conversations else "No prior interactions."

        user_name = self.user_profile.get("name", "The User")

        if self.mode == "fun":
            mode_prompt = "Make it playful, use emojis(little bit), and sound casual like a friend. Keep it light, make the user feel welcomed."
        else:
            mode_prompt = "Maintain a courteous, polite, and professional tone. Avoid jokes or slang."
        
        job_title = self.user_profile.get("professional", {}).get("job_title", "Not Specified")
        skills = ", ".join(self.user_profile.get("professional", {}).get("skills", ["Not Specified"]))

        system_prompt = f"""
        You are impersonating the user's assistant (MimicBot). 
        Your job is to respond to messages as their stand-in when they’re away.

        Additional context:
        - **Mode**: {self.mode}
        - **User ID**: {self.user_id}
        - **User Name**: {user_name}
        - **Job Title**: {job_title}
        - **Skills**: {skills}
        
        Conversation History:
        {past_context}

        Instructions:
        - Respond naturally on behalf of the ${user_name.upper()}.
        - {mode_prompt}
        """

        response = self._call_ai(system_prompt, message)

        self.memory.save_conversation(self.user_id, message, response,type)

        return response

    def summarize_conversation(self, sessions: list):
        """Summarizes away-time conversations for the user."""
        summaries = []

        for session in sessions:
            start_time = session.get("start_time", "Unknown")
            end_time = session.get("end_time", "Unknown")
            messages = session.get("messages", [])

            if not messages:
                summaries.append({
                    "start_time": start_time,
                    "end_time": end_time,
                    "summary": "No messages during this session."
                })
                continue

            formatted_messages = "\n".join(messages)

            system_prompt = f"""
            You are a helpful assistant summarizing away-time messages for the user.
            The following are messages sent to the user between {start_time} and {end_time}:

            ---
            {formatted_messages}
            ---

            Your task:
            Summarize the main points and intentions in 2-4 sentences. Be clear and concise.
            """

            summary = self._call_ai(system_prompt, "Please summarize the above messages.")
            summaries.append({
                "start_time": start_time,
                "end_time": end_time,
                "summary": summary
            })

        return summaries