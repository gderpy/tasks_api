from dataclasses import dataclass
from typing import Optional


@dataclass
class UserRecord:
    id: int 
    email: str 
    password_hash: str 


class InMemoryUserRepo:
    def __init__(self) -> None:
        self._db: dict[str, UserRecord] = {}
        self._seq = 0  # счетчик для автоинкремента

    def get_by_email(self, email: str) -> Optional[UserRecord]:
        return self._db.get(email)
    
    def create(self, email: str, password_hash: str) -> UserRecord:
        self._seq += 1
        user = UserRecord(id=self._seq, email=email, password_hash=password_hash)
        
        self._db[email] = user 
        return user