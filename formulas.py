import numpy as np 

def converter_segundos(ms): #converter tempo de ms para s
    return ms/1000


def calcular_tempo(tempo_s): #tempo total de queima
    return tempo_s[-1] - tempo_s[0]

def calcular_empuxo_maximo(empuxo): #valor maximo do empuxo
    return np.max(empuxo)

def empuxo_medio(empuxo, T): #calculo do valor medio do empuxo
    return np.sum(empuxo) / T

def calcular_t_p(empuxo, )