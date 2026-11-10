# usuwa zera na początku liczby
def usun_zera_wiodace(liczba: str) -> str:
    licznik = 0
    for i in range(len(liczba)):
        if liczba[i] == "0":
            licznik += 1
        else:
            break

    return liczba[licznik:]


# dodaje dwie liczby binarne
def dodaj(a: str, b: str) -> str:
    dlugosc_a = len(a)
    dlugosc_b = len(b)

    # chcemy, żeby pierwsza liczba miała nie więcej cyfr niż druga liczba
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

    if wynik == "":
        return "0"

    return usun_zera_wiodace(wynik)


# dodaje zera na końcu liczby binarnej
def dodaj_zera_na_koncu(liczba: str, ile: int) -> str:
    for i in range(ile):
        liczba += "0"

    return liczba


# mnoży dwie liczby binarne
def pomnoz(a: str, b: str) -> str:
    dlugosc_a = len(a)
    dlugosc_b = len(b)
    
    if dlugosc_b < dlugosc_a:
        a, b = b, a
        dlugosc_a, dlugosc_b = dlugosc_b, dlugosc_a

    wynik = ""
    przesuniecie = 0

    for i in range(dlugosc_a - 1, -1, -1):
        if a[i] == "1":
            wynik = dodaj(wynik, dodaj_zera_na_koncu(b, przesuniecie))

        przesuniecie += 1

    if wynik == "":
        return "0"

    return wynik