from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from typing import Optional

from app.config import settings

# алгоритм подписи токена (HS256 = HMAC + SHA-256)
ALGO = "HS256"

# секретный ключ
SECRET = settings.JWT_SECRET

# сколько минут будет жить токен в env - 60 минут по умолчанию
ACCESS_TTL_MIN = settings.JWT_TTL_MIN

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(raw: str) -> str:
    # qwerty -> %@5d5281....
    return pwd_context.hash(raw)


def verify_password(raw: str, hashed: str) -> bool:
    # qwerty == %@5d5281....
    return pwd_context.verify(raw, hashed)


def create_access_token(sub: str) -> str:
    """
    Создание токена
    """
    now = datetime.now(timezone.utc)

    payload = {
        # идентификатор пользователя (например, user_id или email)
        "sub": sub,
        # (issued at) — время создания токена.
        "iat": int(now.timestamp()),
        # (expiry) — срок жизни токена (now + ACCESS_TTL_MIN).
        "exp": int((now + timedelta(minutes=ACCESS_TTL_MIN)).timestamp()),
    }

    # JWT: header.payload.signature
    # header = метаданные (алгоритм подписи, тип токена)
    # payload = твои данные (sub, iat, exp)
    # signature = подпись, которую можно проверить только с твоим SECRET

    return jwt.encode(payload, SECRET, algorithm=ALGO)  # eyJhbGciOiJI....


def decode_token(token: str) -> Optional[str]:
    """
    Расшифровка токена
    """
    try:

        # 1. Берёт токен (header.payload.signature).
        # 2. Проверяет подпись (signature) с твоим SECRET и алгоритмом HS256.
        # 3. Проверяет, что exp (срок жизни) не истёк.
        # Если всё ок — возвращает payload в виде словаря Python.

        # {
        #   "sub": "user123",
        #   "iat": 1695489120,
        #   "exp": 1695492720
        # }

        data = jwt.decode(token, SECRET, algorithms=[ALGO])

        # Извлекаем из payload поле sub — то, что мы сами туда клали
        # при создании токена (например, id пользователя).

        return data.get("sub")

    # Если токен:
    # подделан (подпись не совпала),
    # просрочен (exp меньше текущего времени),
    # сломан (битая строка),
    # -> то вылетает JWTError, и мы возвращаем None.

    except JWTError:
        return None
