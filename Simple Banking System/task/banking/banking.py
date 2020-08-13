import random
import sqlite3

conn = sqlite3.connect('card.s3db')
conn.row_factory = sqlite3.Row


def create_table():
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS `card` (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    number TEXT, 
    pin TEXT, 
    balance INTEGER DEFAULT 0);
    """)
    conn.commit()


def add_user(card_number, pin):
    cur = conn.cursor()
    cur.execute(f"INSERT INTO `card` (number, pin) VALUES (\"{card_number}\", \"{pin}\");")
    conn.commit()


def get_user(card_number):
    cur = conn.cursor()
    cur.execute(f"SELECT `id`, `number` as `card_number`, `pin`, `balance` FROM `card` WHERE `card_number` = \"{card_number}\"")
    return cur.fetchone()


def auth_user(card_number, pin):
    user = get_user(card_number)
    return user and user['pin'] == pin


def create_check_sum(row_card_number):
    card_digits = [int(d) for d in row_card_number]
    for i in range(0, len(card_digits), 2):
        result = card_digits[i] * 2
        card_digits[i] = result - 9 if result > 9 else result
    sum_of_digits = sum(card_digits)
    check_sum = 0
    while True:
        if (sum_of_digits + check_sum) % 10 == 0:
            break
        else:
            check_sum += 1

    return check_sum


def create_a_card_number():
    mii_bin = "400000"
    account_identifier = str(random.randint(1, 999999999)).zfill(9)
    check_sum = create_check_sum(mii_bin + account_identifier)
    return mii_bin + account_identifier + str(check_sum)


def create_a_pin():
    return str(random.randint(0, 9999)).zfill(4)


def create_an_account():
    while True:
        card_number = create_a_card_number()
        if not get_user(card_number):
            break
    pin = create_a_pin()
    add_user(card_number, pin)

    print("")
    print("Your card has been created")
    print("Your card number:")
    print(card_number)
    print("Your card PIN:")
    print(pin)
    print("")


def check_balance(user):
    user = get_user(user['card_number'])
    print(user['balance'])


def add_income(user, income):
    cur = conn.cursor()
    cur.execute(f"UPDATE `card` SET `balance` = `balance` + {income} WHERE `id` = {user['id']}")
    conn.commit()
    print("Income was added!")


def do_transfer(user):
    print("Transfer")
    print("Enter card number:")
    destination_card_number = input()

    if create_check_sum(destination_card_number[:-1]) != int(destination_card_number[-1:]):
        print("Probably you made mistake in the card number. Please try again!")
        return False

    if destination_card_number == user['card_number']:
        print("You can't transfer money to the same account!")
        return False

    destination_user = get_user(destination_card_number)

    if not destination_user:
        print("Such a card does not exist.")
        return False

    print("Enter how much money you want to transfer:")
    transfer_amount = int(input())

    if transfer_amount > user['balance']:
        print("Not enough money!")
        return False

    add_income(destination_user, transfer_amount)
    add_income(user, -transfer_amount)
    print("Success!")
    return True


def close_account(user):
    cur = conn.cursor()
    cur.execute(f"DELETE FROM `card` WHERE `id` = {user['id']}")
    conn.commit()
    print("The account has been closed!")


def print_user_menu(user):
    print("1. Balance")
    print("2. Add income")
    print("3. Do transfer")
    print("4. Close account")
    print("5. Log out")
    print("0. Exit")

    choice = int(input())

    print("")
    if choice == 1:
        check_balance(user)
    elif choice == 2:
        print("Enter income:")
        add_income(user, int(input()))
    elif choice == 3:
        do_transfer(user)
    elif choice == 4:
        close_account(user)
    elif choice == 5:
        print("You have successfully logged out!")
        print("")
        return False
    else:
        return -1
    print("")
    return True


def log_into_account():
    print("Enter your card number:")
    card_number = input()
    print("Enter your PIN:")
    pin = input()

    if auth_user(card_number, pin):
        print("")
        print("You have successfully logged in!")
        print("")
        while True:
            result = print_user_menu(get_user(card_number))
            if result == -1:
                return None
            if not result:
                break
    else:
        print("")
        print("Wrong card number or PIN!")
        print("")

    return True


def print_main_menu():
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")

    choice = int(input())

    if choice == 1:
        create_an_account()
    elif choice == 2:
        result = log_into_account()
        if result is None:
            return False
    else:
        print("Bye!")
        return False
    return True


# Runtime
create_table()

while True:
    if not print_main_menu():
        break
