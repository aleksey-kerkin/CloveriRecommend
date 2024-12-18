import ast
import json

from app.db.database import SessionLocal
from app.models.user import User


def load_initial_data():
    with open("data.json") as f:
        data = json.load(f)
    db = SessionLocal()
    for entry in data:
        recommendations_str = entry["recommendations"]
        # Use ast.literal_eval to safely evaluate the string as a Python list
        recommendations_list = ast.literal_eval(recommendations_str)
        user = User(
            user_hash=entry["user_hash"], name=entry["name"], recommendations=recommendations_list
        )
        db.add(user)
    db.commit()


if __name__ == "__main__":
    load_initial_data()
