#Streaming Datenbanken
#Das Pythong Programm dient als einen Streaming-Dienst-System, in dem Nutzer ein ABo besitzen und Filme auf ihrer Wathchlist
#21.05.2026


import sqlite3 #Importiert das Modul für die SQLite-Datenbankverwaltung
import tkinter as tk #Importiert das Tkinter-Modul. Ist für die Erstellung der grafischen Benutzoberfläche also für die GUI unter dem Kürzel 'tk' 
from tkinter import messagebox #importiert die messagebox-untermodul von Tkinter, damit man Pop-up Meldungen wie Hinweise und Fehler anzuzeigen

#1. DATENBANK DIENST-FUNKTIONEN

def hole_alle_nutzer():
    # Verbindung öffnen, Daten holen, Verbindung schließen
    connection = sqlite3.connect("streaming.db")
    cursor = connection.cursor()#Erstellt ein Cursor-Objekt, damit man SQL-Befehle auf der Datenbank ausführen kannst
    
    #FÜhrt einen SQL-Befehl aus, um die Spalten "Nutzername" und "E_Mail" aus der Tabelle "Nutzer" zu lesen 
    cursor.execute("SELECT Nutzername,E_Mail FROM NUTZER;")
    #Holt alle Zeilen, die das Ergebnis der SQL-Abfrage zurückgibt, und speichert sie in der Variable "daten"
    daten = cursor.fetchall()
    
    #Schließt die Verbindung zu Datenbank 
    connection.close()
    
    return daten# an den Aufrufer der Funktion zurück 

#Eine Neue Funktion wird definiert um einen neuen Nutzer mit E-Mail, Passwort und Name zu speichern 
def nutzer_speichern(email,passwort,name):
    connection = sqlite3.connect("streaming.db")#Verbindung zur SQL-Datenbankdatei "streaming.db"
    cursor = connection.cursor()#Ein cursor Objekt wird erstellt um S"L- Befehle auszuführen
    cursor.execute("PRAGMA foreign_keys = ON;")#Es wird ein Fremdschlüssel-Unterstützung (Foreign Keys) in SQLite für diese Verbindung
    
    
    #Neuen Nutzer in die Tabelle einfügen
    try:
        cursor.execute("INSERT INTO Nutzer VALUES (?, ?, ?);", (email, passwort, name))#Führt den SQL-Befehl aus, um die übergebenen Daten sicher in die Tabelle "Nutzer" einzufügen
        connection.commit()#Speichert die Änderungen dauerhaft in der Datenbank ab
        messagebox.showinfo("erfolg","Nutzer wurde in der Datenbank gespeichert.")
    except:
        messagebox.showinfo("fehler","E-Mail existiert bereits oder Eingabe fehlerhaft.")
    connection.close()#Schließt die Verbindung zu Datenbank 
        
#Jetzt ist der Teil mit der GUI
        
#Hauptfenster erstellen
app = tk.Tk()#Erstellt das Hauptfenster der Anwendung als Basis für alle GUI-Elemente
app.title("Streaming Dienst - Datenbank Verwaltung")#Setzt den Titel des Hauptfensters, der ganz oben in der Leiste angezeigt wird
app.geometry("400x450")#Legt die feste Startgröße des Fensters auf eine Breite von 400 und eine Höhe von 450 Pixeln fest

#Die Funktionen für die Buttons

def button_anzeigen_kklick():
    #Liste leeren, bevor wir neue Daten anzeigen
    text_anzeige.delete("1.0", tk.END)#Löscht den gesamten aktuellen Text im Textfeld von der ersten Zeile bis zum Ende
    #Dat aus der Datenbank holen
    nutzer_liste = hole_alle_nutzer()
    
    # Mit einer einfachen Schleife in das Textfeld schreiben
    for nutzer in nutzer_liste:#Geht jede Zeile der zurückgegebenen Nutzerdaten einzeln durch
        text_anzeige.insert(tk.END, f"Name: {nutzer[0]} | E-Mail: {nutzer[1]}\n")#Fügt den Namen und die E-Mail des Nutzers formatiert am Ende des Textfelds hinzu
 
def button_speichern_klick():
    # Text aus den Eingabefeldern auslesen
    email = entry_email.get()
    passwort = entry_passwort.get()
    name = entry_name.get()
    
    # Prüfen, ob die Felder leer sind
    if email == "" or passwort == "" or name == "":
        messagebox.showwarning("Achtung", "Bitte alle Felder ausfüllen!")#Zeigt ein Warnungs-Pop-up an, falls eines der Pflichtfelder nicht ausgefüllt wurde
    else:
        # Funktion von oben aufrufen
        nutzer_speichern(email, passwort, name)
        
        # Eingabefelder wieder leeren
        entry_email.delete(0, tk.END)#Löscht den Inhalt des E-Mail-Eingabefelds, damit es wieder frei ist
        entry_passwort.delete(0, tk.END)#Löscht den Inhalt des Passwort-Eingabefelds, damit es wieder frei ist
        entry_name.delete(0, tk.END)#Löscht den Inhalt des Namens-Eingabefelds, damit es wieder frei ist