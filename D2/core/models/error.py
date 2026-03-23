from pydantic import BaseModel
from typing import Optional, Any, Dict


class ErrorData(BaseModel):
    """Модель данных ошибки (data поле)"""
    status: int
    params: Optional[list] = None


class ErrorModel(BaseModel):
    """Модель ошибки WordPress API"""
    code: str
    message: str
    data: Optional[ErrorData] = None


class PostNotFoundError(ErrorModel):
    """Ошибка 404: пост не найден"""
    code: str = "rest_post_invalid_id"
    message: str = "Пост не найден."


class CommentNotFoundError(ErrorModel):
    """Ошибка 404: комментарий не найден"""
    code: str = "rest_comment_invalid_id"
    message: str = "Комментарий не найден."


class UnauthorizedError(ErrorModel):
    """Ошибка 401: не авторизован"""
    code: str = "rest_not_logged_in"
    message: str = "Вы не авторизованы."


class ForbiddenError(ErrorModel):
    """Ошибка 403: доступ запрещен"""
    code: str = "rest_forbidden"
    message: str = "Извините, вам запрещено выполнять это действие."