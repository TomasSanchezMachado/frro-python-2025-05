"""Type, Comprensión de Listas, Sorted y Filter."""

from typing import List, Union


def numeros_al_final_basico(lista: List[Union[float, str]]) -> List[Union[float, str]]:
    """Toma una lista de enteros y strings y devuelve una lista con todos los
    elementos numéricos al final.
    """
    numeros = []
    letras = []

    for elem in lista:
        if isinstance(elem, (float, int)):
            numeros.append(elem)
        elif isinstance(elem, str):
            letras.append(elem)

    return letras + numeros
        
    
# NO MODIFICAR - INICIO
assert numeros_al_final_basico([3, "a", 1, "b", 10, "j"]) == ["a", "b", "j", 3, 1, 10]
# NO MODIFICAR - FIN


###############################################################################


def numeros_al_final_comprension(lista: List[Union[float, str]]) -> List[Union[float, str]]:
    """Re-escribir utilizando comprensión de listas."""
    numeros = list((elem for elem in lista if isinstance(elem, (float | int))))
    letras = list((elem for elem in lista if isinstance(elem, str)))

    return letras + numeros


# NO MODIFICAR - INICIO
assert numeros_al_final_comprension([3, "a", 1, "b", 10, "j"]) == ["a", "b", "j", 3, 1, 10]
# NO MODIFICAR - FIN


###############################################################################


def numeros_al_final_sorted(lista: List[Union[float, str]]) -> List[Union[float, str]]:
    """Re-escribir utilizando la función sorted con una custom key.
    Referencia: https://docs.python.org/3/library/functions.html#sorted
    """
    return sorted(lista, key=lambda x: isinstance(x, (int, float)))

# NO MODIFICAR - INICIO
assert numeros_al_final_sorted([3, "a", 1, "b", 10, "j"]) == ["a", "b", "j", 3, 1, 10]
# NO MODIFICAR - FIN

###############################################################################

def numeros_al_final_filter(lista: List[Union[float, str]]) -> List[Union[float, str]]:
    """CHALLENGE OPCIONAL - Re-escribir utilizando la función filter.
    Referencia: https://docs.python.org/3/library/functions.html#filter
    """
    numeros = list(filter(lambda elem: isinstance(elem, (float | int)), lista))
    strings = list(filter(lambda elem: isinstance(elem, (str)), lista))

    return strings + numeros


# NO MODIFICAR - INICIO
if __name__ == "__main__":
    assert numeros_al_final_filter([3, "a", 1, "b", 10, "j"]) == ["a", "b", "j", 3, 1, 10]
# NO MODIFICAR - FIN


###############################################################################


# def numeros_al_final_recursivo(lista: List[Union[float, str]]) -> List[Union[float, str]]:
#     """CHALLENGE OPCIONAL - Re-escribir de forma recursiva."""
#     if not lista:
#         return []
    
#     primero = lista[0]
#     resto = numeros_al_final_recursivo(lista[1:])
    
#     if isinstance(primero, (int, float)):
#         return resto + [primero]
#     else:
#         return [primero] + resto
    
#     #Esta solución devuelve ["a", "b", "j", 10, 1, 3] ->No se como hacer para que devuelva los numeros en el orden esperado

# # NO MODIFICAR - INICIO
# if __name__ == "__main__":
#     assert numeros_al_final_recursivo([3, "a", 1, "b", 10, "j"]) == ["a", "b", "j", 3, 1, 10]
# # NO MODIFICAR - FIN
