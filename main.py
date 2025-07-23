from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Routers for leads, organizations, scraping, etc. will be included here 