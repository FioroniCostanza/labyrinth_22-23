# Labirinto

Progetto finale del corso di Programmazione a.a. 2022-2023.

Il programma è in grado di calcolare il percorso a peso minimo del labirinto da un determinato punto di partenza, restituendo a parità di costo , il percorso di lunghezza minima.

## Cosa inserire in Input?
Il progetto è stato realizzato per accettare i seguenti formati:

- TIFF
- JPEG
- PNG
- JSON

Per quanto riguarda i formati TIFF, JPEG e PNG il codice elabora l'immagine inserita e la converte in una matrice che rappresenti il labirinto, utilizzando il colore RGB dei pixels (i colori bianco e grigio sono percorribili, mentre il nero no).

Nel caso di un file in formato JSON viene creata la matrice partendo dalle informazioni all'interno del file, che contengono le seguenti caratteristiche del labirinto:

- "larghezza": un numero che indica il numero di posizioni 
    lungo la dimensione orizzontale;
- "altezza": un numero che indica il numero di posizioni 
    lungo la dimensione verticale;
- "pareti": una lista di *segmenti*, ogni 
segmento costituito da un dizionario con chiavi: 
    - "orientamento": "H" per orizzontale, "V" per verticale;
    - "posizione": un coppia di indici che indicano una posizione 
    "iniziale" (per 
    convenzione il segmento si estende in 
    orizzontale da sinistra verso destra e 
    in verticale dall'alto verso il basso);
    - "lunghezza": un numero che indica il numero 
    di posizioni occupate dal segmento;
- "iniziali": una lista di coppie di indici che 
indicano ciascuno una posizione di partenza;
- "finale": una coppia di indici che indica la 
posizione di arrivo;
- "costi": una lista di *posizioni con costo*,
che sono triple costituite da una coppia di indici che indicano 
    una posizione e un valore intero da 1 a 15 che indica il costo. 
    
### Esempio di input:
Una volta avviato il codice viene richiesto di inserire il percorso del file da elaborare:

    Inserisci il percorso del file (.json/.tiff/.png/.jpeg): 

scelta l'immagine/il file JSON basta inserire il percorso associato al file: (Sia assoluto che relativo)
```console  
/Users/utente/Desktop/labyrinth_22-23/indata/30-20_marked.jpeg
```
In questo caso abbiamo scelto l'immagine 30-20_marked.jpeg.

##  Cosa restituisce in Output?  
Dopo aver inserito un'immagine (TIFF, JPEG, PNG) rappresentante un labirinto da analizzare o un file JSON contenente le caratteristiche di tale labirinto, viene fornito il percorso più berve e di costo minore tramite:

- un'immagine (la stessa immagine data in input) con lo stesso formato d'ingresso (TIFF, JPEG, PNG) per ciascun punto di partenza, dove per ogni partenza viene sovrascritto il percorso trovato in colori differenti;
- una Gif per ciascun punto di partenza, dove viene mostrato frame per frame l'intero percorso;
- un file JSON che contiene un dizionario con le seguenti chiavi:
 
  - "start": coordinate del punto di partenza
  - "end": coordinate del punto di fine 
  - "lenght": lunghezza totale del percorso più breve
  - "weight": peso 

Se non si ha nemmeno un percorso possibile partendo dalla posizione di partenza indicata, nel file JSON verrà resituito il seguente messaggio "Nessun percorso possibile dalla posizione di partenza selezionata".

Tutti i risutati possono essere visionati nella directory 'Percorsi'. 
Ogni file in uscita in formato TIFF, JPEG e PNG è stato rinominato aggiungendo al nome iniziale '_path_' + 'n° riferito alla casella di partenza', mentre per quanto riguarda il file JSON viene rinominato semplicemente aggiungendo 'path_info'.

### Esempio
Partendo dall'esempio precedente, l'immagine fornita ha due punti di partenza, quindi nella directory 'Percorsi' saranno presenti due immagini JPEG e un file JSON, come segue:
- 30-20_marked_path_1.jpeg
- 30-20_marked_path_2.jpeg
- 30-20_marked_path_info.json

