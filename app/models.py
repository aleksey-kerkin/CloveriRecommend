from typing import Dict, List, Union

from pydantic import BaseModel


class RecommendationSystem(BaseModel):
    entity_id: int  # Идентификатор пользователя или товара
    entity_type: str  # 'user' или 'product'
    features: Dict[str, float]  # Хар-ки пользователя или товара
    recommendations: List[Dict[str, Union[int, float]]]  # Список рекомендаций с ID и оценками

    class Config:
        json_schema_extra = {
            "example": {
                "entity_id": 123,
                "entity_type": "user",
                "features": {"age": 25, "gender": 0.0, "interest_score": 0.8},
                "recommendations": [
                    {"product_id": 456, "recommendation_score": 0.9},
                    {"product_id": 789, "recommendation_score": 0.85},
                ],
            }
        }
