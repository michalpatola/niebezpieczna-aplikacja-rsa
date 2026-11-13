"""
Liczby ujemne kodowane są zwyczajnie przez dodanie znaku "-" na początku liczby.
"""


# usuwa zera na początku liczby binarnej (DODATNIEJ lub UJEMNEJ)
def usun_zera_wiodace(liczba: str) -> str:
    czy_minus = False
    if liczba != "" and liczba[0] == "-":
        liczba = liczba[1:]
        czy_minus = True

    dlugosc_liczby = len(liczba)

    licznik = 0
    for i in range(dlugosc_liczby):
        if liczba[i] == "0":
            licznik += 1
        else:
            break

    liczba = liczba[licznik:]

    # nie chcemy pustych liczb
    if liczba == "":
        return "0"

    if czy_minus:
        return "-" + liczba

    return liczba


# dodaje dwie DODATNIE liczby binarne
def dodaj_dodatnie(a: str, b: str) -> str:
    if (a != "" and a[0] == "-") or (b != "" and b[0] == "-"):
        raise Exception("Obie liczby muszą być dodatnie!")

    a = usun_zera_wiodace(a)
    b = usun_zera_wiodace(b)

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


# dodaje zera na końcu liczby binarnej (dotyczy tylko liczb DODATNICH)
def dodaj_zera_na_koncu(liczba: str, ile: int) -> str:
    if liczba != "" and liczba[0] == "-":
        raise Exception("Liczba musi być dodatnia!")

    for i in range(ile):
        liczba += "0"

    return liczba


# mnoży dwie DOWOLNE (zarówno dodatnie, jak i ujemne) liczby binarne
def pomnoz(a: str, b: str) -> str:
    a = usun_zera_wiodace(a)
    b = usun_zera_wiodace(b)

    czy_minus = False

    if a[0] == "-":
        czy_minus = not czy_minus
        a = a[1:]

    if b[0] == "-":
        czy_minus = not czy_minus
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

    if czy_minus:
        return "-" + wynik

    return wynik


# zwraca true, jeśli a >= b (gdzie a, b - liczby DODATNIE)
def czy_niemniejsza(a: str, b: str) -> bool:
    if (a != "" and a[0] == "-") or (b != "" and b[0] == "-"):
        raise Exception("Obie liczby muszą być dodatnie!")

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


# zamienia liczbę binarną ze stringa na listę (dotyczy liczb DODATNICH)
def zamien_na_liste(liczba: str) -> list:
    if liczba != "" and liczba[0] == "-":
        raise Exception("Liczba musi być dodatnia!")

    wynik = []
    for cyfra in liczba:
        wynik.append(cyfra)

    return wynik


# oblicza a - b, gdzie a oraz b to DODATNIE liczby binarne
def odejmij_dodatnie(a: str, b: str) -> str:
    if (a != "" and a[0] == "-") or (b != "" and b[0] == "-"):
        raise Exception("Obie liczby muszą być dodatnie!")

    a = usun_zera_wiodace(a)
    b = usun_zera_wiodace(b)

    czy_minus = False

    # jeśli wynik odejmowania miałby wyjść ujemny, to zamieniamy liczby i dodajemy minus na końcu (bo a - b = - (b - a))
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

        if cyfra_a >= cyfra_b: # nic nie trzeba "pożyczać"
            wynik = str(int(cyfra_a) - int(cyfra_b)) + wynik
            i += 1
        else: # tutaj jest mechanizm "pożyczki"
            indeks_a = dlugosc_a - i - 2

            while a[indeks_a] != "1": # szukamy najwcześniejszej jedynki po lewej, z której będziemy pożyczać
                indeks_a -= 1

            a[indeks_a] = "0" # pożyczamy

            # zwiększamy o 1 każde zero (poza ostatnim, czyli tym, dla którego potrzebna była pożyczka) na prawo od znalezionej jedynki
            while indeks_a < dlugosc_a - i - 1:
                indeks_a += 1
                a[indeks_a] = "1"

            a[indeks_a] = "2" # ostatnie zero zwiększamy o 2

    # potem pozostałe cyfry a
    for i in range(dlugosc_a - dlugosc_b - 1, -1, -1):
        wynik = a[i] + wynik

    wynik = usun_zera_wiodace(wynik)

    if czy_minus:
        return "-" + wynik

    return wynik


# zwraca (-1) * liczba dla DOWOLNEJ liczby binarnej
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


# oblicza wynik z dzielenia całkowitego liczba przez 2 dla DOWOLNEJ liczby binarnej
def podziel_calkowicie_przez_2(liczba: str) -> str:
    liczba = usun_zera_wiodace(liczba)

    if liczba == "0" or liczba == "1":
        return "0"

    if liczba == "-1":
        return "-1"

    dlugosc_liczby = len(liczba)
    liczba = liczba[:(dlugosc_liczby - 1)]

    if liczba[0] == "-":
        return dodaj(liczba, "-1")

    return liczba


# oblicza wynik z dzielenia całkowitego a przez b dla DOWOLNYCH liczb binarnych
# działa zgodnie z zasadami matematyki, czyli zwraca wynik taki, że:
# a mod b = a - b * wynik
# w szczególności podziel_calkowicie(a, b) nie musi się równać podziel_calkowicie(-a, -b)
# ta funkcja istnieje głównie dla kolejnej funkcji, czyli modulo
def podziel_calkowicie(a: str, b: str) -> str:
    a = usun_zera_wiodace(a)
    b = usun_zera_wiodace(b)

    czy_minus = False # mówi, czy trzeba na końcu dodać minus do wyniku
    czy_jeden = False # mówi, czy trzeba dodać jeden do wyniku przed ewentualnym dodaniem minusa (podłoga z dzielenia dodatniej liczby to jak sufit po usunięciu jej minusa)

    if a[0] == "-":
        czy_minus = not czy_minus
        czy_jeden = True
        a = a[1:]

    if b[0] == "-":
        czy_minus = not czy_minus
        b = b[1:]

    if b == "0":
        raise Exception("Nie można dzielić przez zero!")

    # jeśli dzielna jest mniejsza od dzielnika, to od razu można podać wynik
    if not czy_niemniejsza(a, b):
        if czy_jeden:
            if czy_minus:
                return "-1"
            return "1"
        return "0"

    # wyszukuję binarnie iloraz
    lewy = "1"
    prawy = a
    srodek = podziel_calkowicie_przez_2(dodaj(lewy, prawy))
    iloczyn = pomnoz(b, srodek)
    kolejny_iloczyn = pomnoz(b, dodaj(srodek, "1"))

    # pętla zatrzymuje się, jeśli zgadnięty_iloraz * dzielnik = dzielna
    # LUB
    # dzielna należy do zbioru ( zgadnięty_iloraz * dzielnik, (zgadnięty_iloraz + 1) * dzielnik ]
    while not (iloczyn == a or (czy_niemniejsza(a, iloczyn) and czy_niemniejsza(kolejny_iloczyn, a))):
        if czy_niemniejsza(a, iloczyn):
            lewy = srodek
        else:
            prawy = srodek

        srodek = podziel_calkowicie_przez_2(dodaj(lewy, prawy))
        iloczyn = pomnoz(b, srodek)
        kolejny_iloczyn = pomnoz(b, dodaj(srodek, "1"))

    # ostateczne modyfikacje wyniku
    if kolejny_iloczyn == a:
        srodek = dodaj(srodek, "1")
    if czy_jeden and iloczyn != a and kolejny_iloczyn != a:
        srodek = dodaj(srodek, "1")
    if czy_minus:
        return "-" + srodek
    return srodek


# oblicza resztę z dzielenia a przez b dla DOWOLNYCH liczb binarnych
# działa zgodnie z zasadami matematyki (reszta z dzielenia jest zawsze nieujemna), czyli tak:
# a mod b = a - b * podziel_calkowicie(a, b)
def modulo(a: str, b: str) -> str:
    return dodaj(a, zmien_znak_liczby(pomnoz(b, podziel_calkowicie(a, b))))