# Emedia
Projekt na przedmiot E-media dotyczący analizy pliku BMP.
Głównym celem projektu był "ręczne" odczytanie metadanych znajdujących się w nagłówkach pliku, 
wykonanie transformaty Fouriera na obrazie oraz wyświetlenia uzyskanych informacji w
postaci wykresu modułu widma oraz fazy. Ponadto należało dokonać odczytu tablicy kolorów, 
profilu kolorów ICC oraz zaprezentowania ich w czytelny, graficzny sposób. 
Plik musiał zostać także poddany anonimizacji mającej na celu usunięcie zbędnych informacji
o pliku, usunięcie bajtów znajdującyh się poza końcem obrazu oraz usunięcie danych, które mogłyby byż szkodliwe. 
Program był testowany dla plików BMP o nagłówkach DIB: BITMAPINFOHEADER, BITMAPV4HEADER oraz BITMAPV5HEADER.
Implementacja programu została wykonana w języku Python3.
