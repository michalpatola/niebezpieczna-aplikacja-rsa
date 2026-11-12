"""
Liczby ujemne kodowane są zwyczajnie przez dodanie znaku "-" na początku liczby.
"""


# usuwa zera na początku liczby DODATNIEJ
def usun_zera_wiodace(liczba: str) -> str:
    licznik = 0
    for i in range(len(liczba)):
        if liczba[i] == "0":
            licznik += 1
        else:
            break

    wynik = liczba[licznik:]

    # nie chcemy pustych liczb
    if wynik == "":
        return "0"

    return wynik


# dodaje dwie DODATNIE liczby binarne
def dodaj_dodatnie(a: str, b: str) -> str:
    if (a != "" and a[0] == "-") or (b != "" and b[0] == "-"):
        raise Exception("Obie liczby muszą być dodatnie!")
    
    dlugosc_a = len(a)
    dlugosc_b = len(b)

    # chcemy, żeby liczba a miała nie więcej cyfr niż liczba b
    if dlugosc_b < dlugosc_a:
        a, b = b, a
        dlugosc_a, dlugosc_b = dlugosc_b, dlugosc_a

    wynik = ""
    przeniesienie = 0

    # najpierw wykorzystujemy wszystkie cyfry a
    for i in range(dlugosc_a):
        indeks_a = dlugosc_a - i - 1
        indeks_b = dlugosc_b - i - 1
        suma = int(a[indeks_a]) + int(b[indeks_b]) + przeniesienie
        wynik = str(suma % 2) + wynik
        przeniesienie = suma // 2

    # potem pozostałe cyfry b
    for i in range(dlugosc_b - dlugosc_a - 1, -1, -1):
        suma = int(b[i]) + przeniesienie
        wynik = str(suma % 2) + wynik
        przeniesienie = suma // 2

    # dodajemy pozostałe przeniesienie
    wynik = str(przeniesienie) + wynik

    return usun_zera_wiodace(wynik)


# dodaje zera na końcu liczby binarnej
def dodaj_zera_na_koncu(liczba: str, ile: int) -> str:
    for i in range(ile):
        liczba += "0"

    return liczba


# mnoży dwie DOWOLNE (zarówno dodatnie, jak i ujemne) liczby binarne
def pomnoz(a: str, b: str) -> str:
    znak = 0

    if a[0] == "-":
        znak += 1
        a = a[1:]

    if b[0] == "-":
            znak += 1
            b = b[1:]

    dlugosc_a = len(a)
    dlugosc_b = len(b)
    
    if dlugosc_b < dlugosc_a:
        a, b = b, a
        dlugosc_a, dlugosc_b = dlugosc_b, dlugosc_a

    wynik = ""
    przesuniecie = 0

    for i in range(dlugosc_a - 1, -1, -1):
        if a[i] == "1":
            wynik = dodaj_dodatnie(wynik, dodaj_zera_na_koncu(b, przesuniecie))

        przesuniecie += 1

    if wynik == "":
        return "0"

    if znak % 2 == 0:
        return wynik

    return "-" + wynik


# zwraca true, jeśli a >= b
def czy_niemniejsza(a: str, b: str) -> bool:
    a = usun_zera_wiodace(a)
    b = usun_zera_wiodace(b)
    dlugosc_a = len(a)
    dlugosc_b = len(b)

    if dlugosc_a > dlugosc_b:
        return True

    if dlugosc_a < dlugosc_b:
        return False
    
    for i in range(dlugosc_a):
        if a[i] == b[i]:
            continue
        if a[i] > b[i]:
            return True
        else:
            return False

    return True


# zamienia liczbę binarną ze stringa na listę
def zamien_na_liste(liczba: str) -> list:
    wynik = []
    for cyfra in liczba:
        wynik.append(cyfra)

    return wynik


# oblicza a - b, gdzie a oraz b to DODATNIE liczby binarne
def odejmij_dodatnie(a: str, b: str) -> str:
    if (a != "" and a[0] == "-") or (b != "" and b[0] == "-"):
        raise Exception("Obie liczby muszą być dodatnie!")

    czy_minus = False

    if not czy_niemniejsza(a, b):
        czy_minus = True
        a, b = b, a

    # zamieniam na listę, żeby dało się modyfikować poszczególne cyfry liczby binarnej
    a = zamien_na_liste(a)
    b = zamien_na_liste(b)

    dlugosc_a = len(a)
    dlugosc_b = len(b)

    wynik = ""

    i = 0
    # najpierw wykorzystujemy wszystkie cyfry b
    while i < dlugosc_b:
        indeks_a = dlugosc_a - i - 1
        indeks_b = dlugosc_b - i - 1
        cyfra_a = a[indeks_a]
        cyfra_b = b[indeks_b]

        if cyfra_a >= cyfra_b:
            wynik = str(int(cyfra_a) - int(cyfra_b)) + wynik
            i += 1
        else: # tutaj jest mechanizm "pożyczki"
            indeks_a = dlugosc_a - i - 2

            while a[indeks_a] != "1":
                indeks_a -= 1

            a[indeks_a] = "0"

            while indeks_a < dlugosc_a - i - 1:
                indeks_a += 1
                a[indeks_a] = "1"

            a[indeks_a] = "2"

    # potem pozostałe cyfry a
    for i in range(dlugosc_a - dlugosc_b - 1, -1, -1):
        wynik = a[i] + wynik

    wynik = usun_zera_wiodace(wynik)

    if czy_minus:
        return "-" + wynik

    return wynik


# zwraca (-1) * liczba
def zmien_znak_liczby(liczba: str) -> str:
    if liczba[0] == "-":
        return liczba[1:]
    return "-" + liczba


# dodaje dwie DOWOLNE (zarówno dodatnie, jak i ujemne) liczby binarne
def dodaj(a: str, b: str) -> str:
    if a == "":
        return usun_zera_wiodace(b)
    
    if b == "":
        return usun_zera_wiodace(a)
    
    if a[0] != "-" and b[0] != "-":
        return dodaj_dodatnie(a, b)
    
    if a[0] == "-" and b[0] == "-":
        return "-" + dodaj_dodatnie(zmien_znak_liczby(a), zmien_znak_liczby(b))

    if a[0] != "-" and b[0] == "-":
        return odejmij_dodatnie(a, zmien_znak_liczby(b))

    if a[0] == "-" and b[0] != "-":
        return odejmij_dodatnie(b, zmien_znak_liczby(a))