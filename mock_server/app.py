from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import sqlite3
import uvicorn

app = FastAPI(title="CrashedQA Mock Fintech API")

# Setup an in-memory database for the demo
conn = sqlite3.connect(":memory:", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE users (id TEXT, name TEXT, balance REAL)")
cursor.execute("INSERT INTO users VALUES ('user_123', 'John Doe', 1000.0)")
cursor.execute("INSERT INTO users VALUES ('user_456', 'Jane Smith', 2500.0)")
conn.commit()

class CheckoutRequest(BaseModel):
    user_id: str
    amount: float

@app.get("/")
async def root():
    return {"status": "online", "service": "CrashedQA Mock API"}

@app.post("/checkout")
async def checkout(request: CheckoutRequest):
    """
    Intentionally vulnerable to SQL injection via the user_id parameter.
    """
    user_id = request.user_id
    
    # VULNERABILITY: String interpolation in SQL query
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    
    try:
        cursor.execute(query)
        user = cursor.fetchone()
        
        if not user:
            # If the SQLi payload causes a syntax error or returns no results, we might get an error here
            raise HTTPException(status_code=404, detail="User not found")
            
        return {
            "message": "Checkout successful",
            "user": {
                "id": user[0],
                "name": user[1],
                "balance": user[2]
            },
            "remaining_balance": user[2] - request.amount
        }
    except sqlite3.Error as e:
        # In a real app, you shouldn't return the full stack trace/error, 
        # but for the demo, we want to show the agent can detect this.
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}. Query was: {query}")

@app.post("/refund")
async def refund(user_id: str, amount: float):
    # Mock refund endpoint
    return {"message": "Refund processed", "user_id": user_id, "amount": amount}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
