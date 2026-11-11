''''
Program generujeacy klucz RSA, który wykorzystuje niebezpieczny generator.
'''

from niebezpieczny_rng import NiebezpiecznyRNG

def generuj_klucze(ziarno: int = None):
    rng = NiebezpiecznyRNG(ziarno)
    p= rng.losowa_liczba_pierwsza(10_000, 100_000) #maly zakres liczb, dodatkowa słabość
    q=rng.losowa_liczba_pierwsza(10_000, 100_000)

    N=p*q
    fi = (p-1)*(q-1)
    e=65537

    return {
        "N": N,
        "e": e,
        "p": p,
        "q": q
    }
