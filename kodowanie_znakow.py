# konwertuje liczbę dziesiętną na binarną
def dec_na_bin(liczba: int) -> str:
    wynik = ""

    if liczba == 0:
          wynik = "0"

    while liczba > 0:
          wynik = str(liczba % 2) + wynik
          liczba //= 2

    return wynik


# dopelnia ciąg znaków reprezentujący liczbę binarną do 8 bitów
def dopelnij_do_bajtu(liczba: str) -> str:
    while len(liczba) < 8:
        liczba = "0" + liczba
    return liczba


# znajduje indeks znaku w napisie
def znajdz_indeks(znak: chr, napis: str) -> int:
    for i in range(len(napis)):
        if napis[i] == znak:
            return i
    return -1


# napis zawierający wszystkie znaki obsługiwane przez nasz komunikator
dopuszczone_znaki = r""" 0123456789aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźżAĄBCĆDEĘFGHIJKLŁMNŃOÓPQRSŚTUVWXYZŹŻ`~!@#$%^&*()-_=+[]{}\|;:'",.<>/?"""


# zamienia znak na ciąg 8 bitów (1 bajt)
def zakoduj(znak: chr) -> str:
    if len(znak) != 1:
        raise Exception("Kodować można tylko pojedyncze znaki!")
    if znajdz_indeks(znak, dopuszczone_znaki) == -1:
         raise Exception("Kodowany znak musi być na dozwolonej liście!")
    # dopuszczone znaki są kodowane w podanej kolejności od zera
    # wystarczyłoby 7 bitów, ale zapasowo wszystkie kody będą ośmiobitowe
    return dopelnij_do_bajtu(dec_na_bin(znajdz_indeks(znak, dopuszczone_znaki)))