import redis
import json
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

redis_client = redis.from_url(REDIS_URL, decode_responses=True)


class RedisSessionStore:

    def _key(self, session_id: str, field: str) -> str:
        return f"session:{session_id}:{field}"

    def store_resume(self, session_id: str, text: str):
        redis_client.set(self._key(session_id, "resume"), text)
        redis_client.set(self._key(session_id, "vector_built"), "false")

    def store_jd(self, session_id: str, text: str):
        redis_client.set(self._key(session_id, "jd"), text)
        redis_client.set(self._key(session_id, "vector_built"), "false")

    def get_resume(self, session_id: str):
        return redis_client.get(self._key(session_id, "resume"))

    def get_jd(self, session_id: str):
        return redis_client.get(self._key(session_id, "jd"))

    def mark_vector_built(self, session_id: str):
        redis_client.set(self._key(session_id, "vector_built"), "true")

    def is_vector_built(self, session_id: str) -> bool:
        return redis_client.get(self._key(session_id, "vector_built")) == "true"

redis_store = RedisSessionStore()
