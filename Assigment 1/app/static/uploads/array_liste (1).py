import numpy as np


class ArrayListe:
    def __init__(self, startkapasitet = 20):
        self.array = np.zeros(startkapasitet, dtype=object)
        self.lengde = 0

    #gir resultatet av len funksjonen
    def __len__(self):
        return self.lengde

    # Kjøretid Theta(n)
    def utvid(self, ny_storrelse=None):
        if ny_storrelse is None:
            ny_storrelse = len(self.array)*2
        ny_array = np.zeros(ny_storrelse, dtype=object)
        for index in range(len(self.array)):
            ny_array[index] = self.array[index]
        self.array = ny_array

    # Legger til element på slutten av lista
    # Kjøretid: Worst case Theta(n) hvis jeg må lage en ny array
    #           Ellers Theta(1)
    # Kjøretid O(1) amortized, O(n) worst case
    def append(self, element):
        if self.lengde >= len(self.array):
            self.utvid()
        self.array[self.lengde] = element
        self.lengde += 1

    # Legger inn det oppgitte elementet på oppgitt indeks, og forskyver alle elementer som ligger
    # etterpå ett hakk bak
    # Best case på slutten O(1)
    # Worst case starten O(n)
    # Gjennomsnitt: Forventningsverdi n/2, O(n)
    def insert(self, indeks, element):
        if self.lengde >= len(self.array):
            self.utvid()
        for index in range(self.lengde-1, indeks-1, -1):
            self.array[index+1] = self.array[index]
        self.array[indeks] = element
        self.lengde += 1

    # Overskriver det som ligger på oppgitt indeks med det oppgitte elementet.
    # Tilsvarer Python liste[indeks] = element
    # Kjøretid Theta(1)
    def put(self, indeks, element):
        self.array[indeks] = element

    # Fjerner første forekomst av oppgitt element
    # Kjøretid Theta(n)
    def remove(self, element):
        index = self.search(element)
        self.delete(index)

    # Fjerner elementet på oppgitt indeks
    # Tilsvarer Python del liste[indeks]
    # Kjøretid er antall elementer som må flyttes
    # Best case siste element O(1)
    # Worst case første element O(n)
    # Gjennomsnitt O(n)
    def delete(self, indeks):
        for i in range(indeks, self.lengde):
            self.array[i] = self.array[i+1]
        self.lengde -= 1

    # Legger alle elementete i oppgitt samling til i lista
    # Kjøretid O(m) best case
    # Kjøretid O(n + m) worst case
    def append_all(self, samling):
        if self.lengde + len(samling) >= len(self.array):
            self.utvid((self.lengde + len(samling))*2)
        for element in samling:
            self.append(element)

    # Setter inn den oppgitte samlingen på oppgitt indeks, og forskyver alt som ligger bak
    # Kjøretid som en flytting + lengden til den nye lista
    def insert_all(self, indeks, samling):
        if self.lengde + len(samling) >= len(self.array):
            self.utvid((self.lengde + len(samling))*2)
        for i in range(self.lengde-1, indeks-1, -1):
            self.array[i+len(samling)] = self.array[i]
        for i in range(len(samling)):
            self.array[indeks+i] = samling[i]

    # Returnerer elementet på oppgitt indeks.
    # Tilsvarer Python variabel = liste[indeks]
    # Kjøretid Theta(1)
    def get(self, indeks):
        return self.array[indeks]

    # Finner første indeks hvor dette elementet forekommer
    # Kjøretid som sekvensielt søk
    def search(self, element):
        for index in range(self.lengde):  # Kjører maks n ganger
            if element == self.array[index]:  # Kjører maks n ganger
                return index  # Kjører maks 1 gang
        return -1  # Kjører maks 1 gang

    # Gå gjennom lista, element for element
    def __iter__(self):
        return ArrayListIterator(self)

    # Python spesialmetoder slik at array-lista kan brukes som en Python liste. Ikke forelest siden
    # det ikke er en sentral del av faget DAT200.
    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        self.put(key, value)

    def __contains__(self, item):
        if self.search(item) != -1:
            return True
        return False

    def __delitem__(self, key):
        self.delete(key)

    # Implementerer "+" operatoren, og viser hva den gjør for lister.
    def __add__(self, liste):
        self.append_all(liste)


class ArrayListIterator:
    def __init__(self, lista):
        self.lista = lista
        self.nv_element = 0

    def __next__(self):
        if self.nv_element >= len(self.lista):
            raise StopIteration
        resultat = self.lista.get(self.nv_element)
        self.nv_element += 1
        return resultat


if __name__ == "__main__":
    liste = ArrayListe(5)
    liste.append(6)
    liste.append(9)
    liste.append(-2)
    liste.insert(0, -5)
    liste.insert(3, -8)
    liste.append(5)
    liste.append(7)
    print(liste.get(2))
    print(liste.search(5))
    print()
    for element in liste:
        print(element)
    print()
    liste.remove(9)
    liste.delete(1)
    for element in liste:
        print(element)
