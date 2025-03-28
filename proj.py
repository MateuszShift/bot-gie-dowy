import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

link = "/Users/macmat/Downloads/META.csv"
data = pd.read_csv(link, sep=';')
dataset = data.to_numpy() #dane kolejno: Date,Open,High,Low,Close,Adj Close,Volume 
money = 1000.0

def EMA(data,span): 
    alpha = 2 / (span+1) #wspołczynnik wygladzania
    ema = [data[0]]
    for i in range(1, len(data)):
        ema.append(alpha * data[i] + (1 - alpha) * ema[i - 1])
    return ema

def MACD(data):
    EMA_12 = np.array(EMA(np.array(data)[:,4],12)) #obliczanie wartosci EMA dla 12 dni z danych zamykajacych
    EMA_26 = np.array(EMA(np.array(data)[:,4],26))
    
    dataset_macd_signal = np.zeros((len(data),2))
    dataset_macd_signal[:,0] = EMA_12 - EMA_26
    dataset_macd_signal[:,1] = np.array(EMA(dataset_macd_signal[:,0],9))
    return dataset_macd_signal
    
dataset_macd_signal = MACD(dataset)

#graf FACEBOOK stock
date = pd.to_datetime(dataset[:,0])
plt.figure(figsize=(10,6))
plt.plot(date,dataset[:,4], marker='', linestyle='-', color='b')
plt.title('Notowania Facebook')
plt.xlabel('Data')
plt.ylabel('Cena zamknięcia')
plt.grid(True)
plt.show()


# TODO: wykres MACD i Signal

plt.figure(figsize=(10,6))
plt.plot(date,dataset_macd_signal[:,0],marker='',linestyle='-', color='green')
plt.plot(date,dataset_macd_signal[:,1],marker='',linestyle='-', color='yellow')
plt.title('Wykres MACD i sygnału MACD')
plt.xlabel('Data')
plt.ylabel('Wartość')
plt.legend()
plt.grid(True)
plt.show()

# TODO: wykres MACD i SINGAL z kupnem i sprzedazą (tutaj dopytac sie jeszcze ale chyba 3 i 4 podpunkt są sobie rowne albo bardzo podobne)

decision_buy = np.ones_like(dataset[:,4])
decision_sell = np.ones_like(dataset[:,4])
bank_balance = []
stocks = 0
decision_buy[0] = None
decision_sell[0] = None
bank_balance.append(money+stocks*dataset[0,4])
for i in range(1, len(dataset_macd_signal)):
    decision_buy[i] = None
    decision_sell[i] = None
    if dataset_macd_signal[i-1, 0] < dataset_macd_signal[i-1, 1] and dataset_macd_signal[i, 0] > dataset_macd_signal[i, 1]: #kiedy MACD przecina sygnal od dolu to kupujemy
        decision_buy[i] = dataset[i,4]
        stocks+=money/dataset[i,4]
        money = 0
        
        
    elif dataset_macd_signal[i-1, 0] > dataset_macd_signal[i-1, 1] and dataset_macd_signal[i, 0] < dataset_macd_signal[i, 1]: #kiedy MACD przecina sygnal od gory to sprzedajemy
        decision_sell[i] = dataset[i,4]
        money += stocks*dataset[i,4] #tutaj zmienione ilosc dni
        stocks = 0  
        continue

    bank_balance.append(money+stocks*dataset[i,4]) #zamienic na money+Stocks*data[i]



#plotting for decision with time and MACD and signal    

plt.figure(figsize=(10, 6))
plt.plot(date,dataset[:,4],label='FACEBOOK STOCK', color='black')
plt.scatter(date,decision_buy,color='green', label='Sygnał kupna')
plt.scatter(date,decision_sell,color='red', label='Sygnał sprzedazy')
plt.title('Wykres ceny akcji wraz z oznaczeniami')
plt.xlabel('Data')
plt.ylabel('Cena')
plt.legend()
plt.grid(True)
plt.show()
 

## Wykres salda konta
plt.plot(bank_balance, label='Saldo konta', color='black')
plt.title('Saldo konta w czasie')
plt.xlabel('Dzień')
plt.ylabel('Saldo konta')
plt.grid(True)
plt.show()




print(f"Końcowa wartość salda bez zmian: {money}")

#TODO: zaimplementowac wskaznik williamsa i polaczyc go z wskaznikiem macd

def WilliamsIndicator(data, span):
    williams = []

    for i in range(len(data)):
        if i >= span - 1:
            high = np.max(data[i - span + 1:i + 1, 2])
            low = np.min(data[i - span + 1:i + 1, 3])

            williams_r = (high - data[i,2]) / (high - low) * -100
            williams.append(williams_r)
        else:
            williams.append(None)

    return williams

williams_indicator = np.array(WilliamsIndicator(dataset,14))

#obliczanie i wstawianie wartosci zmienionej

saldo = 1000.0
improved_dec_buy = np.ones_like(dataset[:,4])
improved_dec_sell = np.ones_like(dataset[:,4])
stocks = 0
improved_dec_buy[0] = None
improved_dec_sell[0] = None

for i in range(1, len(dataset_macd_signal)):
    improved_dec_buy[i] = None
    improved_dec_sell[i] = None
    if dataset_macd_signal[i-1, 0] < dataset_macd_signal[i-1, 1] and dataset_macd_signal[i, 0] > dataset_macd_signal[i, 1] and williams_indicator[i] != None and williams_indicator[i] < -70 and saldo > 0: #kupujemy
        improved_dec_buy[i] = dataset[i,4]
        stocks+=saldo/dataset[i,4]
        saldo = 0
        
        
    elif dataset_macd_signal[i-1, 0] > dataset_macd_signal[i-1, 1] and dataset_macd_signal[i, 0] < dataset_macd_signal[i, 1] and williams_indicator[i] != None and williams_indicator[i] > -20 and stocks > 0: #sprzedajemy
        improved_dec_sell[i] = dataset[i,4]
        saldo += stocks*dataset[i,4]
        stocks = 0  

print(saldo)

plt.figure(figsize=(10, 6))
plt.plot(date,dataset[:,4],label='FACEBOOK STOCK', color='black')
plt.scatter(date,improved_dec_buy,color='green', label='Sygnał kupna')
plt.scatter(date,improved_dec_sell,color='red', label='Sygnał sprzedazy')
plt.title('Wykres ceny akcji wraz z oznaczeniami')
plt.xlabel('Data')
plt.ylabel('Cena')
plt.legend()
plt.grid(True)
plt.show()


