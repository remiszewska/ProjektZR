from tkinter import *
from tkinter import messagebox
import requests
import tkintermapview
from bs4 import BeautifulSoup



jednostki = []

class Jednostka:
    def __init__(self, nazwa, miejscowosc, pracownicy):
        self.nazwa = nazwa
        self.miejscowosc = miejscowosc
        self.pracownicy = pracownicy
        self.wspolrzedne = Jednostka.wspolrzedne(self)

    def wspolrzedne(self) -> list:
        url: str = f'https://pl.wikipedia.org/wiki/{self.miejscowosc}'
        response = requests.get(url)
        response_html = BeautifulSoup(response.text, 'html.parser')
        return [
            float(response_html.select('.latitude')[1].text.replace(",", ".")),
            float(response_html.select('.longitude')[1].text.replace(",", "."))
        ]


def lista_jednostek(listbox_jednostki_strazy, map_widget):
    listbox_jednostki_strazy.delete(0, END)
    for idx, jednostka in enumerate(jednostki):
        listbox_jednostki_strazy.insert(idx, f'{jednostka.nazwa} {jednostka.miejscowosc} {jednostka.pracownicy}')
        jednostka.marker = map_widget.set_marker(jednostka.wspolrzedne[0], jednostka.wspolrzedne[1],
                                            text=f"{jednostka.nazwa}")

def dodaj_jednostke(entry_nazwa, entry_miejscowosc, entry_pracownicy, listbox_jednostki_strazy, map_widget):
    nazwa = entry_nazwa.get()
    miejscowosc = entry_miejscowosc.get()
    pracownicy = entry_pracownicy.get()

    print(nazwa, miejscowosc, pracownicy)
    jednostki.append(Jednostka(nazwa, miejscowosc, pracownicy))

    lista_jednostek(listbox_jednostki_strazy, map_widget)

    entry_nazwa.delete(0, END)
    entry_miejscowosc.delete(0, END)
    entry_pracownicy.delete(0, END)

    entry_nazwa.focus()

def usun_jednostke(listbox_jednostki_strazy, map_widget):
    i = listbox_jednostki_strazy.index(ACTIVE)
    print(i)
    jednostki.pop(i)
    lista_jednostek(listbox_jednostki_strazy, map_widget)


def pokaz_szczegoly_uzytkownika(listbox_jednostki_strazy, label_nazwa_szczegoly_obiektu_wartosc, label_miejscowosc_szczegoly_obiektu_wartosc, label_pracownicy_szczegoly_obiektu_wartosc, map_widget):
    i = listbox_jednostki_strazy.index(ACTIVE)
    nazwa = jednostki[i].nazwa
    label_nazwa_szczegoly_obiektu_wartosc.config(text=nazwa)
    miejscowosc = jednostki[i].miejscowosc
    label_miejscowosc_szczegoly_obiektu_wartosc.config(text=miejscowosc)
    pracownicy = jednostki[i].pracownicy
    label_pracownicy_szczegoly_obiektu_wartosc.config(text=pracownicy)
    map_widget.set_position(jednostki[i].wspolrzedne[0], jednostki[i].wspolrzedne[1])
    map_widget.set_zoom(12)

def edytuj_jednostke(listbox_jednostki_strazy, entry_nazwa, entry_miejscowosc, entry_pracownicy, button_dodaj_jednostke, map_widget):
    i = listbox_jednostki_strazy.index(ACTIVE)
    entry_nazwa.insert(0, jednostki[i].nazwa)
    entry_miejscowosc.insert(0, jednostki[i].miejscowosc)
    entry_pracownicy.insert(0, jednostki[i].pracownicy)

    button_dodaj_jednostke.config(text="Zapisz zmiany", command=lambda: aktualizuj_jednostke(i, entry_nazwa, entry_miejscowosc, entry_pracownicy, listbox_jednostki_strazy, button_dodaj_jednostke, map_widget))

def aktualizuj_jednostke(i, entry_nazwa, entry_miejscowosc, entry_pracownicy, listbox_jednostki_strazy, button_dodaj_jednostke, map_widget):
    jednostki[i].nazwa = entry_nazwa.get()
    jednostki[i].miejscowosc = entry_miejscowosc.get()
    jednostki[i].pracownicy = entry_pracownicy.get()
    lista_jednostek(listbox_jednostki_strazy, map_widget)
    button_dodaj_jednostke.config(text="Dodaj użytkownika", command=lambda: dodaj_jednostke)
    entry_nazwa.delete(0, END)
    entry_miejscowosc.delete(0, END)
    entry_pracownicy.delete(0, END)
    entry_nazwa.focus()

def create_jednostki_root(root):
    jednostki_root = Toplevel(root)
    jednostki_root.title("Jednostki straży pożarnej")
    jednostki_root.geometry("1024x760")

    # ramki do porządkowania struktury

    ramka_jednostki_strazy = Frame(jednostki_root)
    ramka_formularz = Frame(jednostki_root)
    ramka_szczegoly_jednostki = Frame(jednostki_root)

    ramka_jednostki_strazy.grid(column=0, row=0, padx=50)
    ramka_formularz.grid(column=1, row=0)
    ramka_szczegoly_jednostki.grid(column=0, row=1, columnspan=2)

    # lista jednostek

    label_jednostki_strazy = Label(ramka_jednostki_strazy, text="Lista jednostek straży: ")
    listbox_jednostki_strazy = Listbox(ramka_jednostki_strazy, width=50)
    button_pokaz_szczegoly = Button(ramka_jednostki_strazy, text="Pokaż szczegóły obiektu", command=lambda: pokaz_szczegoly_uzytkownika(listbox_jednostki_strazy, label_nazwa_szczegoly_obiektu_wartosc, label_miejscowosc_szczegoly_obiektu_wartosc, label_pracownicy_szegoly_obiektu_wartosc, map_widget))
    button_usun_obiekkt = Button(ramka_jednostki_strazy, text="Usuń obiekt", command=lambda: usun_jednostke(listbox_jednostki_strazy, map_widget))
    button_edytuj_obiekt = Button(ramka_jednostki_strazy, text="Edytuj obiekt", command=lambda: edytuj_jednostke(listbox_jednostki_strazy, entry_nazwa, entry_miejscowosc, entry_pracownicy, button_dodaj_jednostke, map_widget))

    label_jednostki_strazy.grid(row=0, column=0, columnspan=3)
    listbox_jednostki_strazy.grid(row=1, column=0, columnspan=3)
    button_pokaz_szczegoly.grid(row=2, column=0)
    button_usun_obiekkt.grid(row=2, column=1)
    button_edytuj_obiekt.grid(row=2, column=2)

    # formularz jednostki

    label_formularz = Label(ramka_formularz, text="Formularz: ")
    label_nazwa = Label(ramka_formularz, text="Nazwa jednostki: ")
    label_miejscowosc = Label(ramka_formularz, text="Miejscowość: ")
    label_pracownicy = Label(ramka_formularz, text="Podaj liczbę pracowników")

    entry_nazwa = Entry(ramka_formularz)
    entry_miejscowosc = Entry(ramka_formularz)
    entry_pracownicy = Entry(ramka_formularz)

    label_formularz.grid(row=0, column=0, columnspan=2)
    label_nazwa.grid(row=1, column=0, sticky=W)
    label_miejscowosc.grid(row=2, column=0, sticky=W)
    label_pracownicy.grid(row=3, column=0, sticky=W)

    entry_nazwa.grid(row=1, column=1)
    entry_miejscowosc.grid(row=2, column=1)
    entry_pracownicy.grid(row=3, column=1)

    button_dodaj_jednostke = Button(ramka_formularz, text="Dodaj jednostkę do listy", command=lambda: dodaj_jednostke(entry_nazwa, entry_miejscowosc, entry_pracownicy, listbox_jednostki_strazy, map_widget))
    button_dodaj_jednostke.grid(row=5, column=1, columnspan=2)

    # szczegóły obiektu

    label_szczegoly_obiektu = Label(ramka_szczegoly_jednostki, text="Szczegóły jednostki:")
    label_nazwa_szczegoly_obiektu = Label(ramka_szczegoly_jednostki, text="Nazwa jednostki: ")
    label_miejscowosc_szczegoly_obiektu = Label(ramka_szczegoly_jednostki, text="Lokalizacja jednosti: ")
    label_pracownicy_szegoly_obiektu = Label(ramka_szczegoly_jednostki, text="Ilość pracowników danej jednostki: ")

    label_nazwa_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_jednostki, text="...")
    label_miejscowosc_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_jednostki, text="...")
    label_pracownicy_szegoly_obiektu_wartosc = Label(ramka_szczegoly_jednostki, text="...:")

    label_szczegoly_obiektu.grid(row=0, column=0, sticky=W)
    label_nazwa_szczegoly_obiektu.grid(row=1, column=0, sticky=W)
    label_nazwa_szczegoly_obiektu_wartosc.grid(row=1, column=1)
    label_miejscowosc_szczegoly_obiektu.grid(row=1, column=2)
    label_miejscowosc_szczegoly_obiektu_wartosc.grid(row=1, column=3)
    label_pracownicy_szegoly_obiektu.grid(row=1, column=4)
    label_pracownicy_szegoly_obiektu_wartosc.grid(row=1, column=5)

    map_widget = tkintermapview.TkinterMapView(ramka_szczegoly_jednostki, width=900, height=400)
    map_widget.set_position(52.2, 21.0)
    map_widget.set_zoom(8)
    map_widget.grid(row=2, column=0, columnspan=8)
    # marker_WAT = map_widget.set_marker(52.25462674857218, 20.900225912403783, text="WAT")


    return(root)

pracownicy = []

class Pracownik:
    def __init__(self, imie, nazwisko, jednostka):
        self.imie = imie
        self.nazwisko = nazwisko
        self.jednostka = jednostka

def lista_pracownikow(listbox_pracownicy_strazy):
    listbox_pracownicy_strazy.delete(0, END)
    for idx, pracownik in enumerate(pracownicy):
        listbox_pracownicy_strazy.insert(idx, f'{pracownik.imie} {pracownik.nazwisko} {pracownik.jednostka}')

def dodaj_pracownika(entry_imie, entry_nazwisko, entry_jednostka, listbox_pracownicy_strazy):
    imie = entry_imie.get()
    nazwisko = entry_nazwisko.get()
    jednostka = entry_jednostka.get()
    print(imie, nazwisko, jednostka)
    pracownicy.append(Pracownik(imie, nazwisko, jednostka))

    lista_pracownikow(listbox_pracownicy_strazy)

    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_jednostka.delete(0, END)

    entry_imie.focus()

def usun_pracownika(listbox_pracownicy_strazy):
    i = listbox_pracownicy_strazy.index(ACTIVE)
    print(i)
    pracownicy.pop(i)
    lista_pracownikow(listbox_pracownicy_strazy)

def pokaz_szczegoly_pracownika(listbox_pracownicy_strazy,  label_imie_szczegoly_pracownikow_wartosc, label_nazwisko_szczegoly_pracownikow_wartosc, label_jednostka_szczegoly_pracownikow_wartosc):
    i = listbox_pracownicy_strazy.index(ACTIVE)
    imie = pracownicy[i].imie
    label_imie_szczegoly_pracownikow_wartosc.config(text=imie)
    nazwisko = pracownicy[i].nazwisko
    label_nazwisko_szczegoly_pracownikow_wartosc.config(text=nazwisko)
    jednostka = pracownicy[i].jednostka
    label_jednostka_szczegoly_pracownikow_wartosc.config(text=jednostka)

def edytuj_pracownika(listbox_pracownicy_strazy, entry_imie, entry_nazwisko, entry_jednostka, button_dodaj_pracownika):
    i = listbox_pracownicy_strazy.index(ACTIVE)
    entry_imie.insert(0, pracownicy[i].imie)
    entry_nazwisko.insert(0, pracownicy[i].nazwisko)
    entry_jednostka.insert(0, pracownicy[i].jednostka)

    button_dodaj_pracownika.config(text="Zapisz zmiany", command=lambda: aktualizuj_pracownika(i, entry_imie, entry_nazwisko, entry_jednostka, listbox_pracownicy_strazy, button_dodaj_pracownika))

def aktualizuj_pracownika(i, entry_imie, entry_nazwisko, entry_jednostka, listbox_pracownicy_strazy, button_dodaj_pracownika):
    pracownicy[i].imie = entry_imie.get()
    pracownicy[i].nazwisko = entry_nazwisko.get()
    pracownicy[i].jednostka = entry_jednostka.get()
    lista_pracownikow(listbox_pracownicy_strazy)
    button_dodaj_pracownika.config(text="Dodaj pracownika", command=lambda: dodaj_pracownika)
    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_jednostka.delete(0, END)
    entry_imie.focus()


def create_pracownicy_root(root):
    pracownicy_root = Toplevel(root)
    pracownicy_root.title("Pracownicy straży pożarnej")
    pracownicy_root.geometry("1024x760")

    # ramki do porządkowania struktury

    ramka_pracownicy_strazy = Frame(pracownicy_root)
    ramka_formularz = Frame(pracownicy_root)
    ramka_szczegoly_pracownikow = Frame(pracownicy_root)

    ramka_pracownicy_strazy.grid(column=0, row=0, padx=50)
    ramka_formularz.grid(column=1, row=0)
    ramka_szczegoly_pracownikow.grid(column=0, row=1, columnspan=2)

    # lista obiektów

    label_pracownicy_strazy = Label(ramka_pracownicy_strazy, text="Lista pracowników straży pożarnej: ")
    listbox_pracownicy_strazy = Listbox(ramka_pracownicy_strazy, width=50)
    button_pokaz_szczegoly = Button(ramka_pracownicy_strazy, text="Pokaż szczegóły", command=lambda:pokaz_szczegoly_pracownika(listbox_pracownicy_strazy,  label_imie_szczegoly_pracownikow_wartosc, label_nazwisko_szczegoly_pracownikow_wartosc, label_jednostka_szegoly_pracownikow_wartosc))
    button_usun_obiekkt = Button(ramka_pracownicy_strazy, text="Usuń obiekt", command=lambda:usun_pracownika(listbox_pracownicy_strazy))
    button_edytuj_obiekt = Button(ramka_pracownicy_strazy, text="Edytuj obiekt", command=lambda:edytuj_pracownika(listbox_pracownicy_strazy, entry_imie, entry_nazwisko, entry_jednostka, button_dodaj_pracownika))

    label_pracownicy_strazy.grid(row=0, column=0, columnspan=3)
    listbox_pracownicy_strazy.grid(row=1, column=0, columnspan=3)
    button_pokaz_szczegoly.grid(row=2, column=0)
    button_usun_obiekkt.grid(row=2, column=1)
    button_edytuj_obiekt.grid(row=2, column=2)

    # formularz pracownikow

    label_formularz = Label(ramka_formularz, text="Formularz: ")
    label_imie = Label(ramka_formularz, text="Imię: ")
    label_nazwisko = Label(ramka_formularz, text="Nazwisko: ")
    label_jednostka = Label(ramka_formularz, text="Jednostka: ")

    entry_imie = Entry(ramka_formularz)
    entry_nazwisko = Entry(ramka_formularz)
    entry_jednostka = Entry(ramka_formularz)

    label_formularz.grid(row=0, column=0, columnspan=2)
    label_imie.grid(row=1, column=0, sticky=W)
    label_nazwisko.grid(row=2, column=0, sticky=W)
    label_jednostka.grid(row=3, column=0, sticky=W)

    entry_imie.grid(row=1, column=1)
    entry_nazwisko.grid(row=2, column=1)
    entry_jednostka.grid(row=3, column=1)

    button_dodaj_pracownika = Button(ramka_formularz, text="Dodaj pracownika do listy", command=lambda:dodaj_pracownika(entry_imie, entry_nazwisko, entry_jednostka, listbox_pracownicy_strazy))
    button_dodaj_pracownika.grid(row=5, column=1, columnspan=2)

    # szczegóły pracownikow

    label_szczegoly_pracownikow = Label(ramka_szczegoly_pracownikow, text="Szczegóły dotyczące pracownika: ")
    label_imie_szczegoly_pracownikow = Label(ramka_szczegoly_pracownikow, text="Imię: ")
    label_nazwisko_szczegoly_pracownikow = Label(ramka_szczegoly_pracownikow, text="Nazwisko: ")
    label_jednostka_szegoly_pracownikow = Label(ramka_szczegoly_pracownikow, text="Jednostka: ")

    label_imie_szczegoly_pracownikow_wartosc = Label(ramka_szczegoly_pracownikow, text="...")
    label_nazwisko_szczegoly_pracownikow_wartosc = Label(ramka_szczegoly_pracownikow, text="...")
    label_jednostka_szegoly_pracownikow_wartosc = Label(ramka_szczegoly_pracownikow, text="...:")

    label_szczegoly_pracownikow.grid(row=0, column=0, sticky=W)
    label_imie_szczegoly_pracownikow.grid(row=1, column=0, sticky=W)
    label_imie_szczegoly_pracownikow_wartosc.grid(row=1, column=1)
    label_nazwisko_szczegoly_pracownikow.grid(row=1, column=2)
    label_nazwisko_szczegoly_pracownikow_wartosc.grid(row=1, column=3)
    label_jednostka_szegoly_pracownikow.grid(row=1, column=4)
    label_jednostka_szegoly_pracownikow_wartosc.grid(row=1, column=5)

    return (root)

pozary = []

class Pozar:
    def __init__(self, miejscowosc, jednostka):
        self.miejscowosc = miejscowosc
        self.jednostka = jednostka
        self.wspolrzedne = Pozar.wspolrzedne(self)

    def wspolrzedne(self) -> list:
        url: str = f'https://pl.wikipedia.org/wiki/{self.miejscowosc}'
        response = requests.get(url)
        response_html = BeautifulSoup(response.text, 'html.parser')
        return [
            float(response_html.select('.latitude')[1].text.replace(",", ".")),
            float(response_html.select('.longitude')[1].text.replace(",", "."))
        ]

def lista_pozarow(listbox_pozary, map_widget):
    listbox_pozary.delete(0, END)
    for idx, pozar in enumerate(pozary):
        listbox_pozary.insert(idx, f'{pozar.miejscowosc} {pozar.jednostka}')
        pozar.marker = map_widget.set_marker(pozar.wspolrzedne[0],pozar.wspolrzedne[1],
                                            text=f"{pozar.jednostka}")

def dodaj_pozar(entry_miejscowosc, entry_jednostka, listbox_pozary, map_widget):
    miejscowosc = entry_miejscowosc.get()
    jednostka = entry_jednostka.get()

    print(miejscowosc, jednostka)
    pozary.append(Pozar(miejscowosc, jednostka))

    lista_pozarow(listbox_pozary, map_widget)

    entry_miejscowosc.delete(0, END)
    entry_jednostka.delete(0, END)

    entry_miejscowosc.focus()

def usun_pozar(listbox_pozary, map_widget):
    i = listbox_pozary.index(ACTIVE)
    print(i)
    pozary.pop(i)
    lista_pozarow(listbox_pozary, map_widget)

def pokaz_szczegoly_pozaru(listbox_pozary, label_miejsowosoc_szczegoly_pozarow_wartosc, label_jednostka_szczegoly_pozarow_wartosc, map_widget):
    i = listbox_pozary.index(ACTIVE)
    miejscowosc = pozary[i].miejscowosc
    label_miejsowosoc_szczegoly_pozarow_wartosc.config(text=miejscowosc)
    jednostka = pozary[i].jednostka
    label_jednostka_szczegoly_pozarow_wartosc.config(text=jednostka)
    map_widget.set_position(pozary[i].wspolrzedne[0], pozary[i].wspolrzedne[1])
    map_widget.set_zoom(12)

def edytuj_pozar(listbox_pozary, entry_miejscowosc, entry_jednostka, button_dodaj_pozar, map_widget):
    i = listbox_pozary.index(ACTIVE)
    entry_miejscowosc.insert(0, pozary[i].miejscowosc)
    entry_jednostka.insert(0, pozary[i].jednostka)

    button_dodaj_pozar.config(text="Zapisz zmiany", command=lambda: aktualizuj_pozar(i, entry_miejscowosc, entry_jednostka, listbox_pozary, button_dodaj_pozar, map_widget))

def aktualizuj_pozar(i, entry_miejscowosc, entry_jednostka, listbox_pozary, button_dodaj_pozar, map_widget):
    pozary[i].miejscowosc = entry_miejscowosc.get()
    pozary[i].jednostka = entry_jednostka.get()
    lista_pozarow(listbox_pozary, map_widget)
    button_dodaj_pozar.config(text="Dodaj pracownika", command=lambda: dodaj_pozar)
    entry_miejscowosc.delete(0, END)
    entry_jednostka.delete(0, END)
    entry_miejscowosc.focus()


def create_pozary_root(root):
    pozary_root = Toplevel(root)
    pozary_root.title("Miejsca pożarów")
    pozary_root.geometry("1024x760")

    # ramki do porządkowania struktury

    ramka_pozary = Frame(pozary_root)
    ramka_formularz = Frame(pozary_root)
    ramka_szczegoly_pozarow = Frame(pozary_root)

    ramka_pozary.grid(column=0, row=0, padx=50)
    ramka_formularz.grid(column=1, row=0)
    ramka_szczegoly_pozarow.grid(column=0, row=1, columnspan=2)

    # lista obiektów

    label_pozary = Label(ramka_pozary, text="Informacje o pożarach: ")
    listbox_pozary = Listbox(ramka_pozary, width=50)
    button_pokaz_szczegoly = Button(ramka_pozary, text="Pokaż szczegóły", command=lambda: pokaz_szczegoly_pozaru(listbox_pozary, label_miejsowosoc_szczegoly_pozarow_wartosc, label_jednostka_szczegoly_pozarow_wartosc, map_widget))
    button_usun_obiekkt = Button(ramka_pozary, text="Usuń obiekt", command=lambda:usun_pozar(listbox_pozary, map_widget))
    button_edytuj_obiekt = Button(ramka_pozary, text="Edytuj obiekt", command=lambda:edytuj_pozar(listbox_pozary, entry_miejscowosc, entry_jednostka, button_dodaj_pozar, map_widget))

    label_pozary.grid(row=0, column=0, columnspan=3)
    listbox_pozary.grid(row=1, column=0, columnspan=3)
    button_pokaz_szczegoly.grid(row=2, column=0)
    button_usun_obiekkt.grid(row=2, column=1)
    button_edytuj_obiekt.grid(row=2, column=2)

    # formularz pozary

    label_formularz = Label(ramka_formularz, text="Formularz: ")
    label_miejscowosc = Label(ramka_formularz, text="Miejsowość: ")
    label_jednostka = Label(ramka_formularz, text="Jednostka: ")

    entry_miejscowosc = Entry(ramka_formularz)
    entry_jednostka = Entry(ramka_formularz)

    label_formularz.grid(row=0, column=0, columnspan=2)
    label_miejscowosc.grid(row=1, column=0, sticky=W)
    label_jednostka.grid(row=2, column=0, sticky=W)

    entry_miejscowosc.grid(row=1, column=1)
    entry_jednostka.grid(row=2, column=1)

    button_dodaj_pozar = Button(ramka_formularz, text="Dodaj do listy", command=lambda: dodaj_pozar(entry_miejscowosc, entry_jednostka, listbox_pozary, map_widget))
    button_dodaj_pozar.grid(row=5, column=1, columnspan=2)

    # szczegóły pozarow

    label_szczegoly_pozarow = Label(ramka_szczegoly_pozarow, text="Szczegóły dotyczące pożaru: ")
    label_miejsowosoc_szczegoly_pozarow = Label(ramka_szczegoly_pozarow, text="Miejsce pożaru: ")
    label_jednostka_szczegoly_pozarow = Label(ramka_szczegoly_pozarow, text="Jednostka: ")

    label_miejsowosoc_szczegoly_pozarow_wartosc = Label(ramka_szczegoly_pozarow, text="...")
    label_jednostka_szczegoly_pozarow_wartosc = Label(ramka_szczegoly_pozarow, text="...")

    label_szczegoly_pozarow.grid(row=0, column=0, sticky=W)
    label_miejsowosoc_szczegoly_pozarow.grid(row=1, column=0, sticky=W)
    label_miejsowosoc_szczegoly_pozarow_wartosc.grid(row=1, column=1)
    label_jednostka_szczegoly_pozarow.grid(row=1, column=2)
    label_jednostka_szczegoly_pozarow_wartosc.grid(row=1, column=3)

    map_widget = tkintermapview.TkinterMapView(ramka_szczegoly_pozarow, width=900, height=400)
    map_widget.set_position(52.2, 21.0)
    map_widget.set_zoom(8)
    map_widget.grid(row=2, column=0, columnspan=8)

    return (root)