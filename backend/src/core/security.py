from passlib.context import CryptContext

# from src.core.config import get_settings

crypto_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def verify_data(plain_data: str, hashed_data: str) -> bool:
        return crypto_context.verify(plain_data, hashed_data)

    @staticmethod
    def get_data_hash(data: str) -> str:
        return crypto_context.hash(data)
