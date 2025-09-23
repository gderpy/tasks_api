from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

from app.core.security import decode_token
from app.infrastructure.memory_user_repo import UserRecord, InMemoryUserRepo

"""
Depends - встроенный механизм зависимостей в FastAPI. 
          Позволяет 'автоматически подставлять' 
          значения в функции.

HTTPException - исключение, которое FastAPI превращает в JSON-ответ с нужным статусом.

status — константы для статусов (401_UNAUTHORIZED, 404_NOT_FOUND и т.п.).

OAuth2PasswordBearer — стандартный "экстрактор токена" из 
                       заголовка Authorization: Bearer <token>.
"""

# объект, который будет забирать токен из HTTP-заголовка.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# пока что in-memory хранилище пользователей (заглушка вместо БД).
user_repo = InMemoryUserRepo()


# функция зависимости
def get_current_user(token: str = Depends(oauth2_scheme)) -> UserRecord:
    """
    Функция зависимости

    :param token: FastAPI сам возьмёт Authorization: Bearer ... из запроса,
                  передаст его как token.
    :return: текущий пользователь.
    :rtype: UserRecord
    """

    # проверяет JWT и достаёт sub (у тебя это email).
    email: Optional[str] = decode_token(token)

    # Если токен битый/просрочен → выбрасываем 401 Unauthorized.
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    # Ищем пользователя в "базе" (InMemoryUserRepo).
    user = user_repo.get_by_email(email)

    # Если его там нет → тоже 401 Unauthorized.
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    # Возвращаем найденного пользователя.

    # Теперь любой обработчик запроса (endpoint), где ты
    # напишешь user: UserRecord = Depends(get_current_user), будет
    # получать текущего авторизованного юзера.

    return user
