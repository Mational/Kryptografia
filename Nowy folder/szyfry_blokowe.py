import time
from Cryptodome.Cipher import AES


# padding- dostosowanie bloku do odpowiedniego rozmiaru uzywanego przez AES
def padding(data):
    # wyznaczamy dlugosc wypelnienia: roznica miedzy rozmiarem bloku AES, a reszta z dzielenia dlugosci danych przez rozmiar bloku AES
    length = AES.block_size - (len(data) % AES.block_size)
    return data + bytes([length] * length) # do danych dodajemy tyle bajtow o wartosci rownej dlugosci wypelnienia, aby byla wielokrotnoscia rozmiaru bloku AES

# odwrotnosc paddingu
def unpadding(data):
    # przyjmuje dane wejsciowe w postaci bajtow, odczytuje ostatni bajt z danych
    length = data[-1]

    # zwraca dane bez wartosci ostatniego bajtu w danych
    return data[:-length]

# code - szyfr
# szyfrowanie w trybie ECB
def ecb_encryption(key, iv, input_data): # przyjmuje klucz, wektor inicjalizacji i dane do zaszyfrowania
    # tworzymy nowy obiekt z kluczem i trybem ECB
    code = AES.new(key, AES.MODE_ECB)
    # zaszyfrowujemy dane wejsciowe, szyfrogram jest zwracany jako wynik funkcji
    return code.encrypt(padding(input_data))

# deszyfrowanie w trybie ECB
def ecb_decryption(key, iv, ciphertext):  # klucz, wektor, dane zaszyfrowane
    # nowy obiekt deszyfrujacy z kluczem i trybem ECB
    code = AES.new(key, AES.MODE_ECB)
    # przekazujemy dane do funkcji, ktora usuwa wypelnienie dodane przez funkcje padding przed zaszyfrowaniem
    # zwraca odszyfrowane wypelnienia
    return unpadding(code.decrypt(ciphertext))


# szyfrowanie w trybie cbc
def cbc_encryption(key, iv, input_data):
    # nowy obiekt szyfrujacy z kluczem w trybie ecb
    code = AES.new(key, AES.MODE_ECB)
    # inicjacja zmiennej jako pusty ciag bajtow
    ciphertext = b''
    # inicjacja zmiennej jako wektoe inicjacji
    prev_block = iv

    # iteracja po danych wejsciowych w blokach o dlugosci block_size
    for i in range(0, len(input_data), AES.block_size):
        # tworzymy blok wypelniony danymi wejsciowymi
        block = input_data[i:i + AES.block_size]
        # jesli dlugosc bloku danych wejsciowych jest mniejsza od block_size
        if len(block) < AES.block_size:
            # to wtedy blok uzupelniany jest zerami na koncu za pomoca funkcji ljust
            block = block.ljust(AES.block_size, b'\x00')
        # xorujemy blok z poprzednim zaszyfrowanym blokiem danych, czyli z wartoscia prev_block
        block = bytes([block[j] ^ prev_block[j] for j in range(AES.block_size)])
        # wynikowy blok jest szyfrowany
        encrypted_block = code.encrypt(block)
        # zaszyfrowany blok dodajemy do zmiennej
        ciphertext += encrypted_block
        # poprzedni blok danych jest ustawiany na blok wynikowy
        prev_block = encrypted_block
    # zwracamy dane zaszyfrowane
    return ciphertext

# deszyfrowanie w trybie cbc
def cbc_decryption(key, iv, ciphertext):
    code = AES.new(key, AES.MODE_ECB)
    plaintext = b''
    prev_block = iv
    # funkcja iteruje po danych wejsciowych w blokach o dlugosci block_size
    for i in range(0, len(ciphertext), AES.block_size):
        # tworzymy blok wypelniony danymi juz zaszyfrowanymi
        block = ciphertext[i:i+AES.block_size]
        # deszyfrujemy blok danych
        decrypted_block = code.decrypt(block)
        # xorujemy z poprzednim  zaszyfrowanym blokiem danych
        plaintext_block = bytes([decrypted_block[j] ^ prev_block[j] for j in range(AES.block_size)])
        # wynikowy blok dodawany do zmiennej
        plaintext += plaintext_block
        # poprzedni blok ustawiany na biezacy zaszyfrowany blok block
        prev_block = block
    # usuwamy uzupelnienie z ciagu bajtow plaintext
    plaintext = plaintext.rstrip(b'\x00')
    # zwracamy dane zdeszyfrowane
    return plaintext

# szyfrowanie w trybie OFB
def ofb_encryption(key, iv, input_data):
    # nowy obiekt z kluczem, trybem ofb i wektorem inicjalizacji
    # nastepnie wywoluje funkcje padding dla danych wejsciowych, aby wypelnic dane do wielokrotnosci dlugosci bloku AES
    code = AES.new(key, AES.MODE_OFB, iv=iv)
    return code.encrypt(padding(input_data))

# deszyfrowanie w trybie OFB
def ofb_decryption(key, iv, ciphertext):
    code = AES.new(key, AES.MODE_OFB, iv=iv)
    return unpadding(code.decrypt(ciphertext))

# szyfrowanie w trybie cfb
def cfb_encryption(key, iv, input_data):
    code = AES.new(key, AES.MODE_CFB, iv=iv, segment_size=128)
    return code.encrypt(padding(input_data))

# deszyfrowanie w trybie cfb
def cfb_decryption(key, iv, ciphertext):
    code = AES.new(key, AES.MODE_CFB, iv=iv, segment_size=128) # rozmiar segmentu 128 bitów
    return unpadding(code.decrypt(ciphertext))

# szyfrowanie w trybie ctr
def ctr_encryption(key, iv, input_data):
    code = AES.new(key, AES.MODE_CTR, nonce=iv[:8]) # nonce- wartosc niezbedna do inicjalizacji licznika, jednorazowa wartość
    return code.encrypt(padding(input_data))

# deszyfrowanie w trybie ctr
def ctr_decryption(key, iv, ciphertext):
    code = AES.new(key, AES.MODE_CTR, nonce=iv[:8])
    return unpadding(code.decrypt(ciphertext))


if __name__ == '__main__':
    # klucz
    key = b"abcdefghijklmnopqrstuvwxyz012345"
    # wektor inicjalizacji
    iv = b"0123456789abcdef"

    files = [""]
    # wczytywanie plikow
    with open("25_bytes.txt", "rb") as f:
        small_plaintext = f.read()
    with open("64_bytes.txt", "rb") as f:
        medium_plaintext = f.read()
    with open("150_bytes.txt", "rb") as f:
        large_plaintext = f.read()

    # etykiety
    sizes = [("small", small_plaintext), ("medium", medium_plaintext), ("large", large_plaintext)]

    for mode in ["ECB", "CBC", "OFB", "CFB", "CTR"]:
        print(f"Tryb: {mode}")
        for size in sizes:
            name, input_data = size
            print(f"Rozmiar: {name}")
            # mierzymy czas szyfrowania wiadomosci
            start_time = time.perf_counter()
            ciphertext = globals()[f"{mode.lower()}_encryption"](key, iv, input_data)
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            print(f"Czas szyfrowania: {execution_time} sek")

            # mierzymy czas deszyfrowania wiadomosci
            start_time = time.perf_counter()
            decrypted_text = globals()[f"{mode.lower()}_decryption"](key, iv, ciphertext)
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            print(f"Czas deszyfrowania: {execution_time} sek\n")

            assert decrypted_text == input_data

