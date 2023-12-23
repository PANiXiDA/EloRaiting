from tkinter import *
import sqlite3
import os

def CalculationEloInBase(x, y, a, b):#x - игрок 1, y - игрок 2, a - счет первого, b - счет второго
    Ka = a - b; #коэфф первого игрока
    Kb = b - a; #коэфф второго игрока
    Ra = '' #рейтинг первого
    Rb = '' #рейтинг второго

    conn = sqlite3.connect('orders.db') #присоединение к таблице
    cur = conn.cursor() #создание курсора, с помощью которого мы передвигаемся по таблице

    cur.execute("""CREATE TABLE IF NOT EXISTS users(
       nickname TEXT,
       elo BIGINT
    )""")#если таблицы не существует, то создаем ее, где у нас будет 1 переменная ник игрока, вторая его эло рейтинг
    conn.commit()#сохранение измененных данных

    user_nickname1 = x #переименовываем никнейм первого игрока
    '''for value in cur.execute("SELECT * FROM users"):
        print(value)'''#вывод всей таблицы базы данных, цикл выбираем всё в таблице юзерс

    cur.execute('''SELECT nickname FROM users WHERE nickname = ?''', (user_nickname1,))#ищем никнейм игрока 1 в таблице
    if cur.fetchone() is None:#если не нашлось такого игрока, то добавляем его в таблицу
        cur.execute(f"INSERT INTO users VALUES (?, ?)", (user_nickname1, 1000))#ник игрока и его базовый эло рейтинг = 1000
        conn.commit()
        Ra = 1000
    else:
        cur.execute('''SELECT elo FROM users WHERE nickname = ?''', (user_nickname1,))#если игрок есть, то дальше ищем его эло рейтинг
        s = cur.fetchone()
        Ra = int(s[0])

    #всё аналогично для второго игрока
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
    print("Старый эло рейтинг " + x + " = " + str(Ra))
    print("Старый эло рейтинг " + y + " = " + str(Rb))
    per1 = Ra #старый эло игрока a
    per2 = Rb #старый эло игрока b
    #дальше формула подсчета эло рейтинга
    Ea = 1 / (1 + 10 ** ((Rb - Ra) / 400))
    Eb = 1 / (1 + 10 ** ((Ra - Rb) / 400))
    if (Ka>0):
        Ra = int(Ra + 16 * (1 - Ea)*Ka)+1
        Rb = Rb - (Ra - per1)
    else:
        Rb = int(Rb + 16 * (1 - Eb)*Kb)+1
        Ra = Ra - (Rb - per2)
    print("Новый эло рейтинг " + x + " = " + str(Ra) + " Изменение: " + str(Ra-per1))
    print("Новый эло рейтинг " + y + " = " + str(Rb) + " Изменение: " + str(Rb-per2))

    cur.execute(f'UPDATE users SET elo = {Ra} WHERE nickname = "{user_nickname1}"')#обновляем эло рейтинг 1-го игрока
    conn.commit()
    cur.execute(f'UPDATE users SET elo = {Rb} WHERE nickname = "{user_nickname2}"')#обновляем эло рейтинг 2-го игрока
    conn.commit()

def CalculationElo():
    os.system('CLS')
    result1 = txt1.get()
    result2 = txt2.get()
    result3 = txt3.get()
    result4 = txt4.get()
    if (len(result1)!=0 and len(result2)!=0 and len(result3)!=0 and len(result4)!=0):
        if (result3.isdigit() and result4.isdigit()):
            result3 = int(result3)
            result4 = int(result4)
            CalculationEloInBase(result1,result2,result3,result4)
        else:
            print("Введите корректное значение счёта!")
    else:
        print("Заполните все поля!")

def CheckEloInBase(x):
    conn = sqlite3.connect('orders.db')
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users(
       nickname TEXT,
       elo BIGINT
    )""")
    conn.commit()

    user_nickname1 = x

    cur.execute('''SELECT nickname FROM users WHERE nickname = ?''', (user_nickname1,))
    if cur.fetchone() is None:
        print('Игрок не зарегистрирован в базе данных, вам нужно провести с кем-то игру в рамках турнира')
    else:
        cur.execute('''SELECT elo FROM users WHERE nickname = ?''', (user_nickname1,))
        s = cur.fetchone()
        elo = s[0]
        print("Эло рейтинг " + x + " = " + str(elo))

def ShowRaiting():
    os.system('CLS')
    conn = sqlite3.connect('orders.db')
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users(
       nickname TEXT,
       elo BIGINT
    )""")
    conn.commit()

    for value in cur.execute("SELECT * FROM users ORDER BY elo DESC"):
        print(value)

def DeletePlayerInBase(x):
    conn = sqlite3.connect('orders.db')
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users(
       nickname TEXT,
       elo BIGINT
    )""")
    conn.commit()

    user_nickname = x

    cur.execute('''SELECT nickname FROM users WHERE nickname = ?''', (user_nickname,))
    if cur.fetchone() is None:
        print("Такого игрока не существует!")
    else:
        cur.execute('''DELETE from users WHERE nickname = ?''', (user_nickname,))
        conn.commit()
        print("Успешно удалено!")

def DeleteAll():
    os.system('CLS')
    conn = sqlite3.connect('orders.db')
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users(
       nickname TEXT,
       elo BIGINT
    )""")
    conn.commit()

    cur.execute('DELETE from users;',)
    conn.commit()

def CheckElo():
    os.system('CLS')
    result5 = txt5.get()
    if (len(result5) != 0):
        CheckEloInBase(result5)
    else:
        print("Заполните поле!")

def DeletePlayer():
    os.system('CLS')
    result6 = txt6.get()
    if (len(result6) != 0):
        DeletePlayerInBase(result6)
    else:
        print("Заполните поле!")

window = Tk()
window.title("Эло рейнтиг by PANiXiDA")
window.geometry('600x300')

lbl = Label(window, text="Игрок 1    ")
lbl.grid(row=0, column=0)
txt1 = Entry(window, width=10)
txt1.grid(row=0, column=1)
lbl = Label(window, text="vs")
lbl.grid(row=0, column=2)
lbl = Label(window, text="Игрок 2")
lbl.grid(row=0, column=3)
txt2 = Entry(window, width=10)
txt2.grid(row=0, column=4)
lbl = Label(window, text="Счёт:")
lbl.grid(row=0, column=5)
txt3 = Entry(window, width=10)
txt3.grid(row=0, column=6)
lbl = Label(window, text=" : ")
lbl.grid(row=0, column=7)
txt4 = Entry(window, width=10)
txt4.grid(row=0, column=8)
btn = Button(window, text="   Рассчитать    ", command=CalculationElo)
btn.grid(row=0, column=9)

lbl = Label(window, text="Вывести   ")
lbl.grid(row=1, column=0)
lbl = Label(window, text="рейтинг")
lbl.grid(row=1, column=1)
lbl = Label(window, text="игроков")
lbl.grid(row=1, column=2)
btn = Button(window, text="      Рейтинг       ",command=ShowRaiting)
btn.grid(row=1, column=9)

lbl = Label(window, text="Игрок:      ")
lbl.grid(row=2, column=0)
txt5 = Entry(window, width=10)
txt5.grid(row=2, column=1)
btn = Button(window, text="Проверить эло",command=CheckElo)
btn.grid(row=2, column=9)

lbl = Label(window, text="Удалить   ")
lbl.grid(row=3, column=0)
lbl = Label(window, text="игрока")
lbl.grid(row=3, column=1)
txt6 = Entry(window, width=10)
txt6.grid(row=3, column=2)
btn = Button(window, text="       Удалить      ",command=DeletePlayer)
btn.grid(row=3, column=9)

lbl = Label(window, text="Отчистить")
lbl.grid(row=4, column=0)
lbl = Label(window, text="таблицу")
lbl.grid(row=4, column=1)
btn = Button(window, text="      Очистить    ",command=DeleteAll)
btn.grid(row=4, column=9)

window.mainloop()