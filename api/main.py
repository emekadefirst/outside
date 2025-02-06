import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from user.route import auth
from ticket.route import ticket
from payment.route import payment

app = FastAPI(
    title="Outside API",
    description="The official API for outside application",
    version="0.0.1",
)

app.include_router(auth, prefix="/api/v1", tags=["User"])
app.include_router(ticket, prefix="/api/v1", tags=["Ticket"])
app.include_router(payment, prefix="/api/v1", tags=["Payment"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def main():
    return {"message": "Welcome to the FastAPI API!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
