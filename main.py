from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel 
from datetime import datetime

app = FastAPI()

class ProposalRequest(BaseModel):
      client_name: str 
      service_type: str 
      amount_cad: float

@app.post("/api/generate-proposal") 
async def generate_proposal(data: ProposalRequest):
      try: 
            subtotal = data.amount_cad 
            tax = round(subtotal * 0.13, 2)  # 13% Tax 
            total = round(subtotal + tax, 2)
            proposal_text = (
                  f"Hello {data.client_name},\n\n"
              f"Thank you for reaching out! Here is the estimate for the requested service:\n\n"
              f"• Service: {data.service_type}\n"
              f"• Subtotal: ${subtotal:,.2f} CAD\n"
              f"• Tax (13% HST/GST): ${tax:,.2f} CAD\n"
              f"• Total Amount: ${total:,.2f} CAD\n\n"
              f"Please let us know if you have any questions or if you would like to proceed.\n\n"
              f"Best regards,\n"
              f"QuoteGen Canada Team"
            )

            return {"proposal_text": proposal_text}
      except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
app.mount("/", StaticFiles(directory=".", html=True), name="static")
@app.get("/")
async def read_index(): 
      return FileResponse("index.html")
