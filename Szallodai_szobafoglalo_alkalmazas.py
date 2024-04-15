from abc import ABC, abstractmethod
from datetime import datetime

class Szoba(ABC):
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar

    @abstractmethod
    def info(self):
        pass

class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam, ar):
        super().__init__(szobaszam, ar)

    def info(self):
        return f"Egyágyas szoba, Szobaszám: {self.szobaszam}, Ár: {self.ar} Ft/éj"

class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam, ar):
        super().__init__(szobaszam, ar)

    def info(self):
        return f"Kétágyas szoba, Szobaszám: {self.szobaszam}, Ár: {self.ar} Ft/éj"

class Foglalas:
    def __init__(self, szobaszam, datum, nev):
        self.szobaszam = szobaszam
        self.datum = datum
        self.nev = nev

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def szoba_hozzaad(self, szoba):
        self.szobak.append(szoba)

    def foglalas_hozzaadasa(self, szobaszam, datum, nev):
        try:
            datum_obj = datetime.strptime(datum, "%Y-%m-%d")
        except ValueError:
            return "Hibás dátumformátum. Kérem, használja az YYYY-MM-DD formátumot."
        if datum_obj < datetime.now():
            return "A foglalás dátuma nem lehet a múltban."

        szoba_letezik = any(szoba.szobaszam == szobaszam for szoba in self.szobak)
        if not szoba_letezik:
            return f"A {szobaszam} számú szoba nem létezik."

        for foglalas in self.foglalasok:
            if foglalas.szobaszam == szobaszam and foglalas.datum == datum:
                return "Ez a szoba ezen a napon már foglalt."
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                ar = szoba.ar
                break
        self.foglalasok.append(Foglalas(szobaszam, datum, nev))
        return f"Foglalás sikeresen rögzítve. Az ár: {ar} Ft."

    def foglalas_lemondasa(self, szobaszam, datum, nev):
        for foglalas in self.foglalasok:
            if foglalas.szobaszam == szobaszam and foglalas.datum == datum and foglalas.nev == nev:
                self.foglalasok.remove(foglalas)
                return "A foglalás sikeresen lemondva."
        return "Nem található foglalás a megadott adatokkal."

    def foglalasok_listazasa(self):
        if not self.foglalasok:
            print("Nincsenek foglalások.")
            return
        for foglalas in self.foglalasok:
            print(f"Foglalás: {foglalas.nev}, Szobaszám: {foglalas.szobaszam}, Dátum: {foglalas.datum}")

    def elerheto_szobak(self, datum):
        elerheto = {szoba.szobaszam: szoba for szoba in self.szobak}
        for foglalas in self.foglalasok:
            if foglalas.datum == datum and foglalas.szobaszam in elerheto:
                del elerheto[foglalas.szobaszam]
        return list(elerheto.values())

szalloda = Szalloda("Hotel Ruanda")

szalloda.szoba_hozzaad(EgyagyasSzoba("101", 15000))
szalloda.szoba_hozzaad(KetagyasSzoba("102", 23600))
szalloda.szoba_hozzaad(KetagyasSzoba("103", 19800))


szalloda.foglalas_hozzaadasa("101", "2024-05-20", "Kiss Ramóna")
szalloda.foglalas_hozzaadasa("102", "2024-05-24", "Bruce Willis; Demi Moore")
szalloda.foglalas_hozzaadasa("102", "2024-05-11", "Jessica Alba; Horváth Péter")

def main_menu():
    while True:
        print("\nSzállodai szobafoglaló alkalmazás")
        print("Hotel Ruanda")
        print("1. Foglalás")
        print("2. Lemondás")
        print("3. Foglalások listázása")
        print("4. Kilépés")
        valasztas = input("Válasszon egy opciót: ")

        if valasztas == "1":
            datum = input("Dátum (YYYY-MM-DD): ")
            elerheto_szobak = szalloda.elerheto_szobak(datum)
            if not elerheto_szobak:
                print("Nincsenek elérhető szobák ezen a dátumon.")
                continue
            print("\nElérhető szobák:")
            for szoba in elerheto_szobak:
                print(szoba.info())
            szobaszam = input("Válasszon szobaszámot: ")
            nev = input("Foglaló neve: ")
            print(szalloda.foglalas_hozzaadasa(szobaszam, datum, nev))
        elif valasztas == "2":
            szobaszam = input("Szobaszám: ")
            datum = input("Dátum (YYYY-MM-DD): ")
            nev = input("Foglaló neve: ")
            print(szalloda.foglalas_lemondasa(szobaszam, datum, nev))
        elif valasztas == "3":
            szalloda.foglalasok_listazasa()
        elif valasztas == "4":
            break
        else:
            print("Érvénytelen választás. Kérjük, próbálja újra.")


if __name__ == "__main__":
    main_menu()
