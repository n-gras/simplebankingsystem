import random
import sqlite3

conn = sqlite3.connect('card.s3db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS card (
                            id INTEGER PRIMARY KEY,
                            number TEXT,
                            pin TEXT,
                            balance INTEGER DEFAULT 0)''')
conn.commit()


def luhn(number):
    num = 0
    for n in range(len(number)):
        if (n + 1) % 2:
            num += (int(number[n]) * 2) - 9 if int(number[n]) * 2 > 9 else int(number[n]) * 2
        else:
            num += int(number[n])

    for n in range(10):
        if (num + n) % 10 == 0:
            return n


def create_card():
    bin = '400000'
    while True:
        account = str(random.randint(0, 999999999)).rjust(9, '0')
        checksum = luhn(f'{bin}{account}')
        card_number = f'{bin}{account}{checksum}'
        card_pin = str(random.randint(0, 9999)).rjust(4, '0')
        try:
            c.execute("INSERT INTO card VALUES (?, ?, ?, ?)", (account, card_number, card_pin, 0))
        except sqlite3.IntegrityError:
            continue
        break

    conn.commit()
    print('Your card has been created')
    print(f'Your card number:\n{card_number}')
    print(f'Your card pin:\n{card_pin}')


def check_card():
    card_number = str(input('Enter your card number:'))
    card_pin = str(input('Enter your PIN:'))
    c.execute("SELECT id FROM card WHERE number = (?) AND pin = (?)", (card_number, card_pin))
    account = c.fetchone()
    if account:
        return account[0]
    print('Wrong card number or PIN!')
    return False


def balance(account):
    c.execute("SELECT balance FROM card WHERE id = (?)", (account,))
    amount = c.fetchone()[0]
    print(f'Your balance is:\n{amount}\n')


def login(account):
    if not account:
        return True

    else:
        print('\nYou have successfully logged in!')
        while True:
            print('1. Balance\n2. Log out\n0. Exit')
            choic = input()
            if choic == '1':
                balance(account)
            elif choic == '2':
                print('You have successfully logged out!')
                return True
            elif choic == '0':
                return False


def stop():
    conn.close()
    print('Bye!')


def main_menu():
    while True:
        print('\n1. Create an account\n2. Log into account\n0. Exit')
        choice = input()
        if choice == '1':
            create_card()
            continue
        elif choice == '2':
            loggedin = login(check_card())
            if loggedin:
                continue
            else:
                stop()
                break
        elif choice == '0':
            stop()
            break


if __name__ == '__main__':
    main_menu()
