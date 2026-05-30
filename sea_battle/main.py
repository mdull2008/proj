import random
import tkinter as tk
from tkinter import messagebox

RAZMER = 10
KORABLI = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]


class Igra:
    def __init__(self):
        self.okno = tk.Tk()
        self.okno.title("Морской бой")
        self.okno.resizable(False, False)

        self.karta_igrok = {}
        self.karta_vrag = {}
        self.korabli_vrag = {}
        self.ochered = 0
        self.vert = False
        self.faza = "rasstanovka"
        self.hod_igroka = True

        self.ramka = tk.Frame(self.okno)
        self.ramka.pack(padx=10, pady=10)

        self.panel = tk.Frame(self.okno)
        self.panel.pack(pady=5)

        self.knopki_igrok = []
        self.knopki_vrag = []

        self.narisovat_pole()
        self.obnovit_panel()
        self.rasstavit_vraga()

    def sosedi(self, x, y):
        spisok = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                spisok.append((x + dx, y + dy))
        return spisok

    def kletki_korablya(self, x, y, dlina, vert):
        tochki = []
        for i in range(dlina):
            if vert:
                nx, ny = x, y + i
            else:
                nx, ny = x + i, y
            if nx < 0 or nx >= RAZMER or ny < 0 or ny >= RAZMER:
                return None
            tochki.append((nx, ny))
        return tochki

    def mozhno_postavit(self, karta, x, y, dlina, vert):
        tochki = self.kletki_korablya(x, y, dlina, vert)
        if not tochki:
            return False, []
        for tx, ty in tochki:
            if (tx, ty) in karta:
                return False, []
        for tx, ty in tochki:
            for sx, sy in self.sosedi(tx, ty):
                if (sx, sy) in karta:
                    return False, []
        return True, tochki

    def postavit_na_kartu(self, karta, tochki, nomer):
        for t in tochki:
            karta[t] = nomer

    def sluchayno(self, karta):
        poryadok = KORABLI[:]
        random.shuffle(poryadok)
        vrem = {}
        for dlina in poryadok:
            udalos = False
            for popytka in range(500):
                x = random.randint(0, RAZMER - 1)
                y = random.randint(0, RAZMER - 1)
                vert = random.choice([True, False])
                ok, tochki = self.mozhno_postavit(vrem, x, y, dlina, vert)
                if ok:
                    self.postavit_na_kartu(vrem, tochki, dlina)
                    udalos = True
                    break
            if not udalos:
                return False
        for key, val in vrem.items():
            karta[key] = val
        return True

    def rasstavit_vraga(self):
        while not self.sluchayno(self.karta_vrag):
            self.karta_vrag = {}

    def vrag_unichen(self):
        for kletka in self.karta_vrag:
            if kletka not in self.korabli_vrag:
                return False
            if self.korabli_vrag[kletka] != "popal":
                return False
        return True

    def igrok_unichen(self):
        for kletka, znach in self.karta_igrok.items():
            if isinstance(znach, int):
                return False
        return True

    def narisovat_pole(self):
        for w in self.ramka.winfo_children():
            w.destroy()
        self.knopki_igrok = []
        self.knopki_vrag = []

        tk.Label(self.ramka, text="Ваше поле").grid(row=0, column=0, padx=10)
        tk.Label(self.ramka, text="Поле врага").grid(row=0, column=1, padx=10)

        pole1 = tk.Frame(self.ramka)
        pole1.grid(row=1, column=0)
        pole2 = tk.Frame(self.ramka)
        pole2.grid(row=1, column=1)

        for y in range(RAZMER):
            row1 = []
            row2 = []
            for x in range(RAZMER):
                b1 = tk.Button(
                    pole1,
                    width=2,
                    height=1,
                    command=lambda x=x, y=y: self.klik_igrok(x, y),
                )
                b1.grid(row=y, column=x, padx=1, pady=1)
                row1.append(b1)

                b2 = tk.Button(
                    pole2,
                    width=2,
                    height=1,
                    command=lambda x=x, y=y: self.klik_vrag(x, y),
                )
                b2.grid(row=y, column=x, padx=1, pady=1)
                row2.append(b2)
            self.knopki_igrok.append(row1)
            self.knopki_vrag.append(row2)

        self.obnovit_vse()

    def obnovit_vse(self):
        for y in range(RAZMER):
            for x in range(RAZMER):
                b1 = self.knopki_igrok[y][x]
                b2 = self.knopki_vrag[y][x]
                b1.config(text="", bg="SystemButtonFace")
                b2.config(text="", bg="SystemButtonFace")

                if (x, y) in self.karta_igrok and self.faza == "rasstanovka":
                    b1.config(bg="#7ec8ff")
                if (x, y) in self.karta_igrok and self.faza == "igra":
                    b1.config(bg="#7ec8ff")
                if (x, y) in self.korabli_vrag:
                    if self.korabli_vrag[(x, y)] == "promah":
                        b2.config(bg="#dddddd", text="•")
                    if self.korabli_vrag[(x, y)] == "popal":
                        b2.config(bg="#ff6666", text="X")
                if self.faza == "igra":
                    z = self.karta_igrok.get((x, y))
                    if z == "promah":
                        b1.config(bg="#dddddd", text="•")
                    elif z == "hit":
                        b1.config(bg="#ff6666", text="X")
                    elif isinstance(z, int):
                        b1.config(bg="#7ec8ff")

    def obnovit_panel(self):
        for w in self.panel.winfo_children():
            w.destroy()
        if self.faza == "rasstanovka":
            if self.ochered < len(KORABLI):
                dlina = KORABLI[self.ochered]
                napr = "вертикаль" if self.vert else "горизонталь"
                tk.Label(
                    self.panel,
                    text="Корабль на " + str(dlina) + " клетки, " + napr,
                ).pack(side="left", padx=5)
                tk.Button(
                    self.panel, text="Поворот", command=self.povorot
                ).pack(side="left", padx=5)
                tk.Button(
                    self.panel, text="Случайно", command=self.avto_igrok
                ).pack(side="left", padx=5)
            else:
                tk.Button(
                    self.panel, text="Начать игру", command=self.start_igry
                ).pack()
        else:
            txt = "Ваш ход" if self.hod_igroka else "Ход врага"
            tk.Label(self.panel, text=txt).pack()

    def povorot(self):
        self.vert = not self.vert
        self.obnovit_panel()

    def avto_igrok(self):
        self.karta_igrok = {}
        if self.sluchayno(self.karta_igrok):
            self.ochered = len(KORABLI)
            self.obnovit_vse()
            self.obnovit_panel()

    def klik_igrok(self, x, y):
        if self.faza != "rasstanovka":
            return
        if self.ochered >= len(KORABLI):
            return
        dlina = KORABLI[self.ochered]
        ok, tochki = self.mozhno_postavit(self.karta_igrok, x, y, dlina, self.vert)
        if not ok:
            messagebox.showwarning("Ошибка", "Сюда нельзя поставить корабль")
            return
        self.postavit_na_kartu(self.karta_igrok, tochki, dlina)
        self.ochered += 1
        self.obnovit_vse()
        self.obnovit_panel()

    def start_igry(self):
        self.faza = "igra"
        self.obnovit_panel()

    def klik_vrag(self, x, y):
        if self.faza != "igra" or not self.hod_igroka:
            return
        if (x, y) in self.korabli_vrag:
            return
        if (x, y) in self.karta_vrag:
            self.korabli_vrag[(x, y)] = "popal"
        else:
            self.korabli_vrag[(x, y)] = "promah"
            self.hod_igroka = False
            self.okno.after(400, self.hod_vraga)
        self.obnovit_vse()
        if self.vrag_unichen():
            messagebox.showinfo("Победа", "Вы выиграли")
            self.faza = "konets"

    def hod_vraga(self):
        if self.faza != "igra":
            return
        for popytka in range(200):
            x = random.randint(0, RAZMER - 1)
            y = random.randint(0, RAZMER - 1)
            if (x, y) in self.karta_igrok and isinstance(
                self.karta_igrok[(x, y)], str
            ):
                continue
            if (x, y) in self.karta_igrok:
                self.karta_igrok[(x, y)] = "hit"
            else:
                self.karta_igrok[(x, y)] = "promah"
            break
        self.hod_igroka = True
        self.obnovit_vse()
        if self.igrok_unichen():
            messagebox.showinfo("Поражение", "Вы проиграли")
            self.faza = "konets"
        self.obnovit_panel()

    def run(self):
        self.okno.mainloop()


if __name__ == "__main__":
    Igra().run()
