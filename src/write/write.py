import csv

def write_data(array, output_file):
# Kirjoittaa listan csv-tiedostoon. 
# Args: array (list of lists): Kirjoitettava taulukko, jossa jokainen alilista edustaa yhtä riviä CSV-tiedostossa.output_file (str): CSV-tiedoston nimi tai polku, johon taulukko kirjoitetaan.
# Returns: None

# Yritä kirjoittaa taulukko CSV-tiedostoon
    try:
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(array)
        print(f"Tiedot on onnistuneesti kirjoitettu '{output_file}'-tiedostoon.")
    except IOError:
        print(f"Virhe: CSV-tiedostoa '{output_file}' ei voitu kirjoittaa.")

