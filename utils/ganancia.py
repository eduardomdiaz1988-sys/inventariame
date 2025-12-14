# utils/ganancia.py
def calcular_ganancia(valor: int) -> int:
    if valor in [3, 4]:
        return 12
    elif valor == 5:
        return 20
    elif valor == 7:
        return 28
    elif valor == 10:
        return 40
    return 0
