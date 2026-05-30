import tkinter as tk

fio = "Мамедова Мадина Айдынгызы"

okno = tk.Tk()
okno.title("Кнопка")
okno.geometry("800x600")

def nazhat():
    print(fio)

knopka = tk.Button(okno, text=fio, command=nazhat)
knopka.place(relx=0.5, rely=0.5, anchor="center")

okno.mainloop()
