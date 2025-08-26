from fastapi import FastAPI
from pydantic import BaseModel
from flow.agent_flow_controller import GoldInvestmentSession, gold_investment_api, gold_purchase_node
from database.supabase_client import SupabaseDB  # <-- ADD THIS

app = FastAPI(title="Gold Investment AI Agent")
db = SupabaseDB()  # <-- ADD THIS

sessions = {}

class ChatRequest(BaseModel):
    user_id: str
    message: str

@app.post("/agent")
def agent_chat(request: ChatRequest):
    session = sessions.get(request.user_id)
    if not session:
        session = GoldInvestmentSession(user_name=request.user_id)
        sessions[request.user_id] = session
    if session.state == "investment":
        result = gold_investment_api(request.message, session.user_name, chat_history=session.chat_history)
        session.chat_history.append({"role": "user", "content": request.message})
        session.chat_history.append({"role": "assistant", "content": result["message"]})
        if result.get("purchase_triggered"):
            session.state = "purchase"
            session.pending_purchase = None
        return {
            "reply": result["message"],
            "state": session.state
        }
    elif session.state == "purchase":
        node_result = gold_purchase_node(
            user_message=request.message,
            user_name=session.user_name,
            chat_history=session.chat_history,
            pending_purchase=session.pending_purchase,
        )
        session.chat_history.append({"role": "user", "content": request.message})
        session.chat_history.append({"role": "assistant", "content": node_result["message"]})
        if not node_result["success"] and node_result.get("pending_purchase"):
            session.pending_purchase = node_result["pending_purchase"]
        elif node_result["success"]:
            session.state = "investment"
            session.pending_purchase = None
        return {
            "reply": node_result["message"],
            "state": session.state
        }

@app.post("/investment-chat")
def investment_only(request: ChatRequest):
    result = gold_investment_api(request.message, request.user_id, chat_history=[])
    return {"reply": result["message"]}

@app.post("/purchase")
def direct_purchase(request: ChatRequest):
    node_result = gold_purchase_node(
        user_message=request.message,
        user_name=request.user_id,
        chat_history=[],
        pending_purchase=None
    )
    return {"reply": node_result["message"]}

@app.get("/")
def root():
    return {"message": "Gold Investment Agent multi-API is running!"}

@app.get("/transactions")
def get_transactions():
    """
    Returns all gold purchases from the database as JSON.
    """
    try:
        transactions = db.get_all_purchases()
        return {"transactions": transactions}
    except Exception as e:
        return {"error": str(e), "transactions": []}
