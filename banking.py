import random
cards = {}


def create_card():
    account = random.randint(100000000, 999999999)
    card_number = f'400000{account}1'
    card_pin = random.randint(1000, 9999)
    # card = card_number, card_pin
    cards[card_number] = card_pin
    # print(cards)
    print('Your card has been created')
    print(f'Your card number:\n{card_number}')
    print(f'Your card pin:\n{card_pin}')


def check_card():
    card_number = str(input('Enter your card number:'))
    card_pin = int(input('Enter your PIN:'))
    if card_number in cards.keys():
        # print('right card')
        if cards[str(card_number)] == card_pin:
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
