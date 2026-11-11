'''
plik testowy to dzialan binarnych
'''

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "rsa")))

from rsa.dzialania_binarne import (
    usun_zera_wiodace,
    dodaj,
    dodaj_zera_na_koncu,
    pomnoz,
)


def test_usun_zera_wiodace():
    assert usun_zera_wiodace("00101") == "101"
    assert usun_zera_wiodace("101") == "101"
    assert usun_zera_wiodace("1000") == "1000"
    assert usun_zera_wiodace("0010") == "10"



def test_dodaj_zgodne_z_arytmetyka():
    pary = [("101", "1110"), ("1", "1"), ("11", "1"), ("1010", "110"), ("0", "101")]
    for a, b in pary:
        wynik = dodaj(a, b)
        assert int(wynik, 2) == int(a, 2) + int(b, 2)


def test_dodaj_rozne_dlugosci():
    assert int(dodaj("1010", "101"), 2) == 15


def test_dodaj_zera_na_koncu():
    assert dodaj_zera_na_koncu("11", 2) == "1100"    
    assert dodaj_zera_na_koncu("1", 0) == "1"
    assert dodaj_zera_na_koncu("101", 3) == "101000"


def test_pomnoz_zgodne_z_arytmetyka():
    pary = [("101", "11"), ("1010", "10"), ("111", "111"), ("0", "101"), ("1", "0")]
    for a, b in pary:
        wynik = pomnoz(a, b)
        assert int(wynik, 2) == int(a, 2) * int(b, 2)


def test_pomnoz_przez_potege_dwojki():
    assert int(pomnoz("101", "100"), 2) == 20   # 5 * 4


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
