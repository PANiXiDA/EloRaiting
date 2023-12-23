import sqlite3

class Settings:
    def Data(self, x, y, a, b):
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

        Ea = 1/(1+10**((Rb - Ra)/400))
        Eb = 1 / (1 + 10 ** ((Ra - Rb) / 400))
        if Ka > 0:
            Ra = int(Ra + 16 * (Ka - Ea))
        else:
            Ra = int(Ra + 16 * (Ka + Ea))
        if Kb > 0:
            Rb = int(Rb + 16*(Kb - Eb))
        else:
            Rb = int(Rb + 16 * (Kb + Eb))
        print(Ra,Rb)

        cur.execute(f'UPDATE users SET elo = {Ra} WHERE nickname = "{user_nickname1}"')
        conn.commit()
        cur.execute(f'UPDATE users SET elo = {Rb} WHERE nickname = "{user_nickname2}"')
        conn.commit()