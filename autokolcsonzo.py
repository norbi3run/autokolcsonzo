from abc import ABC, abstractmethod
from datetime import datetime


class Auto(ABC):
    def __init__(self, rendszam: str, tipus: str, berleti_dij: int):
        self._rendszam = rendszam
        self._tipus = tipus
        self._berleti_dij = berleti_dij

    @property
    def rendszam(self):
        return self._rendszam

    @property
    def tipus(self):
        return self._tipus

    @property
    def berleti_dij(self):
        return self._berleti_dij

    @abstractmethod
    def auto_tipus(self):
        pass

    def __str__(self):
        return f"{self._tipus} ({self._rendszam}) - {self._berleti_dij} Ft/nap"


class Szemelyauto(Auto):
    def __init__(self, rendszam: str, tipus: str, berleti_dij: int, ulohelyek: int):
        super().__init__(rendszam, tipus, berleti_dij)
        self._ulohelyek = ulohelyek

    def auto_tipus(self):
        return "Személyautó"

    def __str__(self):
        return f"{super().__str__()} | Ülőhelyek száma: {self._ulohelyek}"


class Teherauto(Auto):
    def __init__(self, rendszam: str, tipus: str, berleti_dij: int, teherbiras: int):
        super().__init__(rendszam, tipus, berleti_dij)
        self._teherbiras = teherbiras

    def auto_tipus(self):
        return "Teherautó"

    def __str__(self):
        return f"{super().__str__()} | Teherbírás: {self._teherbiras} kg"


class Berles:
    def __init__(self, auto: Auto, datum: str, berlo_nev: str):
        self._auto = auto
        self._datum = datum
        self._berlo_nev = berlo_nev

    @property
    def auto(self):
        return self._auto

    @property
    def datum(self):
        return self._datum

    @property
    def berlo_nev(self):
        return self._berlo_nev

    def __str__(self):
        return (
            f"Bérlő: {self._berlo_nev} | "
            f"Autó: {self._auto.tipus} ({self._auto.rendszam}) | "
            f"Dátum: {self._datum}"
        )


class Autokolcsonzo:
    def __init__(self, nev: str):
        self._nev = nev
        self._autok = []
        self._berlesek = []

    def auto_hozzaadas(self, auto: Auto):
        self._autok.append(auto)

    def berles_hozzaadas(self, berles: Berles):
        self._berlesek.append(berles)

    def autok_listazasa(self):
        print("\nElérhető autók:")
        for auto in self._autok:
            print(auto)

    def berlesek_listazasa(self):
        print("\nAktuális bérlések:")
        if not self._berlesek:
            print("Nincs aktív bérlés.")
            return

        for index, berles in enumerate(self._berlesek, start=1):
            print(f"{index}. {berles}")

    def auto_berlese(self, rendszam: str, datum: str, berlo_nev: str):
        try:
            datetime.strptime(datum, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Hibás dátumformátum! Használat: ÉÉÉÉ-HH-NN")

        auto = None

        for a in self._autok:
            if a.rendszam == rendszam:
                auto = a
                break

        if auto is None:
            raise ValueError("Nem található autó ezzel a rendszámmal.")

        for berles in self._berlesek:
            if berles.auto.rendszam == rendszam and berles.datum == datum:
                raise Exception("Az autó már foglalt erre a napra.")

        uj_berles = Berles(auto, datum, berlo_nev)
        self._berlesek.append(uj_berles)

        print(f"Sikeres foglalás! Fizetendő: {auto.berleti_dij} Ft")

    def berles_lemondasa(self, rendszam: str, datum: str):
        for berles in self._berlesek:
            if berles.auto.rendszam == rendszam and berles.datum == datum:
                self._berlesek.remove(berles)
                print("Bérlés sikeresen lemondva.")
                return

        raise Exception("Nincs ilyen bérlés.")


def adatok_betoltese():
    kolcsonzo = Autokolcsonzo("Villám Autókölcsönző")

    auto1 = Szemelyauto("ABC-123", "BMW 330 (E46)", 15000, 5)
    auto2 = Szemelyauto("XYZ-456", "Honda Civic", 14000, 5)
    auto3 = Teherauto("TRA-789", "Ford Transit", 20000, 1500)

    kolcsonzo.auto_hozzaadas(auto1)
    kolcsonzo.auto_hozzaadas(auto2)
    kolcsonzo.auto_hozzaadas(auto3)

    kolcsonzo.berles_hozzaadas(
        Berles(auto1, "2026-05-20", "Soós Norbert")
    )
    kolcsonzo.berles_hozzaadas(
        Berles(auto2, "2026-05-21", "Nagy Anna")
    )
    kolcsonzo.berles_hozzaadas(
        Berles(auto3, "2026-05-22", "Tóth Béla")
    )
    kolcsonzo.berles_hozzaadas(
        Berles(auto1, "2026-05-23", "Szabó Gábor")
    )

    return kolcsonzo


def menu():
    kolcsonzo = adatok_betoltese()

    while True:
        print("\n===== AUTÓKÖLCSÖNZŐ RENDSZER =====")
        print("1 - Autók listázása")
        print("2 - Autó bérlése")
        print("3 - Bérlés lemondása")
        print("4 - Bérlések listázása")
        print("0 - Kilépés")

        valasztas = input("Választás: ")

        try:
            if valasztas == "1":
                kolcsonzo.autok_listazasa()

            elif valasztas == "2":
                rendszam = input("Rendszám: ")
                datum = input("Dátum (ÉÉÉÉ-HH-NN): ")
                berlo = input("Bérlő neve: ")

                kolcsonzo.auto_berlese(rendszam, datum, berlo)

            elif valasztas == "3":
                rendszam = input("Rendszám: ")
                datum = input("Dátum (ÉÉÉÉ-HH-NN): ")

                kolcsonzo.berles_lemondasa(rendszam, datum)

            elif valasztas == "4":
                kolcsonzo.berlesek_listazasa()

            elif valasztas == "0":
                print("Program kilépés...")
                break

            else:
                print("Érvénytelen menüpont!")

        except Exception as hiba:
            print(f"Hiba: {hiba}")


if __name__ == "__main__":
    menu()