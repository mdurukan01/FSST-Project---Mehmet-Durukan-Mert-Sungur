#Streaming Datenbanken
#Das Pythong Programm dient als einen Streaming-Dienst-System, in dem Nutzer ein ABo besitzen und Filme auf ihrer Wathchlist
#28.05.2026
 
 
import sqlite3 #Importiert das Modul für die SQLite-Datenbankverwaltung
import tkinter as tk #Importiert das Tkinter-Modul. Ist für die Erstellung der grafischen Benutzoberfläche also für die GUI unter dem Kürzel 'tk' 
from tkinter import messagebox #importiert die messagebox-untermodul von Tkinter, damit man Pop-up Meldungen wie Hinweise und Fehler anzuzeigen

#1. DATENBANK INITIALISIERUNG
def datenbank_einrichten():
    connection = sqlite3.connect("streaming.db")#Verbindung zur SQL-Datenbankdatei "streaming.db"
    cursor = connection.cursor() #Ein cursor Objekt wird erstellt um SQL- Befehle auszuführen

    #Erstellt die Tabelle 'Nutzer', falls sie in der Datei noch fehlt mit den Spalten E_Mail, Passwort und Nutzername
    cursor.execute("""

    CREATE TABLE IF NOT EXISTS Nutzer (

        E_Mail TEXT PRIMARY KEY,

        Passwort TEXT,

        Nutzername TEXT

    );

    """)

    connection.commit() #Speichert die Änderungen dauerhaft in der Datenbank ab

    connection.close() #Schließt die Verbindung zu Datenbank
 
datenbank_einrichten() #Ruft die Einrichtung direkt beim Start auf
 
 
def hole_alle_nutzer():
    #Verbindung öffnen, Daten holen, Verbindung schließen
    connection = sqlite3.connect("streaming.db")
    cursor = connection.cursor() #Erstellt ein Cursor-Objekt, damit man SQL-Befehle auf der Datenbank ausführen kannst

    #FÜhrt einen SQL-Befehl aus, um die Spalten "Nutzername" und "E_Mail" aus der Tabelle "Nutzer" zu lesen
    cursor.execute("SELECT Nutzername, E_Mail FROM Nutzer;")

    #Holt alle Zeilen, die das Ergebnis der SQL-Abfrage zurückgibt, und speichert sie in der Variable "daten"
    daten = cursor.fetchall()

    #Schließt die Verbindung zu Datenbank
    connection.close()
    return daten #An den Aufrufer der Funktion zurück 

def nutzer_speichern(email, passwort, name):
    connection = sqlite3.connect("streaming.db") #Verbindung zur SQL-Datenbankdatei "streaming.db"
    cursor = connection.cursor() #Ein cursor Objekt wird erstellt um S"L- Befehle auszuführen
    cursor.execute("PRAGMA foreign_keys = ON;") #Es wird ein Fremdschlüssel-Unterstützung (Foreign Keys) in SQLite für diese Verbindung


    #Neuen Nutzer in die Tabelle einfügen
    try:
        #Führt den SQL-Befehl aus, um die übergebenen Daten sicher in die Tabelle "Nutzer" einzufügen
        cursor.execute("INSERT INTO Nutzer (E_Mail, Passwort, Nutzername) VALUES (?, ?, ?);", (email, passwort, name))
        connection.commit() #Speichert die Änderungen dauerhaft in der Datenbank ab
        messagebox.showinfo("Erfolg", "Nutzer wurde in der Datenbank gespeichert!")

    except:
        #Wenn ein Fehler auftritt wie zum Beispiel dass die E-Mail schon existiert wird eine Fehlermeldung angezeigt
        messagebox.showerror("Fehler", "E-Mail existiert bereits oder Eingabe fehlerhaft!")
        
    connection.close()#Schließt die Verbindung zu Datenbank 


#2. GUI ENTWICKLUNG einfaches Tkinter-Fenster
 


#Hauptfenster erstellen
app = tk.Tk() #Erstellt das Hauptfenster der Anwendung als Basis für alle GUI-Elemente
app.title("Streaming Dienst - Datenbank Verwaltung") #Setzt den Titel des Hauptfensters, der ganz oben in der Leiste angezeigt wird
app.geometry("400x450") #Legt die feste Startgröße des Fensters auf eine Breite von 400 und eine Höhe von 450 Pixeln fest

#FUNKTIONEN FÜR DIE BUTTONS 

def button_anzeigen_klick():
    #Liste leeren, bevor wir neue Daten anzeigen
    text_anzeige.delete("1.0", tk.END) #Löscht den gesamten aktuellen Text im Textfeld von der ersten Zeile bis zum Ende

    #Daten aus der Datenbank holen
    nutzer_liste = hole_alle_nutzer()

    #Mit einer einfachen Schleife in das Textfeld schreiben
    for nutzer in nutzer_liste: #Geht jede Zeile der zurückgegebenen Nutzerdaten einzeln durch
        text_anzeige.insert(tk.END, f"Name: {nutzer[0]} | E-Mail: {nutzer[1]}\n") #Fügt den Namen und die E-Mail des Nutzers formatiert am Ende des Textfelds hinzu

def button_speichern_klick():
    #Text aus den Eingabefeldern auslesen
    email = entry_email.get()
    passwort = entry_passwort.get()
    name = entry_name.get()

    #Prüfen, ob die Felder leer sind
    if email == "" or passwort == "" or name == "":
        messagebox.showwarning("Achtung", "Bitte alle Felder ausfüllen!") #Zeigt ein Warnungs-Pop-up an, falls eines der Pflichtfelder nicht ausgefüllt wurde

    else:
        #Funktion von oben aufrufen
        nutzer_speichern(email, passwort, name)

        # #Eingabefelder wieder leeren
        entry_email.delete(0, tk.END) #Löscht den Inhalt des E-Mail-Eingabefelds, damit es wieder frei ist
        entry_passwort.delete(0, tk.END) #Löscht den Inhalt des Passwort-Eingabefelds, damit es wieder frei ist
        entry_name.delete(0, tk.END) #Löscht den Inhalt des Namens-Eingabefelds, damit es wieder frei ist


#GUI ELEMENTE Beschriftungen und Textfelder
        
#Überschrift
label_titel = tk.Label(app, text="Nutzer hinzufügen", font=("Arial", 14, "bold")) #Erstellt ein Label für die Hauptüberschrift mit fetter Schriftart
label_titel.pack(pady=10) #Platziert das Label im Fenster mit einem Abstand nach oben und unten

#Eingabe: E-Mail
label_email = tk.Label(app, text="E-Mail-Adresse:") #Erstellt ein Label für die E-Mail Beschriftung
label_email.pack() #Platziert das Label im Fenster
entry_email = tk.Entry(app, width=30) #Erstellt ein Eingabefeld für die E-Mail-Adresse mit einer Breite von 30
entry_email.pack(pady=2) #Platziert das Eingabefeld im Fenster mit kleinem Abstand

#Eingabe: Passwort
label_passwort = tk.Label(app, text="Passwort:") #Erstellt ein Label für die Passwort Beschriftung
label_passwort.pack() #Platziert das Label im Fenster
entry_passwort = tk.Entry(app, width=30, show="*") #show="*" versteckt das Passwort
entry_passwort.pack(pady=2) #Platziert das Eingabefeld im Fenster mit kleinem Abstand

#Eingabe: Nutzername
label_name = tk.Label(app, text="Nutzername:") #Erstellt ein Label für die Nutzername Beschriftung
label_name.pack() #Platziert das Label im Fenster
entry_name = tk.Entry(app, width=30) #Erstellt ein Eingabefeld für den Nutzernamen mit einer Breite von 30
entry_name.pack(pady=2) #Platziert das Eingabefeld im Fenster mit kleinem Abstand

#Button zum Speichern
btn_speichern = tk.Button(app, text="In Datenbank speichern", command=button_speichern_klick, bg="lightgreen")#Erstellt den Speicher-Button in hellgrün und verknüpft ihn mit der Klick-Funktion
btn_speichern.pack(pady=15) #Platziert den Button im Fenster mit einem Abstand von 15 Pixeln

#Button zum Nutzer anzeigen
btn_anzeigen = tk.Button(app, text="Nutzer aus Datenbank laden", command=button_anzeigen_klick, bg="lightblue")#Erstellt den Laden-Button in hellblau und verknüpft ihn mit der Klick-Funktion
btn_anzeigen.pack(pady=5) #Platziert den Button im Fenster mit kleinem Abstand

#Textfeld für die Ausgabe der Daten
text_anzeige = tk.Text(app, width=45, height=8) #Erstellt ein großes mehrzeiliges Textfeld für die Anzeige der geladenen Nutzerdaten
text_anzeige.pack(pady=10) #Platziert das Textfeld im Fenster mit Abstand nach oben und unten


#Startet die GUI-Anwendung
app.mainloop() #Hält das Fenster geöffnet und wartet auf Benutzereingaben

 