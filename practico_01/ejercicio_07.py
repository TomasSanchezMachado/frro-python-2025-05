"""Slicing."""


def es_palindromo(palabra: str) -> bool:
    """Toma un string y devuelve un booleano en base a si se lee igual al
    derecho y al revés.

    Restricción: No utilizar bucles - Usar Slices de listas.
    Referencia: https://docs.python.org/3/tutorial/introduction.html#lists
    """
    if len(palabra) == 0:
        return True
    else:
        if palabra[0] == palabra[-1]:
            return es_palindromo(palabra[1:-1]) #Elimina el primer y el ultimo char
        else:
            return False
            


# NO MODIFICAR - INICIO
assert not es_palindromo("amor")
assert es_palindromo("radar")
assert es_palindromo("")
# NO MODIFICAR - FIN

###############################################################################

def mitad(palabra: str) -> str:
    """Toma un string y devuelve la mitad. Si la longitud es impar, redondear
    hacia arriba.

    Restricción: No utilizar bucles - Usar Slices de listas.
    Referencia: https://docs.python.org/3/tutorial/introduction.html#lists
    """
    if len(palabra) % 2 == 0:
        return palabra[:len(palabra) //2] 
    else:
        return palabra[:(len(palabra) // 2) + 1]


# NO MODIFICAR - INICIO
assert mitad("hello") == "hel"
assert mitad("Moon") == "Mo"
assert mitad("") == ""
# NO MODIFICAR - FIN