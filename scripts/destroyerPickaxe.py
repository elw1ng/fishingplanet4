import random
from scripts.base import BaseScript
import autoit
import time


class DestroyerPickAxe(BaseScript):

    def __init__(self):
        super().__init__()
        self.name = "destroyerPickaxe"
        self.keys = self.keys_data[self.name]
        self.keyActivate = self.keys["activate_key"]
        self.durability = int(self.keys["key10"]["value"])
        self.durability_per_attack = float(self.keys["key11"]["value"])
        self.attacks_count = int(round(self.durability / self.durability_per_attack / 8))  # 1866  933  467  234

        self.cell_1 = self.keys["key12"]["value"]
        self.cell_2 = self.keys["key13"]["value"]
        self.cell_3 = self.keys["key14"]["value"]
        self.cell_4 = self.keys["key15"]["value"]
        self.cell_5 = self.keys["key16"]["value"]
        self.cell_6 = self.keys["key17"]["value"]
        self.cell_7 = self.keys["key18"]["value"]
        self.cell_8 = self.keys["key19"]["value"]
        self.cell_9 = self.keys["key20"]["value"]

        self.weapon_slot = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", self.cell_1, self.cell_2, self.cell_3, self.cell_4, self.cell_5, self.cell_6, self.cell_7, self.cell_8, self.cell_9]  #
        self.started = False
        self.attack_overhead = self.keys["key1"]["value"]
        self.take_weapon = self.keys["key2"]["value"]
        self.jump_key = self.keys["key3"]["value"]
        self.key_forward = self.keys["key4"]["value"]
        self.key_backward = self.keys["key5"]["value"]
        self.hold_attack_time = float(self.keys["key6"]["value"])
        self.after_attack_time = float(self.keys["key7"]["value"])
        self.backward_walking_time = float(self.keys["key8"]["value"])
        self.forward_walking_time = float(self.keys["key9"]["value"])



        self.attack_actually_count_all = 0
        self.actually_weapon = ""


    def master_action(self):
        if not self.started:
            self.started = True
            for key in self.weapon_slot:
                self.actually_weapon = key if "+" not in key else f"shift{key}"
                self.attack_actually_count_all = 0
                self.weapon_changer(key)
                self.attack_and_antiafk()
        self.jumping()

    def jumping(self):
        self.hold_and_release_wait(self.jump_key, 0.3)
        self.wait(1)
        print("jumping")

    def random_float(self):
        return random.uniform(0.7, 1.3)

    def moving(self):
        multiply = self.random_float()
        time_backward = self.backward_walking_time * multiply
        time_forward = self.forward_walking_time * multiply

        self.hold_and_release_wait(self.key_backward, time_backward)
        self.wait(0.2)
        for _ in range(random.choice([1, 2])):
            self.jumping()
        self.wait(0.2)
        self.hold_and_release_wait(self.key_forward, time_forward)
        self.wait(0.5)

        multiply = self.random_float()
        time_backward = self.backward_walking_time * multiply
        time_forward = self.forward_walking_time * multiply

        self.hold_and_release_wait(self.key_backward, time_backward)
        self.wait(0.2)
        for _ in range(random.choice([1, 2])):
            self.jumping()
        self.wait(0.2)
        self.hold_and_release_wait(self.key_forward, time_forward)
        self.wait(0.5)

    def attack_loop(self):
        count = 0
        while self.attacks_count > count:
            if self.isStop or self.exitKey:
                break
            self.attacker()
            self.attack_actually_count_all += 1
            count += 1
            print(f"Кирка клавиши: {self.actually_weapon}                    Пауза: F7        Закрыть: F9")
            print(f"Осталось ударов в цикле: {self.attacks_count - count}")
            print(f"Осталось ударов всего: {(self.attacks_count * 8) - self.attack_actually_count_all}")
            print(f"Предположительная прочность кирки: {round((self.durability - self.attack_actually_count_all*self.durability_per_attack)*100)/100}")
            print()

    def attack_and_antiafk(self):

        for _ in range(8):
            self.wait(1.03)
            self.attack_loop()
            self.wait(1.03)
            self.moving()
            self.wait(1.03)

    def attacker(self):
        if not self.isStop and not self.exitKey:
            self.hold_and_release_wait(self.attack_overhead, self.hold_attack_time)
            time.sleep(self.after_attack_time)
            print()

    def weapon_changer(self, key):
        self.wait(1)
        self.press(key)
        self.wait(2)
        self.press(self.take_weapon)
        self.wait(1)

    def customLoop(self):
        self.started = False
        while not self.exitKey and not self.isStop:
            self.custom()
            self.checkExitKey()
            self.checkStopKey()

    def custom(self):
        self.master_action()


def run():
    script_class = DestroyerPickAxe()
    script_class.custom()


if __name__ == "__main__":
    run()


