import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    # Get port from environment variable or default to 8000
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "127.0.0.1")

    print(f"Starting TungTungSahur API on http://{host}:{port}")

    uvicorn.run("app.main:app", host=host, port=port, reload=True, log_level="info")
