'''
plik testowy do rsa
'''

import os
import sys

# dodajemy folder rsa/ do ścieżki, żeby dało się zaimportować moduł
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "rsa")))

from rsa.rsa_male_liczby import (
    szybkie_potegowanie_modulo,
    prosty_algorytm_euklidesa,
    rozszerzony_algorytm_euklidesa,
    czy_pierwsza,
    znajdz_klucz_prywatny,
    zaszyfruj_rsa,
    odszyfruj_rsa,
)


# pomocnik: sprawdza, czy wywołanie rzuca wyjątek
def zglasza_wyjatek(funkcja) -> bool:
    try:
        funkcja()
    except Exception:
        return True
    return False


# --- potęgowanie modularne ---

def test_potegowanie_zgodne_z_wbudowanym_pow():
    przypadki = [(2, 10, 1000), (7, 0, 13), (5, 117, 19), (123, 456, 789), (3, 3, 7)]
    for a, n, m in przypadki:
        assert szybkie_potegowanie_modulo(a, n, m) == pow(a, n, m)


def test_potegowanie_wykladnik_zero():
    # a^0 = 1 (mod m)
    assert szybkie_potegowanie_modulo(999, 0, 17) == 1


# --- NWD ---

def test_nwd_znane_wartosci():
    assert prosty_algorytm_euklidesa(12, 8) == 4
    assert prosty_algorytm_euklidesa(17, 5) == 1   # względnie pierwsze
    assert prosty_algorytm_euklidesa(100, 75) == 25


# --- test pierwszości ---

def test_czy_pierwsza_dla_pierwszych():
    for liczba in [2, 3, 5, 7, 11, 13, 61, 53, 97]:
        assert czy_pierwsza(liczba) is True


def test_czy_pierwsza_dla_zlozonych():
    for liczba in [0, 1, 4, 6, 9, 15, 100, 121]:
        assert czy_pierwsza(liczba) is False


# --- odwrotność modularna ---

def test_odwrotnosc_modularna():
    # (a * a^-1) mod m powinno dać 1
    przypadki = [(3, 7), (5, 12), (7, 160), (17, 3120)]
    for a, m in przypadki:
        odwrotnosc = rozszerzony_algorytm_euklidesa(a, m)
        assert (a * odwrotnosc) % m == 1


# --- klucz prywatny ---

def test_klucz_prywatny_znane_przyklady():
    # klasyczny przykład podręcznikowy
    assert znajdz_klucz_prywatny(61, 53, 17) == 2753
    assert znajdz_klucz_prywatny(17, 11, 7) == 23


def test_klucz_prywatny_odrzuca_bledne_dane():
    assert zglasza_wyjatek(lambda: znajdz_klucz_prywatny(7, 7, 5))      # p == q
    assert zglasza_wyjatek(lambda: znajdz_klucz_prywatny(8, 11, 7))     # p nie jest pierwsze
    assert zglasza_wyjatek(lambda: znajdz_klucz_prywatny(17, 11, 1))    # e za małe
    assert zglasza_wyjatek(lambda: znajdz_klucz_prywatny(17, 11, 5))    # NWD(e, fi) != 1 (fi=160)


# --- pełny obieg: szyfrowanie -> odszyfrowanie ---

def test_round_trip_odszyfrowanie_zwraca_oryginal():
    p, q, e = 17, 11, 7
    N = p * q
    d = znajdz_klucz_prywatny(p, q, e)
    for M in [2, 3, 10, 100, 186]:        # wszystkie względnie pierwsze z N = 187
        szyfrogram = zaszyfruj_rsa(M, e, N)
        assert odszyfruj_rsa(szyfrogram, d, N) == M


def test_round_trip_wiekszy_klucz():
    p, q, e = 61, 53, 17
    N = p * q
    d = znajdz_klucz_prywatny(p, q, e)
    for M in [2, 42, 1000, 3000]:
        szyfrogram = zaszyfruj_rsa(M, e, N)
        assert odszyfruj_rsa(szyfrogram, d, N) == M


def test_szyfrowanie_odrzuca_bledne_dane():
    N, e = 187, 7
    assert zglasza_wyjatek(lambda: zaszyfruj_rsa(187, e, N))   # M >= N
    assert zglasza_wyjatek(lambda: zaszyfruj_rsa(-1, e, N))    # M < 0
    assert zglasza_wyjatek(lambda: zaszyfruj_rsa(11, e, N))    # NWD(M, N) != 1 (11 | 187)


# --- prosty runner, gdy uruchamiamy bez pytesta ---

if __name__ == "__main__":
    testy = [f for nazwa, f in sorted(globals().items())
             if nazwa.startswith("test_") and callable(f)]
    bledy = 0
    for test in testy:
        try:
            test()
            print("[OK]   " + test.__name__)
        except AssertionError as e:
            bledy += 1
            print("[BLAD] " + test.__name__ + ": " + str(e))
    print("\n{}/{} testow przeszlo".format(len(testy) - bledy, len(testy)))
    sys.exit(1 if bledy else 0)
