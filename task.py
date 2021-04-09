
import random

class Client:
  def __init__(self, name, money):
    self.name = name
    self.money = money

class Bank:
  def __init__(self, name):
    self.name = name

  clients_list = []

  def add_client(self, client):
    client_account_num = random.randint(100000000000, 999999999999)
    print('add the amount of money you want to store')
    money_stored = input()
    if int(money_stored) > client.money:
      not_enough_money ='client does not have enough money'
      return print(not_enough_money)
    else:
      self.clients_list.append([client.name, client_account_num, money_stored])




if __name__ == '__main__':
  bank1 = Bank('bank1')
  print(bank1.name)

  client1 = Client('pawel jaros', 1000)
  print(client1.name)

  bank1.add_client(client1)
  print(bank1.clients_list)