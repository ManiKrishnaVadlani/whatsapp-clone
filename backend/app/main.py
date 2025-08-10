from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow your frontend to talk to the backend without CORS errors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                  "https://whatsapp-clone-liard-three.vercel.app",],  # Can be restricted to ["http://localhost:5173"] later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📌 This returns the chat list for the sidebar
@app.get("/conversations")
def get_conversations():
    return [
        {
            "_id": "919937320320",
            "name": "Ravi Kumar",
            "last_message": "Hi Ravi! Sure, I’d be happy to help you with that. Could you tell me what you're looking for?",
        },
        {
            "_id": "929967673280",
            "name": "Neha Joshi",
            "last_message": "Hi Neha! Absolutely. We offer curated home decor pieces...",
        },
    ]

# 📌 This returns messages for a specific conversation
@app.get("/conversations/{conv_id}")
def get_messages(conv_id: str):
    if conv_id == "919937320320":  # Messages for Ravi Kumar
        return [
            {"from_me": False, "text": "Hi, I’d like to know more about your services."},
            {"from_me": True, "text": "Sure, could you tell me what you're looking for?"},
        ]
    elif conv_id == "929967673280":  # Messages for Neha Joshi
        return [
            {"from_me": False, "text": "Do you have wall art options?"},
            {"from_me": True, "text": "Yes, we have a great collection of wall art."},
        ]
    return []  # If no matching ID found, return empty
