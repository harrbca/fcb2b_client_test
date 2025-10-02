import hmac
import hashlib
import base64
import urllib.parse
import requests
import yaml

from datetime import datetime, timezone
from typing import Dict

class FCB2BClient:
    def __init__(self, host: str, api_key: str, secret_key: str, *, timeout: int = 20):
        """
        host: authority only (e.g. "des.buckwold.com")
        api_key: API key (e.g. "anonymous")
        secret_key: secret key string
        timeout: HTTP timeout seconds
        """
        self.host = host
        self.api_key = api_key
        self.secret_key = secret_key
        self.timeout = timeout

    @staticmethod
    def get_TimeStamp() -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def _encode(value: str) -> str:
        return urllib.parse.quote(value, safe="-_.~")

    def _sign(self, path: str, params: Dict[str, str]) -> Dict[str, str]:
        query_string = "&".join(
            f"{self._encode(k)}={self._encode(v)}"
            for k, v in sorted(params.items())
        )

        string_to_sign = f"GET\n{self.host}\n{path}\n{query_string}"
        digest = hmac.new(self.secret_key.encode("utf-8"),
                          string_to_sign.encode("utf-8"),
                          hashlib.sha256).digest()

        signature_encoded = self._encode(base64.b64encode(digest).decode())

        url = f"https://{self.host}{path}?{query_string}&Signature={signature_encoded}"
        return {
            "string_to_sign": string_to_sign,
            "url": url,
        }


    def get(self, path: str, params: Dict[str, str], *, accept: str = "application/xml") -> Dict[str, str]:
        """
        Perform a signed GET request.
        params must include required fcB2B query parameters (e.g. SupplierItemSKU, TimeStamp, GlobalIdentifier).
        Adds apiKey automatically if not present.
        """
        if "apiKey" not in params:
            params["apiKey"] = self.api_key

        signed = self._sign(path, params)
        resp = requests.get(signed["url"], headers={"Accept": accept}, timeout=self.timeout)

        return {
            "status": resp.status_code,
            "text": resp.text,
            "url": signed["url"],
            "string_to_sign": signed["string_to_sign"]
        }


def load_client_from_yaml(path: str = "config.yaml") -> tuple[FCB2BClient, dict]:
    """
    Reads config.yaml and returns (client, paths_dict)
    """
    with open(path, "r") as f:
        cfg = yaml.safe_load(f)
    client = FCB2BClient(
        host=cfg["host"],
        api_key=cfg["apiKey"],
        secret_key=cfg["secretKey"]
    )

    # print config
    print(f"Config loaded from {path}")
    print(f"Host: {client.host}")
    print(f"API Key: {client.api_key}")
    print(f"Secret Key: {client.secret_key}")
    print()

    return client, cfg.get("paths", {})