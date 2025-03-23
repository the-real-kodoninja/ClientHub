# backend/api/payments.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from ..main import get_db
from ..api.auth import get_current_user
from ..models.user import User
import stripe
from pydantic import BaseModel

app = FastAPI()

stripe.api_key = "your-stripe-secret-key"  # Replace with your Stripe key

class PaymentIntent(BaseModel):
    amount: int  # In cents
    currency: str = "usd"

@app.post("/payments/stripe/intent")
async def create_payment_intent(
    payment: PaymentIntent,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        intent = stripe.PaymentIntent.create(
            amount=payment.amount,
            currency=payment.currency,
            metadata={"user_id": user.id}
        )
        return {"client_secret": intent.client_secret}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# MetaMask integration (client-side, backend verifies)
@app.post("/payments/metamask/verify")
async def verify_metamask_payment(
    tx_hash: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Placeholder: Verify tx_hash via Web3.py or Infura (requires additional setup)
    # For now, assume success
    return {"status": "Verified", "tx_hash": tx_hash}