from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Initialize FastAPI
app = FastAPI()

# Allow frontend access (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class ChatRequest(BaseModel):
    message: str

# Load models and data
embedder = SentenceTransformer('all-MiniLM-L6-v2')

with open('glossary_cleaned.json', 'r', encoding='utf-8') as f:
    glossary = json.load(f)

with open('plans_data_cleaned.jsonl', 'r', encoding='utf-8') as f:
    plans = [json.loads(line) for line in f]

with open('company_links_smart_filled.json', 'r', encoding='utf-8') as f:
    company_links = json.load(f)

# Embedding glossary
glossary_texts = [entry['question'] for entry in glossary]
glossary_embeddings = embedder.encode(glossary_texts, normalize_embeddings=True)
glossary_index = faiss.IndexFlatIP(glossary_embeddings.shape[1])
glossary_index.add(np.array(glossary_embeddings))

# Cache plan embeddings
plan_texts = [f"{plan['State']} {plan['Insurance Company']} {plan['Plan Name']}" for plan in plans]
plan_embeddings = embedder.encode(plan_texts, normalize_embeddings=True)
plan_index = faiss.IndexFlatIP(plan_embeddings.shape[1])
plan_index.add(np.array(plan_embeddings))

# Forbidden words
forbidden_words = ["Fuck", "Bitch", "Mad"]

# Helper Functions
def check_guardrails(user_input):
    for word in forbidden_words:
        if word in user_input.lower():
            return False
    return True

def is_greeting(user_input):
    greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "howdy"]
    user_text = user_input.lower()
    return any(greet in user_text for greet in greetings)

def detect_mode(user_input):
    glossary_keywords = [
        "what is", "explain", "define", "deductible", "co-pay", "coinsurance", "coverage",
        "benefits", "glossary", "out of pocket", "copayment", "eligibility", "exclusions"
    ]
    plan_keywords = [
        "plan", "premium", "suggest", "health plan", "insurance", "recommend", "buy", "purchase",
        "quote", "price", "rate", "cost", "policy", "state", "bronze", "silver", "gold", "platinum"
    ]
    user_text = user_input.lower()
    for word in glossary_keywords:
        if word in user_text:
            return "learn"
    for word in plan_keywords:
        if word in user_text:
            return "buy"
    return "unknown"

def find_best_glossary_answer(user_input):
    query_vec = embedder.encode([user_input], normalize_embeddings=True)
    D, I = glossary_index.search(np.array(query_vec), k=1)
    return glossary[I[0][0]]['answer']

def find_best_plan_recommendation(user_input):
    state_abbrev = { 
        "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO",
        "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
        "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA",
        "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
        "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
        "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
        "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD",
        "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
        "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
    }
    extra_mappings = {
        "newyork": "NY", "newjersey": "NJ", "northcarolina": "NC", "southcarolina": "SC",
        "newmexico": "NM", "newhampshire": "NH", "westvirginia": "WV",
        "northdakota": "ND", "southdakota": "SD", "rhodeisland": "RI", "washingtondc": "DC"
    }

    user_text = user_input.lower()
    selected_state = None
    for state_name, abbrev in state_abbrev.items():
        if state_name.lower() in user_text:
            selected_state = abbrev
            break
    if not selected_state:
        for key, abbrev in extra_mappings.items():
            if key in user_text.replace(" ", ""):
                selected_state = abbrev
                break
    if not selected_state:
        for abbrev in state_abbrev.values():
            if f" {abbrev.lower()} " in f" {user_text} ":
                selected_state = abbrev
                break

    if selected_state:
        filtered_plans = [plan for plan in plans if plan['State'].lower() == selected_state.lower()]
        filtered_plans = [plan for plan in filtered_plans if float(plan.get('Premium', 0)) > 0 and company_links.get(plan['Insurance Company'])]
        if not filtered_plans:
            return f"❗ Sorry, no valid plans found for {selected_state}."

        cheapest = sorted(filtered_plans, key=lambda x: float(x.get('Premium', 9999)))[:5]
        costliest = sorted(filtered_plans, key=lambda x: float(x.get('Premium', 0)), reverse=True)[:5]

        response_lines = [f"Here are some healthcare plans available in {selected_state}:"]

        response_lines.append("<br><br><b>Top 5 Best Plans (High Premium):</b>")
        for plan in costliest:
            company = plan['Insurance Company']
            url = company_links.get(company, "")
            response_lines.append(f"- **{plan['Tier']} plan**<br>Insurance Company: <a href='{url}' target='_blank'>{company}</a><br>Premium: ${plan['Premium']}<br>")

        response_lines.append("<br><b>Top 5 Cheapest Plans (Affordable):</b>")
        for plan in cheapest:
            company = plan['Insurance Company']
            url = company_links.get(company, "")
            response_lines.append(f"- **{plan['Tier']} plan**<br>Insurance Company: <a href='{url}' target='_blank'>{company}</a><br>Premium: ${plan['Premium']}<br>")

        return "<br>".join(response_lines)

    else:
        sorted_plans = sorted(
            [plan for plan in plans if float(plan.get('Premium', 0)) > 0 and company_links.get(plan['Insurance Company'])],
            key=lambda x: float(x.get('Premium', 9999))
        )[:3]
        response_lines = ["Here are some cheaper healthcare plans available across the United States:"]
        for plan in sorted_plans:
            company = plan['Insurance Company']
            url = company_links.get(company, "")
            response_lines.append(f"- **{plan['Tier']} plan**<br>Insurance Company: <a href='{url}' target='_blank'>{company}</a><br>State: {plan['State']}<br>Premium: ${plan['Premium']}<br>")

        return "<br>".join(response_lines)

# API Routes
@app.get("/")
def welcome():
    return {"message": "Health Insurance Assistant (United States)"}

@app.post("/chat")
async def chat(data: ChatRequest):
    user_input = data.message.strip()

    if not check_guardrails(user_input):
        return {"response": "⚠️ Sorry, inappropriate input."}

    if is_greeting(user_input):
        return {"response": "👋 Hello! Feel free to ask me anything about healthcare and insurance plans in the United States 🇺🇸."}

    mode = detect_mode(user_input)

    if mode == "learn":
        answer = find_best_glossary_answer(user_input)
    elif mode == "buy":
        answer = find_best_plan_recommendation(user_input)
    else:
        answer = "❗ Sorry, I can only assist with healthcare insurance and glossary information related to the United States."

    return {"response": answer}
