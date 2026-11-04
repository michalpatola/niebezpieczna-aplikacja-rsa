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



# ----------------------------------------------------------------------------------------------------------------------------------------



# oblicza a^n mod m w czasie O(log n)
def decymalne_szybkie_potegowanie_modulo(a: int, n: int, m: int) -> int:
    wynik = 1
    a %= m
    while n > 0:
        if n % 2 == 1:
            wynik = (wynik * a) % m
        a = (a * a) % m
        n //= 2

    return wynik


# znajduje NWD(a,b)
def prosty_algorytm_euklidesa(a: int, b: int) -> int:
    while b > 0:
        r = a % b
        a = b
        b = r
    return a


# znajduje klucz prywatny d, czyli odwrotność e w modulo (p-1)*(q-1)
def male_liczby_znajdz_klucz_prywatny(p: int, q: int, e: int) -> int:
    fi = (p - 1) * (q - 1)
    if e <= 1 or e >= fi:
        raise Exception("e musi być większe od 1 i mniejsze od (p - 1) * (q - 1)")
    elif prosty_algorytm_euklidesa(e, fi) != 1:
        raise Exception("e musi być względnie pierwsze z (p - 1) * (q - 1)")
    # tu trzeba dokończyć
    return 0