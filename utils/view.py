from tkinter import *
from tkinter import messagebox

jednostki = []

class Jednostka:
    def __init__(self, nazwa, miejscowosc, pracownicy):
        self.nazwa = nazwa
        self.miejscowosc = miejscowosc
        self.pracownicy = pracownicy


def lista_jednostek(listbox_jednostki_strazy):
    listbox_jednostki_strazy.delete(0, END)
    for idx, jednostka in enumerate(jednostki):
        listbox_jednostki_strazy.insert(idx, f'{jednostka.nazwa} {jednostka.miejscowosc} {jednostka.pracownicy}')

def dodaj_jednostke(entry_nazwa, entry_miejscowosc, entry_pracownicy, listbox_jednostki_strazy):
    nazwa = entry_nazwa.get()
    miejscowosc = entry_miejscowosc.get()
    pracownicy = entry_pracownicy.get()

    print(nazwa, miejscowosc, pracownicy)
    jednostki.append(Jednostka(nazwa, miejscowosc, pracownicy))

    lista_jednostek(listbox_jednostki_strazy)

    entry_nazwa.delete(0, END)
    entry_miejscowosc.delete(0, END)
    entry_pracownicy.delete(0, END)

    entry_nazwa.focus()

def usun_jednostke(listbox_jednostki_strazy):
    i = listbox_jednostki_strazy.index(ACTIVE)
    print(i)
    jednostki.pop(i)
    lista_jednostek(listbox_jednostki_strazy)


def pokaz_szczegoly_uzytkownika(listbox_jednostki_strazy, label_nazwa_szczegoly_obiektu_wartosc, label_miejscowosc_szczegoly_obiektu_wartosc, label_pracownicy_szczegoly_obiektu_wartosc):
    i = listbox_jednostki_strazy.index(ACTIVE)
    nazwa = jednostki[i].nazwa
    label_nazwa_szczegoly_obiektu_wartosc.config(text=nazwa)
    miejscowosc = jednostki[i].miejscowosc
    label_miejscowosc_szczegoly_obiektu_wartosc.config(text=miejscowosc)
    pracownicy = jednostki[i].pracownicy
    label_pracownicy_szczegoly_obiektu_wartosc.config(text=pracownicy)

def edytuj_jednostke(listbox_jednostki_strazy, entry_nazwa, entry_miejscowosc, entry_pracownicy, button_dodaj_jednostke):
    i = listbox_jednostki_strazy.index(ACTIVE)
    entry_nazwa.insert(0, jednostki[i].nazwa)
    entry_miejscowosc.insert(0, jednostki[i].miejscowosc)
    entry_pracownicy.insert(0, jednostki[i].pracownicy)

    button_dodaj_jednostke.config(text="Zapisz zmiany", command=lambda: aktualizuj_jednostke(i, entry_nazwa, entry_miejscowosc, entry_pracownicy, listbox_jednostki_strazy, button_dodaj_jednostke))


def aktualizuj_jednostke(i, entry_nazwa, entry_miejscowosc, entry_pracownicy, listbox_jednostki_strazy, button_dodaj_jednostke):
    jednostki[i].nazwa = entry_nazwa.get()
    jednostki[i].miejscowosc = entry_miejscowosc.get()
    jednostki[i].pracownicy = entry_pracownicy.get()
    lista_jednostek(listbox_jednostki_strazy)
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
    button_pokaz_szczegoly = Button(ramka_jednostki_strazy, text="Pokaż szczegóły obiektu", command=lambda: pokaz_szczegoly_uzytkownika(listbox_jednostki_strazy, label_nazwa_szczegoly_obiektu_wartosc, label_miejscowosc_szczegoly_obiektu_wartosc, label_pracownicy_szegoly_obiektu_wartosc))
    button_usun_obiekkt = Button(ramka_jednostki_strazy, text="Usuń obiekt", command=lambda: usun_jednostke(listbox_jednostki_strazy))
    button_edytuj_obiekt = Button(ramka_jednostki_strazy, text="Edytuj obiekt", command=lambda: edytuj_jednostke(listbox_jednostki_strazy, entry_nazwa, entry_miejscowosc, entry_pracownicy, button_dodaj_jednostke))

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

    button_dodaj_jednostke = Button(ramka_formularz, text="Dodaj jednostkę do listy", command=lambda: dodaj_jednostke(entry_nazwa, entry_miejscowosc, entry_pracownicy, listbox_jednostki_strazy))
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

    return(root)

