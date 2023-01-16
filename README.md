# Labirinto

Progetto finale del corso di Programmazione a.a. 2022-2023.

Il programma è in grado di calcolare tutti i percorsi possibili del labirinto da un determinato punto di partenza, restituendo solo quelli con un costo minore, mentre nel caso di costi uguali per uno stesso punto d'inizio fornisce il percorso di lunghezza minima. 

La soluzione viene fornita attraverso un’immagine (la stessa che viene data in ingresso) in formato TIFF, dove per ogni punto di partenza viene sovrascritto il percorso trovato in colori differenti.

N.B. Al momento la soluzione non fornisce alcun file JSON che descrive il punteggio associato ad ogni percorso trovato, ovvero:

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

## Esempio
Inserire il path riferito all’immagine che si vuole analizzare:
```console
filepath = “indata/20-10_marked.tiff”
```

Dopodiché per visualizzare il risultato è possibile visitare la cartella Percorsi, dove vengono caricate tutte le immagini riferite alle soluzioni del Labirinto.

