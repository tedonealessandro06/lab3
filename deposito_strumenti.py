import csv
from operator import attrgetter

class Strumento:
    def __init__(self, codice, tipo, marca, anno_acquisto, valore):
        self.codice = codice
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = anno_acquisto
        self.valore = valore

    def __str__(self):
        return f"{self.codice} - {self.tipo}, {self.marca}, {self.anno_acquisto}, {self.valore} euro"


class Prestito:
    def __init__(self, id_prestito, data, id_strumento, cognome_allievo):
        self.id_prestito = id_prestito
        self.data = data
        self.id_strumento = id_strumento
        self.cognome_allievo = cognome_allievo

    def __str__(self):
        return f"{self.id_prestito} - {self.data}, {self.id_strumento}, {self.cognome_allievo}"


class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        self.nome = nome
        self.responsabile = responsabile
        self.strumenti = {}
        self.prestiti = {}
        self.contatore_prestiti = 0

    def carica_file_strumenti(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for riga in reader:
                if riga: #se riga non vuota
                    strumento = Strumento(riga[0], riga[1], riga[2],int(riga[3]), float(riga[4]))
                    self.strumenti[strumento.codice] = strumento

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        if self.strumenti:
            ultimo_codice = list(self.strumenti.keys())[-1]
            numero = int(ultimo_codice[1:]) + 1
        else:
            numero = 1

        codice = "S" + str(numero)
        strumento = Strumento(codice, tipo, marca, int(anno_acquisto), float(valore))
        self.strumenti[codice] = strumento
        return strumento

    def strumenti_ordinati_per_marca(self):
        return sorted(self.strumenti.values(), key=attrgetter("marca"))


    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        if id_strumento not in self.strumenti:
            raise Exception("Strumento inesistente")

        for prestito in self.prestiti.values():
            if prestito.id_strumento == id_strumento:
                raise Exception("Strumento già in prestito")
        self.contatore_prestiti += 1
        codice = "P" + str(self.contatore_prestiti)
        prestito = Prestito(codice, data, id_strumento, cognome_allievo)
        self.prestiti[codice] = prestito
        return prestito

    def termina_prestito(self, id_prestito):
        if id_prestito not in self.prestiti:
            raise Exception("Prestito inesistente")
        del self.prestiti[id_prestito]