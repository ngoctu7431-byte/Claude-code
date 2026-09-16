"""Kiem tra ket noi toi ERPNext/Frappe. Chi dung thu vien co san cua Python.

Cach chay (khong can cai dat gi):
    python3 check_erp.py <API_KEY> <API_SECRET>

Hoac dat bien moi truong FRAPPE_API_KEY / FRAPPE_API_SECRET roi chay:
    python3 check_erp.py
"""

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime

BASE_URL = os.environ.get("FRAPPE_URL", "https://platform.nguoithuanviet.com").rstrip("/")


def call(path: str, token: str | None) -> tuple[int, str]:
    request = urllib.request.Request(f"{BASE_URL}{path}")
    request.add_header("Accept", "application/json")
    if token:
        request.add_header("Authorization", f"token {token}")
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.status, response.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")
    except Exception as exc:
        return 0, f"{type(exc).__name__}: {exc}"


def main() -> int:
    if len(sys.argv) >= 3:
        key, secret = sys.argv[1], sys.argv[2]
    else:
        key = os.environ.get("FRAPPE_API_KEY", "")
        secret = os.environ.get("FRAPPE_API_SECRET", "")

    if not key or not secret:
        print("Thieu API key/secret. Chay: python3 check_erp.py <API_KEY> <API_SECRET>")
        return 2

    ping_status, ping_body = call("/api/method/frappe.ping", None)
    print(f"ping: HTTP {ping_status} {ping_body.strip()[:120]}")
    if ping_status != 200:
        print("=> Khong toi duoc server. Kiem tra mang/domain truoc khi xet API key.")
        return 1

    auth_status, auth_body = call("/api/method/frappe.auth.get_logged_user", f"{key}:{secret}")
    if auth_status != 200:
        print(f"auth: HTTP {auth_status} {auth_body.strip()[:300]}")
        print("=> 401/403 la sai API key/secret. Vao ERP > User > API Access > Generate Keys.")
        return 1

    try:
        email = json.loads(auth_body).get("message", "")
    except json.JSONDecodeError:
        print(f"auth: HTTP 200 nhung khong doc duoc JSON: {auth_body.strip()[:300]}")
        return 1

    print(f"email: {email}")
    print(f"thoi gian: {datetime.now().astimezone().isoformat(timespec='seconds')}")
    print("=> KET NOI ERP THANH CONG")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
