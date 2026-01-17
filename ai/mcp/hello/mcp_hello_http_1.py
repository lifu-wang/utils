from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 1. Create the app
app = FastAPI(title="HelloWorld Tool")

# 2. Add CORS Middleware (CRITICAL for OpenWebUI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (OpenWebUI)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, OPTIONS)
    allow_headers=["*"],  # Allows all headers
)

# 3. Define the tool
@app.get("/say_hello", operation_id="say_hello")
def say_hello(name: str = "World") -> dict:
    """
    Greets the user.
    """
    return {"result": f"Hello, {name}! Connected via Native OpenAPI."}

if __name__ == "__main__":
    # Run on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)