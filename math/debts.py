# encoding: utf-8


m = 1000000
i = 1000
r = 0.05    # 年利息
mr = r / 12 # 平均月利息

def pay_debt(loan, rate, pay):
    i = 1
    mr = rate / 12
    amount = loan
    while loan >= pay:
        amount += loan * mr
        loan = loan * (1 + mr) - pay
        i += 1
    print(amount, loan)
    return i


def p(amount, interest, year):
    n = year * 12
    month_pay = amount * (interest - 1) / (interest ** n - 1)
    return month_pay


print(pay_debt(1000000, 0.05, 10000))
print(p(100000, 0.05, 10))
