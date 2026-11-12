'''
Plik odpowiadający za generator liczb pierwszych.
W implementacji został wykorzystany LCG (Linear Congruential Generator),
który kryptograficznie nie jest bezpieczny.
Generator wykorzystuje wzór x_{x+1} = (a*x_n + c) mod m,
istotą słabości tego generatora, jest wybór słabego ziarna x_0.
'''

import time
from rsa.rsa_male_liczby import czy_pierwsza

#Stałe LCG
A = 1664525
C = 1013904223
M = 2**32

class NiebezpiecznyRNG:
    def __init__(self, ziarno: int=None):
        if ziarno is None:
            ziarno = int(time.time()) #Słabość generatora - czas z dokładnością do sekundy
        self.stan = ziarno % M

    def nastepna(self) -> int:
        self.stan = (A*self.stan + C) % M
        return self.stan

    def z_zakresu(self, dolny: int, gorny: int) -> int:
        return dolny + self.nastepna()%(gorny-dolny)

    def losowa_liczba_pierwsza(self, dolny: int, gorny: int) -> int:
        kandydat = self.z_zakresu(dolny, gorny)
        if kandydat % 2 == 0:
            kandydat += 1
        while not czy_pierwsza(kandydat):
            kandydat+=2
        return kandydat

