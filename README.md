# Labirinto

Progetto finale del corso di Programmazione a.a. 2022-2023.

Il programma è in grado di calcolare il percorso a peso minimo del labirinto da un determinato punto di partenza, restituendo a parità di costo, il percorso di lunghezza minima.

## Cosa inserire in Input?
Il programma è stato realizzato per accettare in ingresso i seguenti formati:

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
```console  
Inserisci il percorso del file (.json/.tiff/.png/.jpeg): 
```
scelta l'immagine/il file JSON basta inserire il percorso associato al file (sia assoluto che relativo):
``` 
/Users/utente/Desktop/labyrinth_22-23/Labyrinth/indata/30-20_marked.jpeg
```
In questo caso abbiamo scelto l'immagine 30-20_marked.jpeg.

##  Cosa viene restituito in Output?  
Dopo aver inserito un'immagine (TIFF, JPEG, PNG) rappresentante un labirinto da analizzare o un file JSON contenente le caratteristiche di tale labirinto, viene fornito il percorso più berve e di costo minore tramite:

- un'immagine (la stessa immagine data in input) con lo stesso formato d'ingresso (TIFF, JPEG, PNG) per ciascun punto di partenza, dove per ogni partenza viene sovrascritto il percorso trovato in colori differenti;
- una file GIF per ciascun punto di partenza, dove viene mostrato frame per frame l'intero percorso;
- un file JSON che contiene un dizionario con le seguenti chiavi:
 
  - "start": coordinate del punto di partenza
  - "end": coordinate del punto di fine 
  - "lenght": lunghezza totale del percorso più breve
  - "weight": peso 

Se non si ha nemmeno un percorso possibile partendo dalla posizione di partenza indicata, nel file JSON verrà resituito il seguente messaggio "Nessun percorso possibile dalla posizione di partenza selezionata".

Tutti i risutati possono essere visionati nella directory 'Percorsi'. 
Ogni file in uscita in formato TIFF, JPEG e PNG è stato rinominato aggiungendo al nome iniziale '_path_' + 'n° riferito alla casella di partenza', mentre per quanto riguarda il file JSON viene rinominato semplicemente aggiungendo 'path_info'.

### Esempio di output:
Partendo dall'esempio precedente, l'immagine fornita ha due punti di partenza, quindi nella directory 'Percorsi' saranno presenti due immagini JPEG e un file JSON, come segue:

- 30-20_marked_path_1.jpeg

![image](https://user-images.githubusercontent.com/117634064/216378095-1507d4ca-2e57-41a6-b8a6-779f30d53d04.png)

- 30-20_marked_path_2.jpeg

![image](https://user-images.githubusercontent.com/117634064/216377597-c840159f-fb86-4578-b27a-20ac3f419caf.png)

- 30-20_marked_path_info.json
```  
[
    {
        "start": [
            0,
            29
        ],
        "end": [
            21,
            31
        ],
        "length": 64,
        "weight": 63
    },
    {
        "start": [
            19,
            60
        ],
        "end": [
            21,
            31
        ],
        "length": 228,
        "weight": 227
    }
]
```

## Il Dockerfile
Un Dockerfile è l'elemento costitutivo dell'ecosistema Docker, che descrive tutti i passaggi per creare un'immagine Docker. Il flusso di informazioni segue il modello: Dockerfile > immagine Docker > container Docker.

Nel nostro caso il Dockerfile contiene tutte le informazioni per crearsi un'immagine Docker, sviluppando un'ambiente virtuale python, installando i pacchetti necessari specificati in 'requirements.txt' e copiandosi tutti i file appartenenti al progetto. 

### Come si crea un'immagine Docker?
Una volta verificata la posizione del Dockerfile e del file 'requirements.txt', situati prima della cartella contenente il codice per l'elaborazione di un percorso, si puo' utilizzare questo comando:
```  
docker build . -t utente/mymaze:1
```
Il tag **utente/mymaze:1** è un nome generico assegnato all'immagine appena creata, dove **utente** rappresenta colui che ha realizzato l'immagine, **mymaze** è il nome vero e proprio dell'immagine e **1** è la versione.

### Come si esegue un container Docker?
All'interno del Dockerfile è stato specificato che all'avvio del container deve essere eseguito lo script 'main.py' tramite il comando che segue:
```  
CMD ["python", "./main.py"]
```

Per eseguire un container Docker abbiamo inizialmente creato un container fisso, in cui vengono specificati i percorsi della cartella 'indata' e della cartella 'Percorsi', per capire dove prendere i dati in ingresso e posizionare quelli in uscita. 
Il comando utilizzato è il seguente: 
```  
docker container run -a stdin -a stdout -it -v $(pwd)/labyrinth/indata:/usr/src/app/indata -v $(pwd)/labyrinth/Percorsi:/usr/src/app/Percorsi --name labirinto utente/mymaze:1
```
- **$(pwd)/labyrinth/indata** e **$(pwd)/labyrinth/Percorsi** rappresentano i path di riferitimento alle cartelle 'indata' e 'Percorsi' del computer in cui è collegato il container Docker;
- **/usr/src/app/indata** e **/usr/src/app/Percorsi** rappresentano il path delle cartelle virtuali 'indata' e 'Percorsi' presenti nel container;
- **utente/mymaze:1** è l'immagine creata precedentemente;
- **labirinto** è il nome assegnato al container appena eseguito.

Questo comando restituisce come in precedenza il commento:
```console  
Inserisci il percorso del file (.json/.tiff/.png/.jpeg): 
```

Utilizzando un container Docker, bisogna però inserire il path del file virtuale da analizzare, ad esempio: 
``` 
/usr/src/app/indata/30-20_marked.jpeg
```

Per continuare ad eseguire all'interno dello stesso container si può utilizzare:
``` 
docker container start -ai labirinto
```
andando poi ad inserire un nuovo path di un altro file virtuale da analizzare.

### Come visulizzare l'output generato dal container Docker?
Per poter visualizzare se sono stati generati nuovi contenuti nella cartella virtuale 'Percorsi' è possibile utilizzare i comandi:
``` 
docker start labirinto
docker exec -it labirinto /bin/bash
```
che permetteranno l'utilizzo dei comandi linux per spostarsi all'interno della cartella desiderata e visionare direttamente il suo contenuto. 
