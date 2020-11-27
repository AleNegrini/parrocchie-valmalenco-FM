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

Ciascuna parrocchia è dotata di un _NVR_, in cui confluiscono immagine e audio trasmessi dalle relative videocamere. 

Il protocollo streaming utilizzato da ciascuna videocamera è _rtsp_. 

## Schema logico
![Parrocchie Network](https://github.com/AleNegrini/parrocchie-valmalenco-FM/blob/develop/schema/architettura.png)

## Obiettivo