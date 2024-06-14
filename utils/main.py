from tkinter import *
from tkinter import messagebox
from utils.view import create_jednostki_root,create_pracownicy_root,create_pozary_root, lista_jednostek, dodaj_jednostke, usun_jednostke, edytuj_jednostke, pokaz_szczegoly_uzytkownika, aktualizuj_jednostke, lista_pracownikow, dodaj_pracownika, usun_pracownika, edytuj_pracownika, pokaz_szczegoly_pracownika, aktualizuj_pracownika, lista_pozarow, dodaj_pozar, usun_pozar, aktualizuj_pozar, pokaz_szczegoly_pozaru, edytuj_pozar


class Logowanie:
    def __init__(self, glowneokno):
        self.glowneokno = glowneokno
        glowneokno.title("Panel logowania")
        glowneokno.geometry("300x150")

        self.login_label = Label(glowneokno, text="Login:")
        self.login_label.pack()

        self.login_entry = Entry(glowneokno)
        self.login_entry.pack()
        self.login_entry.focus()

        self.haslo_label = Label(glowneokno, text="Hasło:")
        self.haslo_label.pack()

        self.haslo_entry = Entry(glowneokno, show="*")
        self.haslo_entry.pack()

        self.login_button = Button(glowneokno, text="Zaloguj", command=self.sprawdzaj_login)
        self.login_button.pack()

    def sprawdzaj_login(self):
        login = self.login_entry.get()
        haslo = self.haslo_entry.get()

        loginy = ["Zuzanna", "Marek", "Artur", "Marysia"]
        hasla = ["Straz1", "Straz2", "Straz3", "Straz4"]

        if login in loginy:
            if haslo == hasla[loginy.index(login)]:
                self.glowneokno.destroy()
                self.opcje()
            else:
                messagebox.showerror("Błąd", "Błędne hasło")
        else:
            messagebox.showerror("Błąd", "Nie ma takiego użytkownika")
            self.login_entry.focus()

    def opcje(self):
        root = Tk()
        root.title("Baza")
        root.geometry("200x200")

        label = Label(root, text="Wybierz opcję:")
        label.pack()
        button_jednostki = Button(root, text="Jednostki straży pożarnej",
                                  command=lambda: create_jednostki_root(root))
        button_jednostki.pack()
        button_pracownicy = Button(root, text="Pracownicy straży pożarnej",
                                   command=lambda: create_pracownicy_root(root))
        button_pracownicy.pack()
        button_lokalizacje = Button(root, text="Lokalizacje pożarów",
                                    command=lambda: create_pozary_root(root))
        button_lokalizacje.pack()

        root.mainloop()

root = Tk()
moje_logowanie= Logowanie(root)
root.mainloop()
