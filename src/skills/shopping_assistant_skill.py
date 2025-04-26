from groq import Groq
import os
import serpapi

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
serpapi_client = serpapi.Client(api_key=os.getenv("SERPAPI_API_KEY"))

def search_products(query: str) -> list:
    results = serpapi_client.search({
        "engine": "google",
        "q": query,
    })

    products = results.get("organic_results", [])

    formatted = []

    for p in products[:8]:  
        formatted.append({
            "id": p.get("product_id") or p.get("position"),
            "name": p.get("title"),
            "price": p.get("price"),
            "image": p.get("thumbnail"),
            "buy_link": p.get("link")
        })

    return formatted

def generate_shopping_reply(user_prompt: str) -> str:
    system_prompt = "Extract a clean product search query from this user's shopping request.Use the most relevant keywords and phrases to form a concise search query.The user may have provided a lot of context, but focus on the main product they are looking for and give the result in one sentence for example user serach query is 'I want to buy a new laptop for gaming' then the output should be 'gaming laptop'." 
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        model="llama-3.3-70b-versatile"
    )
    return chat_completion.choices[0].message.content.strip()

def handle_shopping_flow(prompt: str) -> dict:
    print("[🧠] Understanding intent...")
    search_query = generate_shopping_reply(prompt)

    print(search_query)
    print(f"[🔍] Searching for products: {search_query}")
    products = search_products(search_query)

    if not products:
        return {"error": "No products found. Try rephrasing."}

    return {
        "products": products,
    }