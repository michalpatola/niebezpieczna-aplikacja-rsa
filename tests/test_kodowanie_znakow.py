'''
plik testowy sprawdzajacy kodowanie znakow
'''

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "rsa")))

from rsa.kodowanie_znakow import (
    dec_na_bin,
    dopelnij_do_bajtu,
    znajdz_indeks,
    zakoduj,
    dopuszczone_znaki,
)


def zglasza_wyjatek(funkcja) -> bool:
    try:
        funkcja()
    except Exception:
        return True
    return False



def test_dec_na_bin_znane_wartosci():
    assert dec_na_bin(0) == "0"
    assert dec_na_bin(1) == "1"
    assert dec_na_bin(5) == "101"
    assert dec_na_bin(8) == "1000"
    assert dec_na_bin(255) == "11111111"


def test_dec_na_bin_zgodne_z_pythonem():
    for liczba in range(0, 300):
        assert dec_na_bin(liczba) == bin(liczba)[2:]   


def test_dopelnij_do_bajtu_dodaje_zera():
    assert dopelnij_do_bajtu("101") == "00000101"
    assert dopelnij_do_bajtu("1") == "00000001"
    assert dopelnij_do_bajtu("1000") == "00001000"


def test_dopelnij_do_bajtu_pelny_bajt_bez_zmian():
    assert dopelnij_do_bajtu("10110011") == "10110011"


# --- znajdz_indeks ---

def test_znajdz_indeks():
    assert znajdz_indeks(" ", dopuszczone_znaki) == 0
    assert znajdz_indeks("0", dopuszczone_znaki) == 1
    assert znajdz_indeks("a", dopuszczone_znaki) == 11
    assert znajdz_indeks("€", dopuszczone_znaki) == -1 


# --- zakoduj ---

def test_zakoduj_zawsze_osiem_bitow():
    for znak in dopuszczone_znaki:
        kod = zakoduj(znak)
        assert len(kod) == 8
        assert all(bit in "01" for bit in kod)


def test_zakoduj_znane_wartosci():
    assert zakoduj(" ") == "00000000"   
    assert zakoduj("0") == "00000001"   
    assert zakoduj("a") == "00001011"   


def test_zakoduj_odrzuca_bledne_dane():
    assert zglasza_wyjatek(lambda: zakoduj("€"))    
    assert zglasza_wyjatek(lambda: zakoduj("ab"))   
    assert zglasza_wyjatek(lambda: zakoduj(""))    


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
