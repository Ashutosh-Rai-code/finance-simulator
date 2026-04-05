from fastapi import APIRouter, HTTPException, Request

from services import VisitorCounter

router = APIRouter(prefix="/api/visitors", tags=["visitors"])
visitor_counter = VisitorCounter()


def get_client_ip(request: Request) -> str:
    """Extract client IP from request, accounting for proxies."""
    if request.headers.get('x-forwarded-for'):
        return request.headers.get('x-forwarded-for').split(',')[0].strip()
    return request.client.host if request.client else "unknown"


@router.get("/")
def get_visitor_count():
    """Return the current unique visitor count."""
    try:
        return {"count": visitor_counter.get_count()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
def track_visitor(request: Request):
    """Track a unique visitor by IP address and return current count."""
    try:
        client_ip = get_client_ip(request)
        count = visitor_counter.register_visitor(client_ip)
        return {"count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
