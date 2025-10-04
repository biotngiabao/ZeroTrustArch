# proxy_simple.py
import os
import httpx
from fastapi import FastAPI, Request, Response
from .opa.index import opa_client

UPSTREAM = os.getenv("UPSTREAM", "http://127.0.0.1:8000")  # where PHP is running

app = FastAPI()


@app.api_route(
    "/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]
)
async def proxy(path: str, request: Request):
    url = f"{UPSTREAM}/{path}"
    if request.url.query:
        url += f"?{request.url.query}"

    input_data = {
        "method": request.method,
        "path": path.split("/"),
        "token": {"roles": ["billing.viewer"]},
    }

    if not opa_client.is_allowed(
        input_data=input_data, package_path="authz", rule_name="allow"
    ):
        return Response(content="Forbidden", status_code=403)

    async with httpx.AsyncClient(follow_redirects=False, timeout=None) as client:
        r = await client.request(
            request.method,
            url,
            content=await request.body(),
            headers={k: v for k, v in request.headers.items() if k.lower() != "host"},
            cookies=request.cookies,
        )

    headers = {
        k: v
        for k, v in r.headers.items()
        if k.lower() not in {"content-length", "transfer-encoding"}
    }

    return Response(
        content=r.content,
        status_code=r.status_code,
        headers=headers,
        media_type=r.headers.get("content-type"),
    )
