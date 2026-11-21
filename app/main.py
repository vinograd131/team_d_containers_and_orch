from fastapi import FastAPI

app = FastAPI(title="Habit Tracker")


@app.get("/health")
def health():
    return {"status": "ok"}