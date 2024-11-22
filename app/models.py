from sqlalchemy import JSON, Column, Integer, String

from ..database import Base


class RecommendationSystem(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, nullable=False)  # ID записи
    entity_id = Column(Integer, nullable=False)  # ID пользователя или товара
    entity_type = Column(String, nullable=False)  # 'user' или 'product'
    features = Column(JSON, nullable=False)  # Хар-ки пользователя или товара
    recommendations = Column(JSON, nullable=False)  # Список рекомендаций с ID и оценками
