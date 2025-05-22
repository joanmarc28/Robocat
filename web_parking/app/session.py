from itsdangerous import URLSafeSerializer
from fastapi import Request, Response
import os
from dotenv import load_dotenv
load_dotenv()

serializer = URLSafeSerializer(os.getenv("SECRET_KEY"))

def create_session_cookie(user_id: int) -> str:
    return serializer.dumps({"user_id": user_id})

def get_user_from_cookie(request: Request):
    cookie = request.cookies.get("session")
    if cookie:
        try:
            data = serializer.loads(cookie)
            return data.get("user_id")
        except Exception:
            return None
    return None

def clear_session_cookie(response: Response):
    response.delete_cookie("session")
