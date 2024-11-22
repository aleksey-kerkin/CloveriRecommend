from typing import Dict, List, Union

from pydantic import BaseModel


class RecommendationSystem(BaseModel):
    entity_id: int  # Идентификатор пользователя или товара
    entity_type: str  # 'user' или 'product'
    features: Dict[str, Union[int, float]]  # Хар-ки пользователя или товара
    recommendations: List[Dict[str, Union[int, float]]]  # Список рекомендаций с ID и оценками

    class Config:
        from_attributes = True
