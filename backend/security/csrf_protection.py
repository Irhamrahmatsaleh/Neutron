from fastapi import Request, HTTPException

def check_csrf_token(request: Request):
    token = request.headers.get("X-CSRF-Token")
    if not token or token != "NEUTRON_CSRF_TOKEN":
        raise HTTPException(status_code=403, detail="CSRF token tidak valid.")
