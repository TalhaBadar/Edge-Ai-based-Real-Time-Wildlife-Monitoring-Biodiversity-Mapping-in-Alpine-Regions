import socket


class InternetMonitor:
    @staticmethod
    def is_connected(host: str = "8.8.8.8", port: int = 53, timeout: float = 2.0) -> bool:
        try:
            socket.setdefaulttimeout(timeout)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((host, port))
            return True
        except OSError:
            return False
