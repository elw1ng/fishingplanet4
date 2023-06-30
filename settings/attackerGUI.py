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
        if right.get() != "":
            settings["key2"]["value"] = right.get()
        if left.get() != "":
            settings["key3"]["value"] = left.get()
        if down.get() != "":
            settings["key4"]["value"] = down.get()
        if mode.get() != "":
            settings["key5"]["value"] = mode.get()
        if timing.get() != "":
            settings["key6"]["value"] = timing.get()
        if charging.get() != "":
            settings["key7"]["value"] = charging.get()

        data["attacker"] = settings
        tools.jsonOper.saveKeys(data)

    def reset():
        tools.jsonOper.reset()
        exit(0)

    def do():
        setting()
        exit(0)

    data = tools.jsonOper.loadKeysGui()
    settings = data["attacker"]

    window1 = Tk()
    window1.title("Mortal Online 2 Scripts")
    window1.geometry('600x400')

    count_row = 0
    for i in settings:
        if i != "base":
            if count_row == 0:

                lbl_name = Label(window1, text="Активация")
                lbl_name.grid(column=0, row=count_row)

                lbl_key = Label(window1, text=f"|    {settings[i]}")
                lbl_key.grid(column=1, row=count_row)
                count_row += 1

            else:

                lbl_name = Label(window1, text=f'{settings[i]["name"]}  ')
                lbl_name.grid(column=0, row=count_row)

                lbl_key = Label(window1, text=f'|    {settings[i]["value"]}')
                lbl_key.grid(column=1, row=count_row)
                count_row += 1

    activate = Entry(window1, width=10)
    activate.grid(column=2, row=0)

    overhead = Entry(window1, width=10)
    overhead.grid(column=2, row=1)

    right = Entry(window1, width=10)
    right.grid(column=2, row=2)

    left = Entry(window1, width=10)
    left.grid(column=2, row=3)

    down = Entry(window1, width=10)
    down.grid(column=2, row=4)

    mode = Entry(window1, width=10)
    mode.grid(column=2, row=5)

    timing = Entry(window1, width=10)
    timing.grid(column=2, row=6)

    charging = Entry(window1, width=10)
    charging.grid(column=2, row=7)

    lbl_pass = Label(window1, text="               ")
    lbl_pass.grid(column=5)
    btn = Button(window1, text="Принять настройки", command=do)
    btn.grid(column=6, row=0)
    btn = Button(window1, text="Сбросить", command=reset)
    btn.grid(column=6, row=2)
    btn = Label(window1, text="Моды: \n"
                     "1:  3 удара, боковой слева\n"
                     "2:  3 удара, боковой справа\n"
                     "3:  только нижние атаки\n"
                     "4:  нижние и верхние\n"
                     "5:  все стороны")
    btn.grid(column=2, row=8)

    window1.mainloop()


def name():
    return "attacker"

if __name__ == "__main__":
    main()



