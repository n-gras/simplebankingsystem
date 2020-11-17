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


def luhn_compare(number, checksum):
    return int(luhn(number)) == int(checksum)


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


def check_account(card_nr):
    c.execute("SELECT id FROM card WHERE number = (?)", (card_nr,))
    acc = c.fetchone()
    if acc:
        return acc[0]
    return False


def balance(account):
    c.execute("SELECT balance FROM card WHERE id = (?)", (account,))
    amount = c.fetchone()[0]
    return amount


def add_income(account):
    money = int(input('Enter income:'))
    try:
        c.execute("UPDATE card SET balance = balance + (?) WHERE id = (?)", (money, account))
        conn.commit()
        print('Income was added!')
    except sqlite3.Error as error:
        print('Failed to update the balance', error)


def transfer(from_account, to_account):
    trans_money = int(input('Enter how much money you want to transfer:'))
    if trans_money < balance(from_account):
        try:
            c.execute("UPDATE card SET balance = balance - (?) WHERE id = (?)", (trans_money, from_account))
            c.execute("UPDATE card SET balance = balance + (?) WHERE id = (?)", (trans_money, to_account))
            conn.commit()
            print('Success!')
        except sqlite3.Error as error:
            print('Failed to transfer the money', error)
    else:
        print('Not enough money!')


def delete_account(account):
    try:
        c.execute("DELETE FROM card WHERE id = (?)", (account,))
        conn.commit()
        print('Account closed!')
    except sqlite3.Error as error:
        print('Failed to delete the account', error)


def login(account):
    if not account:
        return True
    else:
        print('\nYou have successfully logged in!')
        while True:
            print('1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit')
            choic = input()
            if choic == '1':
                print(f'Your balance is:\n{balance(account)}\n')
            elif choic == '2':
                add_income(account)
            elif choic == '3':
                print('Transfer')
                to_acc = input('Enter card number:')
                if check_account(to_acc):
                    transfer(account, check_account(to_acc))
                else:
                    if luhn_compare(to_acc[:-1], to_acc[-1]):
                        print('Such a card does not exist.')
                    else:
                        print('Probably you made a mistake in the card number. Please try again!')

            elif choic == '4':
                delete_account(account)
                return True
            elif choic == '5':
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
            if login(check_card()):
                continue
            else:
                stop()
                break
        elif choice == '0':
            stop()
            break


if __name__ == '__main__':
    main_menu()
