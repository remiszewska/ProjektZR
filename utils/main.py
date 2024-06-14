from tkinter import *
from tkinter import messagebox


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

        root.mainloop()

root = Tk()
moje_logowanie= Logowanie(root)
root.mainloop()
