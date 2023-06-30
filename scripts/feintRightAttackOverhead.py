from scripts.base import BaseScript
import pyautogui


class FeintRightAttackOverhead(BaseScript):

    def __init__(self):
        super().__init__()
        self.name = "feintRightAttackOverhead"
        self.keyActivate = self.keys[self.name]
        self.loop = False

    def custom(self):
        pyautogui.FAILSAFE = False

        with pyautogui.hold("alt"):

            self.wait(0.1)
        with pyautogui.hold('space'):
            pyautogui.press('e')

            self.wait(0.1)
            pyautogui.press('q')




def run():
    script_class = FeintRightAttackOverhead()
    script_class.custom()


if __name__ == "__main__":
    run()
