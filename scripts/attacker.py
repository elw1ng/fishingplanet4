import random
from scripts.base import BaseScript
import pyautogui


class Attacker(BaseScript):

    def __init__(self):
        super().__init__()
        self.name = "attacker"
        self.keys = self.keys_data[self.name]  # загрузка настройки всех ключей данного скрипта
        self.keyActivate = self.keys["activate_key"]  # кнопка активации скрипта
        overhead = self.keys["key1"]["value"]
        right = self.keys["key2"]["value"]
        left = self.keys["key3"]["value"]
        down = self.keys["key4"]["value"]
        self.mode = self.keys["key5"]["value"]
        self.timing = float(self.keys["key6"]["value"])
        self.charging = float(self.keys["key7"]["value"])
        self.move_keys = []
        match self.mode:
            case '1':
                self.move_keys = [overhead, down, left]
            case '2':
                self.move_keys = [overhead, down, right]
            case '3':
                self.move_keys = [down]
            case '4':
                self.move_keys = [overhead, down]
            case '5':
                self.move_keys = [overhead, down, right, left]

    def custom(self):
        self._debug(f" mode = {self.mode}")
        self.hold_and_release_wait(random.choice(self.move_keys), self.charging)
        self.wait(self.timing)


def run():
    script_class = Attacker()
    script_class.custom()


if __name__ == "__main__":
    run()
