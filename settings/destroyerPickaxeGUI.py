from tkinter import Tk, Label, Entry, Button
from main import MortalScripts
import tools.jsonOper
#
#


def main():

    def setting():

        if activate.get() != "":
            settings["activate_key"] = activate.get()
        if overhead.get() != "":
            settings["key1"]["value"] = overhead.get()
        if weapon_up.get() != "":
            settings["key2"]["value"] = weapon_up.get()
        if jump.get() != "":
            settings["key3"]["value"] = jump.get()
        if forward.get() != "":
            settings["key4"]["value"] = forward.get()
        if backward.get() != "":
            settings["key5"]["value"] = backward.get()
        if attack_charge.get() != "":
            settings["key6"]["value"] = attack_charge.get()
        if after_attack.get() != "":
            settings["key7"]["value"] = after_attack.get()
        if move_backward.get() != "":
            settings["key8"]["value"] = move_backward.get()
        if move_forward.get() != "":
            settings["key9"]["value"] = move_forward.get()

        if attack_count.get() != "":
            settings["key10"]["value"] = attack_count.get()
        if durability_per_attack.get() != "":
            settings["key11"]["value"] = durability_per_attack.get()

        if cell_1.get() != "":
            settings["key12"]["value"] = cell_1.get()
        if cell_2.get() != "":
            settings["key13"]["value"] = cell_2.get()
        if cell_3.get() != "":
            settings["key14"]["value"] = cell_3.get()
        if cell_4.get() != "":
            settings["key15"]["value"] = cell_4.get()
        if cell_5.get() != "":
            settings["key16"]["value"] = cell_5.get()
        if cell_6.get() != "":
            settings["key17"]["value"] = cell_6.get()
        if cell_7.get() != "":
            settings["key18"]["value"] = cell_7.get()
        if cell_8.get() != "":
            settings["key19"]["value"] = cell_8.get()
        if cell_9.get() != "":
            settings["key20"]["value"] = cell_9.get()

        data["destroyerPickaxe"] = settings
        tools.jsonOper.saveKeys(data)


    def reset():
        tools.jsonOper.reset()
        exit(0)

    def do():
        setting()
        exit(0)

    data = tools.jsonOper.loadKeysGui()
    settings = data["destroyerPickaxe"]

    window1 = Tk()
    window1.title("Mortal Online 2 Scripts")
    window1.geometry('400x600')

    count_row = 0
    for i in settings:
        if i != "base":
            if count_row == 0:

                lbl_name = Label(window1, text="Активация")
                lbl_name.grid(column=0, row=count_row)

                lbl_key = Label(window1, text=settings[i])
                lbl_key.grid(column=1, row=count_row)
                count_row += 1

            else:

                lbl_name = Label(window1, text=settings[i]["name"])
                lbl_name.grid(column=0, row=count_row)

                lbl_key = Label(window1, text=settings[i]["value"])
                lbl_key.grid(column=1, row=count_row)
                count_row += 1

    activate = Entry(window1, width=10)
    activate.grid(column=2, row=0)

    overhead = Entry(window1, width=10)
    overhead.grid(column=2, row=1)

    weapon_up = Entry(window1, width=10)
    weapon_up.grid(column=2, row=2)

    jump = Entry(window1, width=10)
    jump.grid(column=2, row=3)

    forward = Entry(window1, width=10)
    forward.grid(column=2, row=4)

    backward = Entry(window1, width=10)
    backward.grid(column=2, row=5)

    attack_charge = Entry(window1, width=10)
    attack_charge.grid(column=2, row=6)

    after_attack = Entry(window1, width=10)
    after_attack.grid(column=2, row=7)

    move_backward = Entry(window1, width=10)
    move_backward.grid(column=2, row=8)

    move_forward = Entry(window1, width=10)
    move_forward.grid(column=2, row=9)

    attack_count = Entry(window1, width=10)
    attack_count.grid(column=2, row=10)

    durability_per_attack = Entry(window1, width=10)
    durability_per_attack.grid(column=2, row=11)

    cell_1 = Entry(window1, width=10)
    cell_1.grid(column=2, row=12)

    cell_2 = Entry(window1, width=10)
    cell_2.grid(column=2, row=13)

    cell_3 = Entry(window1, width=10)
    cell_3.grid(column=2, row=14)

    cell_4 = Entry(window1, width=10)
    cell_4.grid(column=2, row=15)

    cell_5 = Entry(window1, width=10)
    cell_5.grid(column=2, row=16)

    cell_6 = Entry(window1, width=10)
    cell_6.grid(column=2, row=17)

    cell_7 = Entry(window1, width=10)
    cell_7.grid(column=2, row=18)

    cell_8 = Entry(window1, width=10)
    cell_8.grid(column=2, row=19)

    cell_9 = Entry(window1, width=10)
    cell_9.grid(column=2, row=20)

    lbl_pass = Label(window1, text="               ")
    lbl_pass.grid(column=5)
    btn = Button(window1, text="Принять настройки", command=do)
    btn.grid(column=6, row=0)
    btn = Button(window1, text="Сбросить", command=reset)
    btn.grid(column=6, row=2)

    window1.mainloop()


def name():
    return "destroyerPickaxe"


if __name__ == "__main__":
    main()


