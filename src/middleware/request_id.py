import uuid
from fastapi import Request
from src.utils.request_context import request_id_context


async def request_id_middleware(request: Request, call_next):

    request_id = uuid.uuid4().hex[:8]

    token = request_id_context.set(request_id)

    try:
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

    finally:
        request_id_context.reset(token)