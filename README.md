# Scrap.py - Narzędzie do pobierania słów ze stron internetowych

## Autor
Stworzone przez Przemysław Szmaj z wykorzystaniem AI | [www.ehaker.pl](https://www.ehaker.pl)

## Opis

**Scrap.py** to narzędzie służące do scrapowania (zbierania) słów z podanych stron internetowych. Skrypt pozwala na odwiedzanie stron oraz podstron i zapisanie wszystkich znalezionych słów w pliku tekstowym. Może być używany jako podstawowe narzędzie do analizowania zawartości stron internetowych, np. w celu badania dostępności publicznych informacji czy mapowania dostępnych podstron.

Skrypt automatycznie obsługuje podany URL, dodając protokół (np. `https://`) w przypadku jego braku. W szczególnych przypadkach zamienia protokół `https` na `http`, jeśli strona wymaga dostępu przez nieszyfrowany protokół.

## Funkcjonalności

- **Pobieranie słów z dowolnej strony internetowej**: Skrypt wykorzystuje bibliotekę `requests` do pobierania treści stron internetowych, a następnie parsuje je przy pomocy `BeautifulSoup`.
- **Obsługa podstron**: Narzędzie może odwiedzać określoną liczbę podstron i zbierać słowa z wielu stron powiązanych z początkowym URL-em.
- **Automatyczne dodawanie protokołu**: Jeśli użytkownik nie poda protokołu w adresie URL, skrypt automatycznie doda `https://`, a w niektórych przypadkach zamieni `https://` na `http://`, jeśli strona tego wymaga.
- **Zapis wyników**: Skrypt zapisuje wszystkie znalezione słowa w pliku tekstowym, gdzie nazwa pliku jest generowana na podstawie domeny strony.

## Odpowiedzialność 


- **Autor nie ponosi odpowiedzialności za jakiekolwiek nielegalne lub niewłaściwe użycie tego narzędzia. Narzędzie zostało stworzone wyłącznie do celów edukacyjnych oraz legalnych testów bezpieczeństwa, np. w ramach testów penetracyjnych na własnych zasobach lub za wyraźną zgodą właściciela witryny. Użycie tego narzędzia do działań sprzecznych z prawem może naruszać przepisy dotyczące prywatności, prawa autorskiego i innych regulacji prawnych.

## Wymagania

Do działania skryptu wymagane są następujące biblioteki:

- `requests`
- `beautifulsoup4`
- `pyfiglet`
- `colorama`

Można je zainstalować, używając poniższego polecenia:

```bash
pip install -r requirements.txt
