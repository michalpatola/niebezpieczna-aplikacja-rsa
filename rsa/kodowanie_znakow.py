# napis zawierający wszystkie znaki obsługiwane przez nasz komunikator
dopuszczone_znaki = r""" 0123456789aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźżAĄBCĆDEĘFGHIJKLŁMNŃOÓPQRSŚTUVWXYZŹŻ`~!@#$%^&*()-_=+[]{}\|;:'",.<>/?"""


# konwertuje liczbę dziesiętną na binarną
def _dec_na_bin(liczba: int) -> str:
    wynik = ""

    if liczba == 0:
          wynik = "0"

    while liczba > 0:
          wynik = str(liczba % 2) + wynik
          liczba //= 2

    return wynik


# konwertuje liczbę binarną na dziesiętną
def _bin_na_dec(liczba: str) -> int:
    wynik = 0
    obecna_potega_2 = 1
    for i in range(len(liczba) - 1, -1, -1):
        if liczba[i] == "1":
            wynik = wynik + obecna_potega_2

        obecna_potega_2 *= 2

    return wynik


# dopelnia ciąg znaków reprezentujący liczbę binarną do 8 bitów
def _dopelnij_do_bajtu(liczba: str) -> str:
    while len(liczba) < 8:
        liczba = "0" + liczba
    return liczba


# znajduje indeks znaku w napisie
def _znajdz_indeks(znak: chr, napis: str) -> int:
    for i in range(len(napis)):
        if napis[i] == znak:
            return i
    return -1


# zamienia znak na ciąg 8 bitów (1 bajt)
def _zakoduj_znak(znak: chr) -> str:
    if len(znak) != 1:
        raise Exception("Kodować można tylko pojedyncze znaki!")
    if _znajdz_indeks(znak, dopuszczone_znaki) == -1:
         raise Exception("Kodowany znak musi być na dozwolonej liście!")
    # dopuszczone znaki są kodowane w podanej kolejności od zera
    # wystarczyłoby 7 bitów, ale zapasowo wszystkie kody będą ośmiobitowe
    return _dopelnij_do_bajtu(_dec_na_bin(_znajdz_indeks(znak, dopuszczone_znaki)))


# sprawdza, czy ciąg znaków składa się z samych zer i jedynek
def _czy_liczba_binarna(liczba: str) -> bool:
    for znak in liczba:
        if znak != "0" and znak != "1":
            return False

    return True


# zamienia ciąg bitów na odpowiadający mu znak
def _odkoduj_znak(bity: str) -> chr:
    if not _czy_liczba_binarna(bity):
        raise Exception("Nie można odkodować ciągu znaków innego niż binarnego!")

    dec = _bin_na_dec(bity)

    if dec >= len(dopuszczone_znaki):
        raise Exception("Brak znaku o podanym ciągu bitów na dozwolonej liście!")

    return dopuszczone_znaki[dec]


# zakodowuje wiadomość na ciąg bitów zgodnie z poniższymi zasadami:
# 1. wiadomości będą dzielone na bloki ośmioznakowe (czyli 64-bitowe) w celu szyfrowania, więc len(zakodowana_wiadomość) % 64 MUSI się równać 0
# 2. każdy znak dopełnienia ostatniego bloku na razie będzie kodowany jako osiem jedynek (czyli odpowiadał liczbie dziesiętnej 255)
# 3. dopełnienie będzie występować na KOŃCU ostatniego bloku
# 4. zakodowany blok składa się ze sklejonych zakodowanych kolejnych znaków wiadomości (+ ewentualnego dopełnienia)
# 5. zakodowana wiadomość składa się ze sklejonych zakodowanych kolejnych bloków
def zakoduj_wiadomosc(wiadomosc: str) -> str:
    zakodowana = ""
    dlugosc_wiadomosci = len(wiadomosc)

    for i in range(dlugosc_wiadomosci):
        zakodowana += _zakoduj_znak(wiadomosc[i])

    # dodanie ewentualnego dopełnienia
    if dlugosc_wiadomosci % 8 != 0:
        for i in range(8 - (dlugosc_wiadomosci % 8)):
            zakodowana += "11111111"

    return zakodowana


# odkodowuje wiadomość zgodnie z powyższymi zasadami
# UWAGA: ma sens tylko dla wiadomości o długości podzielnej przez 64 (pilnują tego: funkcja szyfrująca i odszyfrowująca RSA)
def odkoduj_wiadomosc(wiadomosc: str) -> str:
    odkodowana = ""
    bajt = ""
    dlugosc_wiadomosci = len(wiadomosc)

    i = 0
    while i < dlugosc_wiadomosci:
        bajt += wiadomosc[i]
        i += 1

        if i % 8 == 0:
            if bajt == "11111111":
                break
            
            odkodowana += _odkoduj_znak(bajt)
            bajt = ""

    return odkodowana
