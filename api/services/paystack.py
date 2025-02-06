import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()

secret_key = os.getenv("PAYSTACK_KEY")


async def initialize_transaction(email, amount):
    url = "https://api.paystack.co/transaction/initialize"
    data = {"email": email, "amount": amount * 100}
    headers = {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                response_data = await response.json()
                return {
                    "reference": response_data["data"]["reference"],
                    "authorization_url": response_data["data"]["authorization_url"],
                }
            else:
                error_message = await response.text()
                print(f"Error: {response.status} - {error_message}")
                return {"error": response.status, "message": error_message}
