import uuid
from dataclasses import dataclass
from multiprocessing import Process


class Client:

    def __init__(self, name, money, client_accounts=[]):
        self.name = name
        self.money = money
        self.client_accounts = client_accounts
        self._email = ''

    def money_left(self, money_stored):
        self.money -= money_stored

    def money_after_withdraw(self, money_withdrawn):
        self.money += money_withdrawn

    def add_new_bank_acc(self, account):
        self.client_accounts.append(
            [account.bank, account.acc_num, account.funds])

    @property
    def email(self):
        first, last = self.name.split(" ")
        self._email = '{}.{}@gmail.com'.format(first, last)
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @staticmethod
    def is_email_valid(email):
        if '@' in email:
            return True
        else:
            return False

    @classmethod
    def client_name(cls, name, money, client_accounts):
        client = cls(name, money, client_accounts)
        return client


@dataclass
class Account:
    bank: str
    acc_num: int
    owner: str
    funds: float


class Bank:
    def __init__(self, name, accounts_list=[]):
        self.name = name
        self.accounts_list = accounts_list

    def add_client(self, client, is_deal_on):
        client_account_num = uuid.uuid4().int & (1 << 51)-1
        initial_funds = 0
        if is_deal_on:
            initial_funds = 100
        account = Account(self.name, client_account_num,
                          client.name, initial_funds)
        self.accounts_list.append(account)
        client.add_new_bank_acc(account)

    def deposit_money(self, client, money_to_store):
        if money_to_store <= client.money:
            for account in self.accounts_list:
                for clients_acc in client.client_accounts:
                    if clients_acc[1] == account.acc_num:
                        account.funds += money_to_store
                        clients_acc[2] += money_to_store
                        client.money_left(money_to_store)

    def withdraw(self, client, money_to_withdraw):
        for account in self.accounts_list:
            for clients_acc in client.client_accounts:
                if clients_acc[1] == account.acc_num:
                    if clients_acc[2] >= money_to_withdraw:
                        account.funds -= money_to_withdraw
                        clients_acc[2] -= money_to_withdraw
                        client.money_after_withdraw(money_to_withdraw)

    def transfer(self, clientA, clientB, bankB, money_to_transfer):
        for account in self.accounts_list:
            for clients_acc in clientA.client_accounts:
                if clients_acc[1] == account.acc_num:
                    if clients_acc[2] >= money_to_transfer:
                        account.funds -= money_to_transfer
                        clients_acc[2] -= money_to_transfer
        for account in bankB.accounts_list:
            for clients_acc in clientB.client_accounts:
                if clients_acc[1] == account.acc_num:
                    account.funds += money_to_transfer
                    clients_acc[2] += money_to_transfer

    def credit(self, client, money):
        for account in self.accounts_list:
            for clients_acc in client.client_accounts:
                if clients_acc[1] == account.acc_num:
                    account.funds += money
                    clients_acc[2] += money
                    client.money_left(money)

    def delete_acc(self, client):
        for account in self.accounts_list:
            for clients_acc in client.client_accounts:
                if clients_acc[1] == account.acc_num:
                    client.client_accounts.remove(clients_acc)
                    self.accounts_list.remove(account)

    def change_bank(self, client, bank):
        for account in self.accounts_list:
            for clients_acc in client.client_accounts:
                if clients_acc[1] == account.acc_num:
                    money = account.funds
                    self.delete_acc(client)
                    bank.add_client(client, False)
                    bank.deposit_money(client, money)


if __name__ == '__main__':

    bank1 = Bank('bank1', [])
    bank2 = Bank('bank2', [])
    bank3 = Bank('bank3', [])

    client1 = Client('pawel jaros', 10000, [])
    client2 = Client('marak gajos', 20000, [])
    client3 = Client('xxx yyy', 18500, [])
    client4 = Client('test test', 18800, [])
    client5 = Client('andrzej jaros', 20000, [])
    client6 = Client('czasna hiszpanski', 11000, [])
    client7 = Client('szklanka wody', 8000, [])
    client8 = Client('pawel pawel', 10800, [])
    client9 = Client('jaroslaw mak', 5000, [])
    client10 = Client('bohdan tom', 9000, [])
    client11 = Client('igor dziewa', 10010, [])
    client12 = Client('krzysztof duleba', 10300, [])

    bank1.add_client(client1, True)
    p1 = Process(target=bank1.deposit_money, args=[client1, 2500])
    p1.run()
    p1.start()

    bank1.add_client(client2, False)
    p2 = Process(target=bank1.deposit_money, args=[client2, 2500])
    p2.run()
    p2.start()

    bank1.add_client(client3, False)
    p3 = Process(target=bank1.deposit_money, args=[client3, 2500])
    p3.run()
    p3.start()

    bank1.add_client(client4, True)
    p4 = Process(target=bank1.deposit_money, args=[client4, 2500])
    p4.run()
    p4.start()

    bank2.add_client(client5, False)
    p5 = Process(target=bank2.deposit_money, args=[client5, 2500])
    p5.run()
    p5.start()

    bank2.add_client(client6, False)
    p6 = Process(target=bank2.deposit_money, args=[client6, 2500])
    p6.run()
    p6.start()

    bank2.add_client(client7, True)
    p7 = Process(target=bank2.deposit_money, args=[client7, 2500])
    p7.run()
    p7.start()

    bank2.add_client(client8, False)
    p8 = Process(target=bank2.deposit_money, args=[client8, 2500])
    p8.run()
    p8.start()

    bank3.add_client(client9, False)
    p9 = Process(target=bank3.deposit_money, args=[client9, 2500])
    p9.run()
    p9.start()

    bank3.add_client(client10, True)
    p10 = Process(target=bank3.deposit_money, args=[client10, 2500])
    p10.run()
    p10.start()

    bank3.add_client(client11, False)
    p11 = Process(target=bank3.deposit_money, args=[client11, 2500])
    p11.run()
    p11.start()

    bank3.add_client(client12, False)
    p12 = Process(target=bank3.deposit_money, args=[client12, 2500])
    p12.run()
    p12.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()
    p7.join()
    p8.join()
    p9.join()
    p10.join()
    p11.join()
    p12.join()

    print("bank1 account list: \n", bank1.accounts_list, '\n')

    bank1.transfer(client1, client2, bank1, 500)
    bank1.transfer(client2, client5, bank2, 500)
    bank1.transfer(client3, client7, bank2, 500)
    bank1.transfer(client4, client8, bank2, 500)
    bank2.transfer(client5, client11, bank3, 500)
    bank2.transfer(client6, client12, bank3, 500)
    bank2.transfer(client7, client12, bank3, 500)
    bank2.transfer(client8, client2, bank1, 500)
    bank3.transfer(client9, client1, bank1, 500)
    bank3.transfer(client10, client7, bank2, 500)
    bank3.transfer(client11, client6, bank2, 500)
    bank3.transfer(client12, client2, bank1, 500)
    bank1.transfer(client1, client2, bank1, 500)
    bank1.transfer(client2, client2, bank1, 500)
    bank1.transfer(client3, client2, bank1, 500)
    bank1.transfer(client4, client2, bank1, 500)

    print("bank1 account list after 16 transactions: \n", bank1.accounts_list, '\n')
    print('#########################')
    print("client1 money not stored: ", client1.money)
    bank1.withdraw(client1, 1000)
    print("client1 money not stored after withdrawal: ", client1.money)
    print('######################### \n')
    print("bank1 account list: \n", bank1.accounts_list, '\n')
    print("bank2 account list: \n", bank2.accounts_list)
    print(' ')
    bank1.change_bank(client1, bank2)
    print("bank1 account list after account transfer: \n", bank1.accounts_list, '\n')
    print("bank2 account list after account transfer: \n", bank2.accounts_list, '\n')
    
    client1._email = "asdasdasdas@gmail.com"
    print('inserted email: ', client1._email)
    print('static method is_email_valid: ', Client.is_email_valid(client1._email))