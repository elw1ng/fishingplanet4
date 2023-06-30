from scripts.base import BaseScript


class Domination(BaseScript):

    def __init__(self):
        super().__init__()
        self.name = "domination"
        self.keys = self.keys_data[self.name]
        self.keyActivate = self.keys["activate_key"]

    def custom(self):

        print("16 domination")
        # self.press("{CTRLDOWN}")
        self.wait(0.1)
        self.hold("v")
        self.wait(5)
        # self.press("{CTRLUP}")
        self.wait(0.1)
        self.release("r")
        self.wait(0.2)


def run():
    script_class = Domination()
    script_class.custom()


if __name__ == "__main__":
    run()

