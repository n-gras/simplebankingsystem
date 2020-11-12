import random
cards = {}

def luhn(number):
    num = 0
    for n in range(15):
        if (n + 1) % 2:
            num += (int(number[n]) * 2) - 9 if int(number[n]) * 2 > 9 else int(number[n]) * 2
            print(num)
        else:
            num += int(number[n])
            print(num)

    for n in range(10):
        if (num + n) % 10 == 0:
            return n


def create_card():
    bin = '400000'
    account = str(random.randint(0, 999999999)).rjust(9, '0')
    checksum = luhn(f'{bin}{account}')
    card_number = f'{bin}{account}{checksum}'
    card_pin = str(random.randint(0, 9999)).rjust(4, '0')
    # card = card_number, card_pin
    cards[card_number] = card_pin
    # print(cards)
    print('Your card has been created')
    print(f'Your card number:\n{card_number}')
    print(f'Your card pin:\n{card_pin}')


def check_card():
    card_number = str(input('Enter your card number:'))
    card_pin = str(input('Enter your PIN:'))
    if card_number in cards.keys():
        # print('right card')
        if cards[card_number] == card_pin:
            # print('right pin')
            return True
    return False


def balance():
    print('\nBalance: 0')


def login():
    print('\nYou have successfully logged in!')
    while True:
        print('1. Balance\n2. Log out\n0. Exit')
        choic = input()
        if choic == '1':
            balance()
        elif choic == '2':
            print('You have successfully logged out!')
            return True
        elif choic == '0':
            print('Bye!')
            return False


def main_menu():
    while True:
        print('\n1. Create an account\n2. Log into account\n0. Exit')
        choice = input()
        if choice == '1':
            create_card()
            continue
        elif choice == '2':
            if check_card() is True:
                loggedin = login()
                if loggedin:
                    continue
                else:
                    break
            else:
                print('Wrong card number or PIN!')
                continue
        elif choice == '0':
            print('Bye!')
            break


if __name__ == '__main__':
    main_menu()
