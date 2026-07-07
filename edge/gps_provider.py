import time
from typing import Dict, Optional

try:
    import serial
    import pynmea2
except Exception:
    serial = None
    pynmea2 = None


class GPSProvider:
    """Provides GPS location either from fixed config or serial GPS module."""

    def __init__(self, mode: str = "fixed", fixed_latitude: float = 0.0, fixed_longitude: float = 0.0, serial_port: str = "/dev/ttyUSB0", baud_rate: int = 9600):
        self.mode = mode
        self.fixed_latitude = fixed_latitude
        self.fixed_longitude = fixed_longitude
        self.serial_port = serial_port
        self.baud_rate = baud_rate

    def get_location(self) -> Dict[str, Optional[float]]:
        if self.mode == "serial":
            loc = self._read_serial_once()
            if loc:
                return loc
        return {"latitude": self.fixed_latitude, "longitude": self.fixed_longitude}

    def _read_serial_once(self) -> Optional[Dict[str, float]]:
        if serial is None or pynmea2 is None:
            return None
        try:
            with serial.Serial(self.serial_port, self.baud_rate, timeout=2) as ser:
                start = time.time()
                while time.time() - start < 3:
                    line = ser.readline().decode("ascii", errors="ignore").strip()
                    if line.startswith("$GPGGA") or line.startswith("$GPRMC"):
                        msg = pynmea2.parse(line)
                        if getattr(msg, "latitude", None) and getattr(msg, "longitude", None):
                            return {"latitude": float(msg.latitude), "longitude": float(msg.longitude)}
        except Exception:
            return None
        return None
