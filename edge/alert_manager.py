from utils.yolo_utils import load_dangerous_classes


class AlertManager:
    def __init__(self, classes_yaml: str = "configs/classes.yaml", enable_console: bool = True, enable_gpio: bool = False, gpio_pin: int = 18):
        self.dangerous = load_dangerous_classes(classes_yaml)
        self.enable_console = enable_console
        self.enable_gpio = enable_gpio
        self.gpio_pin = gpio_pin
        self.gpio = None
        if enable_gpio:
            try:
                import Jetson.GPIO as GPIO
                self.gpio = GPIO
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(gpio_pin, GPIO.OUT)
            except Exception:
                self.gpio = None

    def is_dangerous(self, species: str) -> bool:
        return species in self.dangerous

    def trigger(self, species: str, confidence: float):
        if self.enable_console:
            print(f"ALERT: Dangerous animal detected -> {species} ({confidence:.2f})")
        if self.gpio:
            try:
                self.gpio.output(self.gpio_pin, self.gpio.HIGH)
            except Exception:
                pass

    def cleanup(self):
        if self.gpio:
            try:
                self.gpio.output(self.gpio_pin, self.gpio.LOW)
                self.gpio.cleanup()
            except Exception:
                pass
