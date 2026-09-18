from socket import AF_INET, SOCK_STREAM, socket
from urllib.parse import urlparse

from app.config import get_settings


class NetworkStatusService:
    LOCAL_HOSTS = {"127.0.0.1", "localhost"}

    def __init__(self) -> None:
        self.settings = get_settings()

    def get_status(self) -> dict[str, bool | str]:
        parsed = urlparse(self.settings.model_endpoint)
        hostname = parsed.hostname or ""
        port = parsed.port or 80
        endpoint_local = hostname in self.LOCAL_HOSTS

        reachable = False
        if endpoint_local:
            try:
                with socket(AF_INET, SOCK_STREAM) as sock:
                    sock.settimeout(0.25)
                    reachable = sock.connect_ex((hostname, port)) == 0
            except OSError:
                reachable = False

        return {
            "offline_mode": self.settings.offline_mode,
            "model_endpoint": self.settings.model_endpoint,
            "model_endpoint_local": endpoint_local,
            "model_endpoint_reachable": reachable,
            "note": "Reports app-level offline configuration and local endpoint checks; host firewall proof is out of scope.",
        }
