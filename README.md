# Parrocchie Valmalenco FM

Tutte le parrocchie della Valmalenco sono state cablate in un'unica rete intranet.
Sei sono le chiese attualmente collegate nell'intranet parrocchiale: 
- Chiesa in Valmalenco
- Caspoggio
- Lanzada
- Primolo
- Torre S.Maria
- Spriana

Ogni parrocchia, è dotata di un sistema di videosorveglianza. 

Ogni sistema di sorveglianza è composto da sei IP cam, cinque di queste si occupano solamente di fare streaming 
video (no audio), la sesta invece, oltre a trasmettere il video, è collegata al sistema audio della 
chiesa, per cui trasmette anche l'audio via rete. 
Lo stesso audio viene trasmesso in rete anche da un Ethernet MP3 Broadcaster. La peculiarità di questo dispositivo è che 
è allineato al sistema di alimentazione dell'amplicatore: se l'amplicatore è spento sarà spento, se l'amplificatore è acceso, sarà acceso. 

Ciascuna parrocchia è dotata di un _NVR_, in cui confluiscono immagine e audio trasmessi dalle relative videocamere. 

Il protocollo streaming utilizzato da ciascuna videocamera è _rtsp_, mentre del dispositivo Broadcast MP3 è _http_ 

## Architettura logica
![Parrocchie Network](https://github.com/AleNegrini/parrocchie-valmalenco-FM/blob/develop/schema/architettura.png)

## Obiettivo
Attualmente le celebrazioni vengono trasmesse in radio in maniera manuale. 

L'obiettivo è quello di sviluppare una soluzione in grado di rendere l'intero processo completamente automatico, secondo 
un calendario di celebrazioni dato in input.

Rispetto alla versione 1.x del software, questa versione ha l'obiettivo di limitare il più possibile gli "spazi bianchi" in radio (frequenza 98.4Mhz). 
Nella soluzione precedente, infatti, l'evento di **Inizio trasmissione** e di **Fine trasmissione** in radio era totalmente gestito
dall'orario di partenza e dall'orario di fine della celebrazione. 
Ci si è rapidamente resi conto però che, sebbene l'orario di inizio sia piuttosto affidabile, l'orario di fine è molto più variabile: 
1) a volte la celebrazione termina prima dell'orario previsto, lasciando un lungo momento in radio di silenzio
2) a volte la celebrazione termina oltre l'orario previsto, e non viene trasmessa la celebrazione nella sua totalità

## Soluzione
Al fine di soddisfare i requisiti sopra, si è sviluppato uno script python che, dato in ingresso un calendario di 
celebrazioni (_orari.csv_), si occupa di orchestrare l'avvio (e la chiusura) di VLC, come dettagliato sotto. 

Per poter risolvere il problema legato agli spazi bainchi viene utilizzato un evento aggiuntivo (la raggiungibilità del microfono in rete). 
Se il microfono è acceso, sarà acceso anche il broadcast MP3 e sarà visibile in rete. Se il microfono è spento, il broadcast MP3 non sarà visibile in rete. 
Per cui, grazie ad una combinazione della coppia di eventi _orario_ e _raggiungibilità broadcast MP3_, la celebrazione viene trasmessa.

**Evento di start**

La trasmissione è eligibile ad essere mandata in onda, se l'orario attuale si trova tra _l'orario di partenza_ e _l'orario 
di fine massima_. Per poterla mandare in onda, il dispositivo Ethernet MP3 deve però essere raggiungibile in rete.   

**Evento di stop**

Due sono i possibili eventi di stop della trasmissione: 
- il termine massimo di conclusione della celebrazione non è ancora stato raggiunto, ma il dispositivo non è più raggiungibile in rete 
(timeout di connessione di default è 5 secondi)
- il termine massimo di conclusione della celebrazione è stato raggiunto, a prescindere dal fatto se il dispositivo sia raggiungibile o meno. 

### File di input
- il file _config.ini_ (per motivi di sicurezza non è presente nella repository github, vedi _config-sample.ini_) 
contiene le configurazioni relative agli IP e porta per ciascun dispositivo Ethernet che trasmette l'audio per 
ciascuna chiesa
- il file _config-relay.ini_ contiene le configurazioni relative agli IP e porta del relay
- il file _orari.csv_ contiene invece il calendario delle celebrazioni che si vuole trasmettere in radio

### Funzionamento 
In fase di avvio, il programma effettua il parsing del file di configurazione delle telecamere e del relay e verifica se
il formato è corretto. 

Ogni 60 secondi va a verificare se all'interno del file _orari.csv_ ci sono messe da trasmettere. Se non ci sono messe 
da trasmettere, attende 60 secondi ed effettua un nuovo controllo, e così via. 

Se invece, c'è una celebrazione da trasmettere gli step che vengono fatti sono:
- finchè il dispositivo Ethernet MP3 non è raggiungibile in rete, non viene fatto niente e ogni minuto viene rifatto un controllo. 
- appena il dispositivo risulta raggiungibile, VLC viene lanciato da linea di comando:
    1) per prima cosa viene lanciata la sigla che comunica da quale chiesa si sta trasmettendo
    2) poi viene lanciato lo stream, in modalità "Apri rete ...". 
    
L'_URL_ viene costruito dinamicamente in base alla messa che bisogna trasmettere, attivando l'uscita audio del PC. 
Il formato dell'url è: `http://<username>:<password>@<IP>:<PORT>`. 
- come secondo step, è necessario sollecitare un relay che "stacca" il circuito per cui, in assenza di celebrazioni, 
trasmette _Radio Maria_ e "attacca" l'audio in uscita dal PC.
Il relay in oggetto è un "IP Relay", per cui viene essere sollecitato da una chiamata API all'endpoint:
```
http://<IP_relay>/relays.cgi?relay=1
```

Lo stesso succede per lo spegnimento (vedi sopra i due possibili evneti di spegnimento):
- lo script chiude VLC da linea di comando, disattivando l'uscita audio del PC
- viene avviata la sigla di termine trasmissione, relativa a quella chiesa
- il relay, viene ri-sollecitato con la stessa chiamata API. In questo modo, viene "riattaccato" il cicuito per cui
viene trasmessa in radio Radio Maria.

## Startup
Per poter godere di un servizio continuativo, lo script deve essere attivo 24/7. 

Di default, viene lanciato allo startup del pc attraverso un file `activate.bat` che viene lanciato automaticamente a
startup time. 

Qualora di volesse riavviarlo, killare il processo da 'Gestione Risorse' e poi riavviare con:
- se si vuole eseguire in background, navigare all'interno della folder `src` e lanciare: 
```
pythonw main.py
```
- se non si vuole eseguirlo in background, navigare all'interno della folder `src` e lanciare:
```
python main.py
```

## FAQ
### Come aggiungo una celebrazione?
Per aggiungere una celebrazione, è sufficiente aprire il file _orari.csv_ e aggiungere la nuova celebrazione.
 
Il file degli orari può essere modificato in ogni momento, senza la necessità di stoppare il programma, e deve avere il
seguente formato:
```
<comune>,dd/mm/yyyy,hh:mm,hh:mm
```
Il primo campo contiene il nome del comune (caspoggio, lanzada, chiesa_vco, torre, spriana, primolo), il secondo campo
il giorno, il terzo l'orario di partenza, il quarto l'orario massimo entro cui la trasmissione della messa si deve concludere.
 
Ad esempio, per fare in modo che in radio (dalle 8.00) venga trasmessa la celebrazione svolta nella 
chiesa di Caspoggio, basta aggiungere la seguente riga 
```
caspoggio, 22/07/2020, 08:00, 09:00
```

Salva il file, e chiudi.

### Come cambio la configurazione di un dispositivo Ethernet MP3 Broadcast ?
Aprire il file _config.ini_ ed effettuare il cambio di configurazione (cambio IP, cambio user, ...) relativa al comune 
specifico che si vuole cambiare.

Per poter fare in modo che il programma percepisca le nuove configurazioni bisogna riavviare il programma (vedi sezione
_startup_ per maggiori dettagli). 

### Come aggiungo un nuovo dispositivo Ethernet MP3 Broadcast?
L'aggiunta di una nuova telecamera è trasparente. E' sufficiente aprire il file _config.ini_ ed aggiungere le nuove 
configurazioni del dispositivo nel formato:
```
[<nome_comune>]
cam_ip = <ip>
cam_port = <port>
username = <username>
password = <pwd>
```
Per poter fare in modo che il programma percepisca le nuove configurazioni bisogna riavviare il programma (vedi sezione
_startup_ per maggiori dettagli). 

## TODO
- [ ] Gli eventi di start e stop delle celebrazioni devono essere loggate su un file esterno
- [ ] Aggiungere sigla iniziale e sigla finale
- [ ] Aggiungere supporto per celebrazioni a cavallo di due giorni
- [ ] Migliorare la gestione degli errori a runtime
- [ ] Migliorare la gestione dello stato del relay, dopo averlo acceso/spento
- [ ] Sviluppo interfaccia grafica per inserimento nuove celebrazioni in maniera più easy
- [ ] Aggiungere supporto che verifichi che non ci siano celebrazioni sovrapposte
- [ ] Aggiungere possibilità di inserire eventi ricorrenti
- [ ] Salvare calendario celebrazioni su un DB esterno, non più su un file