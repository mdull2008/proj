import hashlib
import sqlite3

DB_NAME = "app.db"

RAZDELY = ["buh", "kadry", "upr", "proiz"]


def parol_hash(parol):
    return hashlib.sha256(parol.encode("utf-8")).hexdigest()


def connect():
    return sqlite3.connect(DB_NAME)


def init_db():
    con = connect()
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS admin ("
        "id INTEGER PRIMARY KEY, login TEXT, password TEXT)"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "id INTEGER PRIMARY KEY, login TEXT, password TEXT, "
        "fio TEXT, dolzhnost TEXT, "
        "buh TEXT, kadry TEXT, upr TEXT, proiz TEXT)"
    )
    cur.execute("SELECT COUNT(*) FROM admin")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO admin (login, password) VALUES (?, ?)",
            ("admin", parol_hash("admin")),
        )
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        spisok = [
            (
                "director",
                "director",
                "Петров Сергей Николаевич",
                "директор",
                "просмотр",
                "просмотр",
                "полный",
                "просмотр",
            ),
            (
                "buhgalter",
                "buhgalter",
                "Сидорова Анна Ивановна",
                "бухгалтер",
                "полный",
                "просмотр",
                "запрещен",
                "запрещен",
            ),
            (
                "kadrovik",
                "kadrovik",
                "Козлов Игорь Петрович",
                "кадровик",
                "запрещен",
                "полный",
                "запрещен",
                "запрещен",
            ),
            (
                "findir",
                "findir",
                "Морозова Елена Викторовна",
                "финансовый директор",
                "просмотр",
                "запрещен",
                "полный",
                "запрещен",
            ),
            (
                "nachproiz",
                "nachproiz",
                "Волков Дмитрий Александрович",
                "начальник производства",
                "запрещен",
                "запрещен",
                "запрещен",
                "полный",
            ),
            (
                "madina",
                "madina",
                "Мамедова Мадина Айдынгызы",
                "бухгалтер",
                "полный",
                "просмотр",
                "запрещен",
                "запрещен",
            ),
        ]
        for row in spisok:
            login, parol, fio, dolzh, buh, kadry, upr, proiz = row
            cur.execute(
                "INSERT INTO users (login, password, fio, dolzhnost, "
                "buh, kadry, upr, proiz) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    login,
                    parol_hash(parol),
                    fio,
                    dolzh,
                    buh,
                    kadry,
                    upr,
                    proiz,
                ),
            )
    con.commit()
    con.close()


def proverit_admin(login, parol):
    con = connect()
    cur = con.cursor()
    cur.execute(
        "SELECT id FROM admin WHERE login=? AND password=?",
        (login, parol_hash(parol)),
    )
    row = cur.fetchone()
    con.close()
    return row is not None


def proverit_user(login, parol):
    con = connect()
    cur = con.cursor()
    cur.execute(
        "SELECT * FROM users WHERE login=? AND password=?",
        (login, parol_hash(parol)),
    )
    row = cur.fetchone()
    con.close()
    if row:
        return {
            "id": row[0],
            "login": row[1],
            "fio": row[3],
            "dolzhnost": row[4],
            "buh": row[5],
            "kadry": row[6],
            "upr": row[7],
            "proiz": row[8],
        }
    return None


def vse_polzovateli():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT id, fio, dolzhnost, buh, kadry, upr, proiz FROM users")
    rows = cur.fetchall()
    con.close()
    return rows


def sohranit_prava(user_id, buh, kadry, upr, proiz):
    con = connect()
    cur = con.cursor()
    cur.execute(
        "UPDATE users SET buh=?, kadry=?, upr=?, proiz=? WHERE id=?",
        (buh, kadry, upr, proiz, user_id),
    )
    con.commit()
    con.close()
