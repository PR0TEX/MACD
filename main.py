import numpy as np
import pandas
import matplotlib.pyplot as plt
import matplotlib
x = 2

def EMA(N,samples, sample_id):
    alpha = 2 / (N + 1)
    base = 1 - alpha
    sum_top = 0
    sum_bottom = 0
    for i in range(N):
        if sample_id - i >= 0:
            base_pow = pow(base,i)
            sum_bottom += base_pow
            sum_top += base_pow * samples[sample_id - i]

    return sum_top/sum_bottom

def MACD(samples, sample_id):
    EMA_12 = EMA(12,samples,sample_id)
    EMA_26 = EMA(26,samples,sample_id)

    return EMA_12 - EMA_26

def generate_MACD(n,samples):
    MACD_val = []
    for i in range(n):
        MACD_val.append(MACD(samples,i))
    return MACD_val

def SIGNAL(MACD_val,id):
    return EMA(9,MACD_val,id)

def generate_SIGNAL(n, MACD_val):
    SIGNAL_val = []
    for i in range(n):
        SIGNAL_val.append(SIGNAL(MACD_val, i))
    return SIGNAL_val
def read_file(file_name):
    file = pandas.read_csv(file_name,index_col=0)
    values = []
    for i,j in  file.iterrows():
        #print(file.at[i,'Zamkniecie'])
        values.append(file.at[i,'Zamkniecie'])
    # if not open(file):
    #     print("Something went wrong, unable to open file")
    #     return -1
    return values
#flag determines if it needs 2 diagrams at plot on not
def make_plot(MACD_val, title, isTwoDiagrams, label1, label2='',SIGNAL_val=None):
    matplotlib.use('Tkagg')
    range = np.linspace(0,1000,1000) #check if it is nessesary and how it worksq
    line1, = plt.plot(range,MACD_val, label=label1)
    if(isTwoDiagrams):
        line2, = plt.plot(range,SIGNAL_val, label=label2)
        plt.legend(handles=[line1, line2])
    else:
        plt.legend(handles=[line1])
    plt.title(title)
def simulation(N,MACD_val, SIGNAL_val,samples,value,delay):
    max_size = value-1
    delay_cond = (delay if delay == 0 else delay - 1) # condition to avoid -1 in case dealy equals 0
    assets = value / samples[0]
    value = 0
    for i in range(N):
        if i >= delay:
            if MACD_val[i-delay] > SIGNAL_val[i-delay] and MACD_val[i- delay_cond] < SIGNAL_val[i-delay_cond] and assets != 0:
                value = assets * samples[i]
                assets = 0
            elif MACD_val[i-2] < SIGNAL_val[i-delay] and MACD_val[i-delay_cond] > SIGNAL_val[i-delay_cond] and value != 0:
                assets = value / samples[i]
                value = 0
    if(value == 0):
        value = assets * samples[max_size]
    print(value)
def L14(samples,period,start): #finds the lowest price traded of the 14 previous trading sessions
    min = samples[start]
    for i in range(start,period):
        if samples[i] < min:
            min = samples[i]
    return min

def stochastic_oscillator(samples):

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    n = 1000
    samples = read_file('wig20_d.csv')
    make_plot(samples,'Wig20',False,'wig20')
    plt.figure()
    MACD_val = generate_MACD(n,samples)
    SIGNAL_val = generate_SIGNAL(n,MACD_val)
    print(MACD_val)
    print(SIGNAL_val)
    simulation(n,MACD_val,SIGNAL_val,samples,1000,40)
    make_plot(MACD_val,'MACD AND SIGNAL', True, 'MACD', 'SIGNAL',SIGNAL_val)
    #plt.set_figwidth(300)
    plt.show()