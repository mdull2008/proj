import os

from atm_machine import ATMmachine
from bank import Bank


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    data = os.path.join(base, "data")

    bank1 = Bank(os.path.join(data, "bank1.json"))
    bank2 = Bank(os.path.join(data, "bank2.json"))
    bank3 = Bank(os.path.join(data, "bank3.json"))

    banks = [bank1, bank2, bank3]
    atm = ATMmachine(bank1.bank_id, 200000, 50000, banks)

    print("Банкомат", atm.bank_id)
    while atm.start_session():
        pass
    print("Банкомат выключен")


if __name__ == "__main__":
    main()
