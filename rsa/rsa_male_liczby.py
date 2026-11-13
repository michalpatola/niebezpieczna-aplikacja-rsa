# oblicza a^n mod m w czasie O(log n)
def szybkie_potegowanie_modulo(a: int, n: int, m: int) -> int:
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


# zwraca tablicę kolejnych ilorazów
def zwroc_tablice_ilorazow(a: int, b: int) -> list:
    Q = []

    # chcemy, żeby zawsze pierwsza liczba była niemniejsza od drugiej
    if a < b:
        a, b = b, a

    while b > 1:
        Q.append(a // b)
        r = a % b
        a = b
        b = r
    
    return Q


# zwraca x takie, że x * a + y * m = 1 (mod m), czyli oblicza a^(-1)
def rozszerzony_algorytm_euklidesa(a: int, m: int) -> int:
    Q = zwroc_tablice_ilorazow(a, m)
    x = (-1) * Q[len(Q) - 1]
    y = 1

    # zauważyłem, jak współczynniki przy coraz wcześniejszych parach reszt zależą od poprzedniej pary współczynników, rozpisując sobie na przykładzie
    for i in range(len(Q) - 2, -1, -1):
        x, y = (y - x * Q[i]), x

    return x % m # modulo jest po to, żeby x był ze zbioru {0, 1, 2, ..., m - 1}


# sprawdza, czy podana liczba jest liczbą pierwszą
def czy_pierwsza(liczba: int) -> bool:
    if liczba < 2:
        return False

    i = 2
    while i * i <= liczba:
        if liczba % i == 0:
            return False
        i += 1

    return True


# znajduje klucz prywatny d, czyli odwrotność e w modulo (p-1)*(q-1)
def znajdz_klucz_prywatny(p: int, q: int, e: int) -> int:
    if p == q:
        raise Exception("p oraz q muszą być różne od siebie!") # inaczej wzór na fi byłby inny oraz złamanie N byłoby trywialne

    fi = (p - 1) * (q - 1)

    if not (czy_pierwsza(p) and czy_pierwsza(q)):
        raise Exception("Zarówno p, jak i q muszą być liczbami pierwszymi!")
    if e <= 1 or e >= fi:
        raise Exception("e musi być większe od 1 i mniejsze od (p - 1) * (q - 1)")
    if prosty_algorytm_euklidesa(e, fi) != 1:
        raise Exception("e musi być względnie pierwsze z (p - 1) * (q - 1)")

    d = rozszerzony_algorytm_euklidesa(e, fi)

    if d == e:
        raise Exception("Ale pech! Klucz prywatny wyszedł taki sam jak publiczny (niedopuszczalne)! Wybierz inny klucz publiczny (wykładnik e)!")

    return d


# szyfruje wiadomość za pomocą RSA
def zaszyfruj_rsa(tekst_jawny: int, klucz_publiczny: int, modul_systemu: int) -> int:
    if tekst_jawny < 0 or tekst_jawny >= modul_systemu:
        raise Exception("Wiadomość musi być większa lub równa 0 i mniejsza od modułu systemu!") # inaczej nie będzie się dało jednoznacznie odszyfrować szyfrogramu
    if prosty_algorytm_euklidesa(tekst_jawny, modul_systemu) != 1:
        raise Exception("Dla małych liczb wiadomość musi być względnie pierwsza z modułem systemu!") # inaczej łatwo wyliczyć klucz prywatny z C oraz N = p * q
    
    return szybkie_potegowanie_modulo(tekst_jawny, klucz_publiczny, modul_systemu)


# odszyfrowuje wiadomość za pomocą RSA
def odszyfruj_rsa(szyfrogram: int, klucz_prywatny: int, modul_systemu: int) -> int:
    return szybkie_potegowanie_modulo(szyfrogram, klucz_prywatny, modul_systemu)


# wyświetla menu wyboru dla przykładu poniżej
def wyswietl_menu():
    print()
    print("1 - Wylicz klucz prywatny")
    print("2 - Zaszyfruj wiadomość")
    print("3 - Odszyfruj wiadomość")
    print("4 - Wyjdź")


# przykład działania RSA dla małych liczb (decymalnych)
if __name__ == "__main__":
    print("Tu możesz szyfrować i odszyfrowywać wiadomości przy użyciu RSA")
    print("--------------------------------------------------------------")

    while True:
        wyswietl_menu()
        wybor = int(input("Twój wybór: "))
        if wybor == 1:
            p = int(input("Podaj p (liczbę pierwszą): "))
            q = int(input("Podaj q (liczbę pierwszą, inną niż p): "))
            e = int(input("Podaj klucz publiczny (wykładnik e, taki że e > 1 ORAZ e < (fi = (p - 1) * (q - 1)) ORAZ NWD(e, fi) = 1): "))
            print("Klucz prywatny:", znajdz_klucz_prywatny(p, q, e))
            print("N =", p * q)
            print("fi =", (p - 1) * (q - 1))
        elif wybor == 2:
            N = int(input("Podaj moduł systemu (N = p * q): "))
            e = int(input("Podaj klucz publiczny: "))
            M = int(input("Podaj wiadomość do zaszyfrowania (tekst jawny M, taki że M >= 0 ORAZ M < N ORAZ dla małych liczb NWD(M, N) = 1): "))
            print("Zaszyfrowana wiadomość:", zaszyfruj_rsa(M, e, N))
        elif wybor == 3:
            N = int(input("Podaj moduł systemu: "))
            d = int(input("Podaj klucz prywatny (wykładnik d, taki że e * d = 1 (mod fi)): "))
            C = int(input("Podaj wiadomość do odszyfrowania: "))
            print("Odszyfrowana wiadomość:", odszyfruj_rsa(C, d, N))
        elif wybor == 4:
            break
        else:
            print("Niepoprawny wybór!")