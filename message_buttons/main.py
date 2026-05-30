import tkinter as tk

okno = tk.Tk()
okno.title("Кнопки")
okno.geometry("500x400")
okno.configure(bg="#555555")

tekst = "Передача сообщения"
knopki = []

ramka = tk.Frame(okno, bg="#555555")
ramka.place(relx=0.5, rely=0.5, anchor="center")

levaya = tk.Frame(ramka, bg="#555555")
levaya.pack(side="left", padx=10)

pravaya = tk.Frame(ramka, bg="#555555")
pravaya.pack(side="left", padx=10)


def nazhat(event):
    btn = event.widget
    try:
        nomer = knopki.index(btn)
    except ValueError:
        return
    text = btn.cget("text").strip()
    if text == "":
        return
    btn.config(text="")
    if nomer + 1 < len(knopki):
        sled = knopki[nomer + 1]
        sled.config(text=str(nomer + 2) + ". " + tekst)


for i in range(5):
    b = tk.Button(
        levaya,
        text="",
        width=22,
        height=2,
        bg="#87CEEB",
        activebackground="#6bb6d6",
    )
    if i == 0:
        b.config(text="1. " + tekst)
    b.pack(pady=4)
    b.bind("<Button-1>", nazhat)
    knopki.append(b)

visokaya = tk.Button(
    pravaya,
    text="",
    width=4,
    height=16,
    bg="#87CEEB",
    activebackground="#6bb6d6",
)
visokaya.pack()
visokaya.bind("<Button-1>", nazhat)
knopki.append(visokaya)

okno.mainloop()
