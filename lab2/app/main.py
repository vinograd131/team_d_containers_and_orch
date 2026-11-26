from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.storage import check_habit, create_habit, list_habits

app = FastAPI(title="Habit Tracker")


class HabitCreate(BaseModel):
    name: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/habits")
def get_habits():
    return list_habits()


@app.post("/habits", status_code=201)
def post_habit(habit: HabitCreate):
    return create_habit(habit.name)


@app.post("/habits/{habit_id}/check")
def post_check(habit_id: int):
    habit = check_habit(habit_id, date.today())
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit
