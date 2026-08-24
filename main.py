from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
import database
app = FastAPI(title="Canada QuoteAI SaaS")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
allow_methods=["*"], allow_headers=["*"])
def get_db():
db = database.SessionLocal()
try: yield db
finally: db.close()
class ProposalRequest(BaseModel):
client_name: str
service_type: str
amount_cad: float @app.get("/")
def read_root(): return FileResponse("index.html")
@app.post("/api/generate-proposal")
def generate(req: ProposalRequest, db: Session = Depends(get_db)):
if not req.client_name or not req.service_type or req.amount_cad <= 0:
raise HTTPException(status_code=400, detail="Invalid input")
tax_hst = req.amount_cad * 0.13 # Ontario HST 13%
total = req.amount_cad + tax_hst
text = (f"Hi {req.client_name},
Thank you for reaching out! Here is your estimate for: {req.service_type}.
"
"
f"• Subtotal: ${req.amount_cad:,.2f} CAD
• HST (13%): ${tax_hst:,.2f} CAD
• Total: ${total:,.2f} CAD
f"Scope includes standard execution & 30-day guarantee.")
item = database.Proposal(client_name=req.client_name, service_type=req.service_type,
amount_cad=req.amount_cad, generated_proposal=text)
db.add(item); db.commit()
return {"status": "success", "result": text}