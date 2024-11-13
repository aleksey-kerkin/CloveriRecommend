from typing import Dict

from fastapi import FastAPI
from models import RecommendationSystem

from ml.model import load_model, predict  # Предположим, что у нас есть такие функции

app = FastAPI()
model = None


# Создаем маршрут
@app.get("/")
def index():
    return {"text": "Система рекомендаций товаров"}


# Регистрируем функцию, которая будет выполняться при старте
@app.on_event("startup")
def startup_event():
    global model
    model = load_model()


# Обработчики маршрутов FastAPI
@app.get("/predict", response_model=RecommendationSystem)
def predict_recommendations(entity_id: int, entity_type: str, features: Dict[str, float]):
    recommendations = predict(model, entity_id, entity_type, features)

    response = RecommendationSystem(
        entity_id=entity_id,
        entity_type=entity_type,
        features=features,
        recommendations=recommendations,
    )
    return response
