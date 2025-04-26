import time
import uuid
import json

from pinecone import Pinecone,ServerlessSpec
from langchain_huggingface import HuggingFaceEmbeddings

import os
from dotenv import load_dotenv
load_dotenv(override=True)

class MemoryManager:
    def __init__(self):
        self.pc = Pinecone(api_key=os.getenv("PINECONE_KEY")) 
        self.index_name = "proxy-persona-memory"
        self.embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        existing_indexes = [idx["name"] for idx in self.pc.list_indexes()]
        if self.index_name not in existing_indexes:
            self.pc.create_index(
                name=self.index_name,
                dimension=384,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )

        self.index = self.pc.Index(self.index_name)
    

    def save_user_profile(self,user_id, user_profile):
         """Stores user profile details in memory."""
         embedding = self.embedding_model.embed_query(json.dumps(user_profile))  
         vector_id = f"profile-{user_id}"

         self.index.upsert([
                (vector_id, embedding, {"user_id": user_id, "profile_data": json.dumps(user_profile), "timestamp": time.time()})
            ])

    def get_user_profile(self, user_id):
        """Retrieves structured user profile from Pinecone."""
        vector_id = f"profile-{user_id}"
        results = self.index.fetch([vector_id])
        if results.vectors and vector_id in results.vectors:
            profile_data = results.vectors[vector_id].metadata.get("profile_data")
            return json.loads(profile_data) if profile_data else None
        return None

    def save_conversation(self,user_id, user_input, ai_response,type = "general"):
        """Stores past conversation for memory consistency."""
        embedding = self.embedding_model.embed_query(user_input)  
        vector_id = str(uuid.uuid4())  

        self.index.upsert([
            (
                vector_id,
                embedding,
                {
                    "user_id": user_id,  
                    "user_input": user_input,
                    "response": ai_response,
                    "type": type,
                    "timestamp": time.time()
                }
            )
        ]) 

    def get_recent_conversations(self,user_id, user_input, limit=10):
        """Retrieves past stored messages for better context awareness."""
        index_stats = self.index.describe_index_stats()
        if index_stats["namespaces"].get("", {}).get("vector_count", 0) == 0:
            return []

        query_vector = self.embedding_model.embed_query(user_input)

        results = self.index.query(vector=query_vector, top_k=limit, include_metadata=True)

        past_messages = [
            (
                r["metadata"].get("user_input", ""), 
                r["metadata"].get("response", ""),   
                r["metadata"].get("type", "")        
            )
            for r in results["matches"]
            if r["metadata"].get("user_id") == user_id  
        ]

        past_messages.sort(key=lambda x: x[1], reverse=True)
    
        return past_messages