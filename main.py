from tinkoff.invest import Client
from datetime import datetime

# класс для денег
class Money:
    def __int__(self, unit, fractional, currency):
        self.unit = unit
        self.fractional = fractional // 10000000
        self.currency = currency
        self.numeration = 100
        self.value = unit * 100 + fractional

    def __str__(self):
        return f'{self.unit} руб. {self.fractional} коп.'

    def __mul__(self, other):
        return self.value * other

# метод для получения купонов

def getcoupons(bonds):
    bonds_coupons = []
    for bond in bonds:
        coupons = Client.instruments.get_bond_coupons(figi=bond['figi']).events

# вытаскиваем даты и размеры выплат из ответа тинька

        bond['coupons'] = {'date': [], 'pay_one_bond': []}
        bond['coupons']['date'].extend([coupon.coupon_date for coupon in coupons])
        moneys = [coupon.pay_one_bond for coupon in coupons]
        print(moneys[0].units, moneys[1].nano, moneys[2].currency)
        example = Money(33, 100, 'rub')
        print(example)
        moneys_new = [Money(coupon.units, coupon.nano, coupon.currency) for coupon in moneys]
        print(moneys_new)
#        bond['coupons']['pay_one_bond'].extend([coupon.pay_one_bond for coupon in coupons])
#        bonds_coupons.append({'isin': bond['instrument_isin'], 'quantity': bond['quantity'],
       #                       'coupons': zip(bond['coupons']['date'], bond['coupons']['pay_one_bond'])})
    middle = []

# приводим в удобный вид для дальнейшей работы с данными

    for bond in bonds_coupons:
         for idx, coupon in enumerate(bond['coupons']):
             middle.append((coupon[0], coupon[1] * bond['quantity']))
         bond['coupons'] = middle.copy()
         middle.clear()
    print(bonds_coupons)
    return bonds_coupons


with open('Token.txt') as f:
    TOKEN = f.read()

with open('BCS_acc.txt') as f:
    bcs_poz = f.readlines()

# Конструкция для формирования списка ценных бумаг из портфеля

with Client(TOKEN) as Client:
    accounts = Client.users.get_accounts().accounts
    for account in accounts:
        if account.name == 'ИИС':
            id_acc = account.id
    positions = Client.operations.get_positions(account_id=id_acc).securities
    poz_list = []

# перебор позиций и выделение интересующих нас данных из ответа тинька

    for position in positions:
        poz_list.append({'instrument_uid': position.instrument_uid,
                    'instrument_type': position.instrument_type,
                    'quantity': position.balance,
                    'figi': position.figi})
    positions.clear()
    positions_dict = {'bond': [], 'etf': [], 'share': []}

#разделение бумаг по типу: облигации, акции, паи

    for position in poz_list:
        instr_ts = Client.instruments.find_instrument(query=position['instrument_uid']).instruments
        position['instrument_isin'] = instr_ts[0].isin
        if position['instrument_type'] == 'bond':
            positions_dict['bond'].append(position)
        elif position['instrument_type'] == 'share':
            positions_dict['share'].append(position)
        elif position['instrument_type'] == 'etf':
            positions_dict['etf'].append(position)
    bonds = getcoupons(positions_dict['bond'])
#print(positions_dict)


