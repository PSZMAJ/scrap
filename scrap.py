import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import pyfiglet
from colorama import init, Fore, Style

# Inicjalizacja Colorama
init(autoreset=True)

# Funkcja do generowania napisu ASCII
def display_title():
    title = pyfiglet.figlet_format("scrap.py")
    print(Fore.GREEN + title + Style.RESET_ALL)
    
    # Informacja o autorze
    author_info = "Stworzone przez Przemysław Szmaj | www.ehaker.pl"
    print(Fore.YELLOW + author_info + Style.RESET_ALL)

# Funkcja do pobierania słów z danej strony
def get_words_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Pobieranie całego tekstu z HTML-a
        text = soup.get_text(separator=' ')
        
        # Zwracamy listę słów
        words = text.split()
        return words
    except requests.RequestException as e:
        # Informacje dla osób nietechnicznych
        if e.response:
            status_code = e.response.status_code
            if status_code == 403:
                print(Fore.RED + f"Błąd 403: Odmowa dostępu. Serwer blokuje dostęp do tej strony." + Style.RESET_ALL)
            elif status_code == 404:
                print(Fore.RED + f"Błąd 404: Strona nie została znaleziona." + Style.RESET_ALL)
            elif status_code == 500:
                print(Fore.RED + f"Błąd 500: Błąd serwera. Problem leży po stronie serwera." + Style.RESET_ALL)
            else:
                print(Fore.RED + f"Nieznany błąd {status_code}: {e.response.reason}" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"Błąd sieci: {e}" + Style.RESET_ALL)
        return []

# Funkcja do rekurencyjnego pobierania słów z podstron
def crawl_and_collect_words(start_url, max_pages):
    visited_urls = set()
    words_collected = []
    urls_to_visit = [start_url]
    
    while urls_to_visit and len(visited_urls) < max_pages:
        current_url = urls_to_visit.pop(0)
        
        # Jeśli już odwiedziliśmy ten URL, pomijamy go
        if current_url in visited_urls:
            continue
        
        print(Fore.CYAN + f"Pobieranie słów ze strony: {current_url}" + Style.RESET_ALL)
        
        words = get_words_from_url(current_url)
        words_collected.extend(words)
        
        visited_urls.add(current_url)
        
        # Parsowanie linków do podstron
        try:
            response = requests.get(current_url)
            soup = BeautifulSoup(response.content, "html.parser")
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                # Budowanie pełnego URL-a
                full_url = urljoin(current_url, href)
                
                # Sprawdzanie, czy URL jest w tej samej domenie
                if urlparse(full_url).netloc == urlparse(start_url).netloc and full_url not in visited_urls:
                    urls_to_visit.append(full_url)
        
        except requests.RequestException as e:
            print(Fore.RED + f"Błąd przy parsowaniu strony: {current_url}, {e}" + Style.RESET_ALL)
    
    return words_collected

# Funkcja zapisująca słowa do pliku
def save_words_to_file(words, filename="words.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        for word in words:
            file.write(word + "\n")
    
    print(Fore.GREEN + f"Słowa zostały zapisane do pliku: {filename}" + Style.RESET_ALL)
    print(Fore.YELLOW + f"Liczba zapisanych słów: {len(words)}" + Style.RESET_ALL)

# Funkcja generująca nazwę pliku na podstawie domeny
def generate_filename_from_url(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace('.', '_')
    return f"{domain}.txt"

# Funkcja zmieniająca https na http, jeśli trzeba
def enforce_http_protocol(url):
    if url.startswith("https://"):
        url = "http://" + url[8:]  # Zamienia https:// na http://
        print(Fore.MAGENTA + f"Zmieniono adres URL na: {url}" + Style.RESET_ALL)
    return url

# Funkcja dodająca http:// lub https:// jeśli brak protokołu
def add_protocol_if_missing(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        # Zakładamy domyślnie https, ponieważ większość stron używa obecnie https
        url = "https://" + url
        print(Fore.MAGENTA + f"Dodano brakujący protokół: {url}" + Style.RESET_ALL)
    return url

# Główna funkcja programu
def main():
    # Wyświetlenie napisu na początku programu
    display_title()

    start_url = input(Fore.CYAN + "Podaj URL strony startowej w formacie np. https://www.ehaker.pl: " + Style.RESET_ALL)

    # Dodanie brakującego protokołu, jeśli go nie ma
    start_url = add_protocol_if_missing(start_url)
    
    # Zamiana https na http, jeśli trzeba
    start_url = enforce_http_protocol(start_url)

    max_pages = int(input(Fore.CYAN + "Podaj maksymalną liczbę podstron do odwiedzenia: " + Style.RESET_ALL))
    
    # Pobieranie słów ze stron
    words = crawl_and_collect_words(start_url, max_pages)
    
    # Generowanie nazwy pliku na podstawie URL-a
    filename = generate_filename_from_url(start_url)
    
    # Zapis słów do pliku
    save_words_to_file(words, filename)

if __name__ == "__main__":
    main()
