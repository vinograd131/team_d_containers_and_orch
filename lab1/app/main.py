from datetime import date

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from app.storage import load_habits, save_habits

app = FastAPI(title="Habit Tracker")


class HabitCreate(BaseModel):
    name: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/habits")
def list_habits():
    return load_habits()


@app.post("/habits", status_code=201)
def create_habit(habit: HabitCreate):
    habits = load_habits()
    new_id = max((h["id"] for h in habits), default=0) + 1
    new_habit = {"id": new_id, "name": habit.name, "checks": []}
    habits.append(new_habit)
    save_habits(habits)
    return new_habit

@app.post("/habits/{habit_id}/check")
def check_habit(habit_id: int):
    habits = load_habits()
    for habit in habits:
        if habit["id"] == habit_id:
            today = date.today().isoformat()
            if today not in habit["checks"]:
                habit["checks"].append(today)
                save_habits(habits)
            return habit
    raise HTTPException(status_code=404, detail="Habit not found")