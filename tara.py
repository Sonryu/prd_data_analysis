import numpy as np

def aplicar_transformacao(x, y_raw):
    """
    Aplica a transformação linear nos dados de entrada.
    Equação: y = -4.51 * 10^-3 * y_raw + 37900
    """
    # Converte para array numpy para permitir operações vetorizadas
    y_raw = np.array(y_raw)
    x = np.array(x)
    
    # Aplica a fórmula
    y_transformado = -4.51e-3 * y_raw + 37900
    
    return x, y_transformado

# Exemplo de uso:
# x_input = [1, 2, 3]
# y_input = [1000, 2000, 3000]
# x_final, y_final = aplicar_transformacao(x_input, y_input)