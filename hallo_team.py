#Streaming Datenbanken
#Das Pythong Programm dient als einen Streaming-Dienst-System, in dem Nutzer ein ABo besitzen und Filme auf ihrer Wathchlist
#21.05.2026


import sqlite3
import tkinter as tk
from tkinter import messagebox

#1. DATENBANK DIENST-FUNKTIONEN

def hole_alle_nutzer():
    # Verbindung öffnen, Daten holen, Verbindung schließen
    connection = sqlite3.connect("streaming.db")
    cursor = connection.cursor()
    