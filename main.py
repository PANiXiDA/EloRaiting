from tkinter import *
import sqlite3

def Data(x, y, a, b):
    alf = '0123456789'
    Ka = a - b;
    Kb = b - a;
    Ra = ''
    Rb = ''

    conn = sqlite3.connect('orders.db')
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users(
       nickname TEXT,
       elo BIGINT
    )""")
    conn.commit()

    user_nickname1 = x
    '''for value in cur.execute("SELECT * FROM users"):
        print(value)'''

    cur.execute('''SELECT nickname FROM users WHERE nickname = ?''', (user_nickname1,))
    if cur.fetchone() is None:
        cur.execute(f"INSERT INTO users VALUES (?, ?)", (user_nickname1, 1000))
        conn.commit()
        Ra = 1000
    else:
        cur.execute('''SELECT elo FROM users WHERE nickname = ?''', (user_nickname1,))
        s = cur.fetchone()
        Ra = int(s[0])

    user_nickname2 = y

    cur.execute('''SELECT nickname FROM users WHERE nickname = ?''', (user_nickname2,))
    if cur.fetchone() is None:
        cur.execute(f"INSERT INTO users VALUES (?, ?)", (user_nickname2, 1000))
        conn.commit()
        Rb = 1000
    else:
        cur.execute('''SELECT elo FROM users WHERE nickname = ?''', (user_nickname2,))
        s = cur.fetchone()
        Rb = int(s[0])
    Ea = 1 / (1 + 10 ** ((Rb - Ra) / 400))
    Eb = 1 / (1 + 10 ** ((Ra - Rb) / 400))
    if (Ka>0):
        Ra = int(Ra + 16 * (1 - Ea)*Ka)+1
        Rb = int(Rb + 16 * (0 - Eb)*Ka)
    else:
        Ra = int(Ra + 16 * (0 - Ea)*Kb)
        Rb = int(Rb + 16 * (1 - Eb)*Kb)+1
    print(Ra, Rb)

    cur.execute(f'UPDATE users SET elo = {Ra} WHERE nickname = "{user_nickname1}"')
    conn.commit()
    cur.execute(f'UPDATE users SET elo = {Rb} WHERE nickname = "{user_nickname2}"')
    conn.commit()

def getTextInput():
    result1 = txt1.get()
    result2 = txt2.get()
    result3 = int(txt3.get())
    result4 = int(txt4.get())
    Data(result1,result2,result3,result4)

window = Tk()
window.title("Эло рейнтиг by PANiXiDA")
window.geometry('500x300')

lbl = Label(window, text="Игрок 1")
lbl.pack(side = LEFT)
txt1 = Entry(window, width=10)
txt1.pack(side = LEFT)
lbl = Label(window, text="vs")
lbl.pack(side = LEFT)
lbl = Label(window, text="Игрок 2")
lbl.pack(side = LEFT)
txt2 = Entry(window, width=10)
txt2.pack(side = LEFT)
lbl = Label(window, text="Счёт:")
lbl.pack(side = LEFT)
txt3 = Entry(window, width=10)
txt3.pack(side = LEFT)
lbl = Label(window, text=" : ")
lbl.pack(side = LEFT)
txt4 = Entry(window, width=10)
txt4.pack(side = LEFT)
btn = Button(window, text="Рассчитать", command=getTextInput)
btn.pack(side = LEFT)
window.mainloop()