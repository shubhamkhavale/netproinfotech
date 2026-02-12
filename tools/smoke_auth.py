#!/usr/bin/env python3
"""
Smoke test for auth availability.

Checks:
1) GET /accounts/login/ returns 200
2) POST /accounts/login/ with invalid credentials does not return 500
"""

import argparse
import http.cookiejar
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request


DEFAULT_TIMEOUT = 20


def http_request(opener, url, method="GET", data=None, headers=None, timeout=DEFAULT_TIMEOUT):
    request = urllib.request.Request(url, data=data, method=method)
    for key, value in (headers or {}).items():
        request.add_header(key, value)

    try:
        with opener.open(request, timeout=timeout) as response:
            return response.status, response.read().decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as error:
        return error.code, error.read().decode("utf-8", errors="ignore")


def extract_csrf_token(html):
    match = re.search(r'name="csrfmiddlewaretoken"\s+value="([^"]+)"', html)
    return match.group(1) if match else None


def run_smoke(base_url, timeout):
    login_url = f"{base_url.rstrip('/')}/accounts/login/"
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())
    )

    get_status, get_body = http_request(
        opener,
        login_url,
        method="GET",
        headers={"User-Agent": "netproinfotech-smoke/1.0"},
        timeout=timeout,
    )
    if get_status != 200:
        print(f"[FAIL] GET {login_url} -> {get_status} (expected 200)")
        return 1
    print(f"[PASS] GET {login_url} -> {get_status}")

    csrf_token = extract_csrf_token(get_body)
    if not csrf_token:
        print("[FAIL] CSRF token not found on login page")
        return 1

    payload = urllib.parse.urlencode(
        {
            "csrfmiddlewaretoken": csrf_token,
            "username": "invalid_smoke_user",
            "password": "invalid_smoke_password",
        }
    ).encode("utf-8")

    post_status, _ = http_request(
        opener,
        login_url,
        method="POST",
        data=payload,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": login_url,
            "User-Agent": "netproinfotech-smoke/1.0",
        },
        timeout=timeout,
    )

    if post_status >= 500:
        print(f"[FAIL] POST {login_url} -> {post_status} (unexpected server error)")
        return 1

    print(f"[PASS] POST {login_url} -> {post_status} (non-500 as expected)")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Auth smoke test for netproinfotech")
    parser.add_argument(
        "--base-url",
        default=os.getenv("SMOKE_BASE_URL", "http://127.0.0.1:8000"),
        help="Base URL to test, e.g. https://netproinfotech.onrender.com",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"HTTP timeout in seconds (default: {DEFAULT_TIMEOUT})",
    )
    args = parser.parse_args()

    exit_code = run_smoke(args.base_url, args.timeout)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
