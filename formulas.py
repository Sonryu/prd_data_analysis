import numpy as np 

def converter_segundos(ms): #converter tempo de ms para s
    return ms/1000

def calcular_tempo(tempo_s): #tempo total de queima
    return tempo_s[-1] - tempo_s[0]

def calcular_empuxo_maximo(empuxo): #valor maximo do empuxo
    return np.max(empuxo)

def empuxo_medio(empuxo, T): #calculo do valor medio do empuxo
    return np.sum(empuxo) / T

def calcular_t_p(empuxo, tempo_s): #instante de tempo onde o empuxo é maximo
    indice = np.argmax(empuxo)
    return tempo_s[indice]

def calcular_impulso_total(empuxo, tempo_s): #calcular impulso total pela regra trapezoidal resolvendo a integral: I = f(t) dt
    return np.trapz(empuxo, tempo_s)

