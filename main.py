from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from crew import IncrementumCrew
import os
from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr
from tools.email_sender import send_outreach_email

load_dotenv()

app = FastAPI(title="IncrementumAI - Agent Workplace")

# Kreiraj crew instancu
crew = IncrementumCrew()

# Request models
class ExpansionRequest(BaseModel):
    market: str
    industry: str

class OutreachRequest(BaseModel):
    target_persona: str
    market: str
    context: str = ""

class LeadRequest(BaseModel):
    lead_info: str

class ContentRequest(BaseModel):
    content_type: str
    topic: str
    market: str
class EmailRequest(BaseModel):
    to_email: EmailStr
    subject: str
    body: str

@app.post("/api/send-email")
async def send_email(request: EmailRequest):
    """
    Send drafted outreach email
    """
    try:
        result = send_outreach_email(
            to_email=request.to_email,
            subject=request.subject,
            body=request.body
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# API Endpoints
@app.post("/api/expansion-plan")
async def create_expansion_plan(request: ExpansionRequest):
    """
    Koordinirani multi-agent workflow za expansion plan
    """
    try:
        result = crew.create_expansion_plan(
            market=request.market,
            industry=request.industry
        )
        return {"success": True, "result": str(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/draft-outreach")
async def draft_outreach(request: OutreachRequest):
    """
    Outreach specialist kreira personalized message
    """
    try:
        result = crew.draft_outreach(
            target_persona=request.target_persona,
            market=request.market,
            context=request.context
        )
        return {"success": True, "result": str(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/qualify-lead")
async def qualify_lead(request: LeadRequest):
    """
    Lead Qualifier evaluira lead
    """
    try:
        result = crew.qualify_lead(lead_info=request.lead_info)
        return {"success": True, "result": str(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/create-content")
async def create_content(request: ContentRequest):
    """
    Content Creator kreira marketing materijale
    """
    try:
        result = crew.create_content(
            content_type=request.content_type,
            topic=request.topic,
            market=request.market
        )
        return {"success": True, "result": str(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/agents")
async def list_agents():
    """
    Lista svih dostupnih agenata
    """
    return {
        "agents": [
            {"id": "strategy", "name": "Strategy Coordinator", "description": "Orchestrates multi-agent workflows"},
            {"id": "research", "name": "Market Researcher", "description": "Analyzes markets and competitors"},
            {"id": "outreach", "name": "Outreach Specialist", "description": "Crafts personalized communications"},
            {"id": "content", "name": "Content Creator", "description": "Creates marketing materials"},
            {"id": "qualifier", "name": "Lead Qualifier", "description": "Evaluates and scores leads"}
        ]
    }

# Serve static files (HTML/CSS/JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Serve main web interface
    """
    with open("static/index.html", "r") as f:
        return f.read()

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 3000))
    uvicorn.run(app, host="0.0.0.0", port=port)