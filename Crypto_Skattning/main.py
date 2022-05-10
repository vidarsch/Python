import csv
from datetime import datetime


def column(matrix, i):
    return [row[i] for row in matrix]


def main():

    with open('Period4.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    #INFO
    #data[i][1] = Tid               data[i][4] = valuta
    #data[i][2] = Ordertyp          data[i][5] = Mängd av valuta
    #data[i][3] = köp/sälj/fee

    first_buy = False
    store_time = 0
    buy_sell_counter = 0
    pair_buy_list = []
    pair_sell_list = []
    fees_list = {}
    currency_dict = {

    }
    sell_currency_dict = {}

    for i in range(len(data)):
        if data[i][3] == 'Buy':
            first_buy = True
        if data[i][3] == 'Buy' or data[i][3] == 'Sell':
            buy_sell_counter += 1

        if data[i][3] =='Fees':

            if x not in fees_list:
                fees_list.update({x:float(data[i][5])})
            else:
                fees_list.get({x:float(data[i][5])})

        if first_buy:
            time_seconds = (datetime.strptime(str(data[i][1]),'%Y-%m-%d %H:%M:%S')).second

            if data[i][3] == 'Buy':

                pair_buy_list.append(data[i])
                sell_currencies = []
                for x in column(pair_sell_list,4): #få en lista av nr 4 istället för en siffra
                     if x not in sell_currencies:
                        sell_currencies.append(x)

                for k in range(len(pair_sell_list)):
                    if pair_sell_list[k][4] == sell_currencies[0]:  # lägger till i dict
                        if pair_sell_list[k][4] + sell_currencies[1] not in sell_currency_dict:
                            sell_currency_dict.update({pair_sell_list[k][4] + sell_currencies[1]: pair_sell_list[k][5]})
                            #mer info här

                    if pair_sell_list[k][4] == sell_currencies[1]:  # lägger till i dict
                        if pair_sell_list[k][4] + sell_currencies[0] not in sell_currency_dict:
                            sell_currency_dict.update({pair_sell_list[k][4] + sell_currencies[0]: pair_sell_list[k][5]})


                        s_pre_val = abs(float(sell_currency_dict.get(pair_sell_list[k][4] + sell_currencies[0])))

                        if pair_sell_list[k][4] + sell_currencies[0] in sell_currency_dict:  # updaterar priset på valutan
                            #print(currency_dict.get(pair_buy_list[k][4] + currencies[0]))
                            if float(sell_currency_dict.get(pair_sell_list[k][4] + sell_currencies[0])) < 0 and float(
                                    pair_sell_list[k][5]) > 0:
                                sell_currencies[0], sell_currencies[1] = sell_currencies[1], sell_currencies[0]
                                print("YUP SWAP TIME")

                            sell_currency_dict.update({pair_sell_list[k][4] + sell_currencies[0]:
                                float(sell_currency_dict.get(pair_sell_list[k][4] + sell_currencies[0])) +
                                float(pair_sell_list[k][5])
                                                 })

                        if pair_sell_list[k][4] + sell_currencies[1] in sell_currency_dict:  #updatera värden
                            sell_currency_dict.update({pair_sell_list[k][4] + sell_currencies[1]:
                                float(sell_currency_dict.get(pair_sell_list[k][4] + sell_currencies[1])) +
                                float(pair_sell_list[k][5])
                                                 })
                        s_curr_val = abs(float(sell_currency_dict.get(pair_sell_list[k][4] + sell_currencies[0])))

                        if s_curr_val<s_pre_val:
                            print("Hmmmmmm ???????")
                pair_sell_list = []


            if data[i][3] == 'Sell': #----------------------------------------------------------------
                currencies = []
                pair_sell_list.append(data[i])

                for x in column(pair_buy_list,4): #få en lista av nr 4 istället för en siffra
                     if x not in currencies:
                        currencies.append(x)

                if len(currencies)==1:
                    currencies.append('-')
                    print(i)
                    raise Exception

                for k in range(len(pair_buy_list)):
                    if pair_buy_list[k][4] == currencies[0]: #lägger till i dict
                        if pair_buy_list[k][4] + currencies[1] not in currency_dict:
                            currency_dict.update({pair_buy_list[k][4] + currencies[1]: pair_buy_list[k][5]})
                            #mer info här

                    if pair_buy_list[k][4] == currencies[1]: #lägger till i dict
                        if pair_buy_list[k][4] + currencies[0] not in currency_dict:
                            currency_dict.update({pair_buy_list[k][4] + currencies[0]: pair_buy_list[k][5]})


                        pre_val = abs(float(currency_dict.get(pair_buy_list[k][4] + currencies[0])))

                        if pair_buy_list[k][4] + currencies[0] in currency_dict: # updaterar priset på valutan
                            #print(currency_dict.get(pair_buy_list[k][4] + currencies[0]))
                            if float(currency_dict.get(pair_buy_list[k][4] + currencies[0])) < 0 and float(
                                    pair_buy_list[k][5]) > 0:
                                currencies[0], currencies[1] = currencies[1], currencies[0]
                                print("YUP SWAP TIME")

                            currency_dict.update({pair_buy_list[k][4] + currencies[0]:
                                float(currency_dict.get(pair_buy_list[k][4] + currencies[0])) +
                                float(pair_buy_list[k][5])
                                                 })


                        if pair_buy_list[k][4] + currencies[1] in currency_dict: #updatera värden
                            currency_dict.update({pair_buy_list[k][4] + currencies[1]:
                                float(currency_dict.get(pair_buy_list[k][4] + currencies[1])) +
                                float(pair_buy_list[k][5])
                                                 })
                        curr_val = abs(float(currency_dict.get(pair_buy_list[k][4] + currencies[0])))

                        if curr_val<pre_val:
                            print("Hmmmmmm ???????")

                pair_buy_list = []
                #print(currencies)
                #print(currency_dict)

    Kop_Dollares = sum([abs(float(v)) for k, v in currency_dict.items() if 'USDT' in k[0:6]])
    Sell_Dollares = sum([abs(float(v)) for k, v in sell_currency_dict.items() if 'USDT' in k[0:6]])
    print(Kop_Dollares)
    print(Sell_Dollares - Kop_Dollares)
    print(currency_dict)
    print(sell_currency_dict)
    print(buy_sell_counter)


if __name__ == '__main__':
    main()
