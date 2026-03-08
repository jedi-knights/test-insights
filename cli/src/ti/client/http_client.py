import httpx

from ti.config import store


DEFAULT_BASE_URL = "http://localhost:8000"


def _base_url() -> str:
    return store.get("api_url", DEFAULT_BASE_URL).rstrip("/")


def _headers() -> dict:
    token = store.get("access_token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


def _refresh_tokens() -> bool:
    refresh_token = store.get("refresh_token")
    if not refresh_token:
        return False
    resp = httpx.post(
        f"{_base_url()}/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
        timeout=10,
    )
    if resp.status_code == 200:
        data = resp.json()
        store.set_key("access_token", data["access_token"])
        store.set_key("refresh_token", data["refresh_token"])
        return True
    return False


def request(method: str, path: str, **kwargs) -> httpx.Response:
    url = f"{_base_url()}{path}"
    resp = httpx.request(method, url, headers=_headers(), timeout=30, **kwargs)
    if resp.status_code == 401 and _refresh_tokens():
        resp = httpx.request(method, url, headers=_headers(), timeout=30, **kwargs)
    return resp


def get(path: str, **kwargs) -> httpx.Response:
    return request("GET", path, **kwargs)


def post(path: str, **kwargs) -> httpx.Response:
    return request("POST", path, **kwargs)


def put(path: str, **kwargs) -> httpx.Response:
    return request("PUT", path, **kwargs)


def delete(path: str, **kwargs) -> httpx.Response:
    return request("DELETE", path, **kwargs)
