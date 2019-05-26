# SPLETO KAZEC

## Navodila za zagon

#### Requirements
Namestitev: `pip3 install -r requirements.txt`  
+ bs4  
+ nltk  
  Ker modul *nltk* nima vključenih slovenskih stopwordov, je pred samim indeksiranjem modulu treba dodati stopworde, ki se 
  nahajajo v *data/slovenian* (to datoteko se lahko skopira v mapo */Users/\<User>/nltk_data/corpora/stopwords* (macOS) 
  oziroma *C:\Users\\\<user>\AppData\Roaming\nltk_data\corpora\stopwords* (Windows).  
  
### Klicanje skript
Skripti za indeksiranje in pridobivanje rezultatov poizvedb se nahajata v mapi *indexer*.

Pred klicem skripte, je treba preveriti in po potrebi popraviti konfiguracijske vrednosti v *indexer/config.py*. Parametri:
+ *db_file* - pot do datoteke, kamor naj se shranjujejo SQLite podatki  
+ *data_path* - pot do mape, kjer se v podmapah nahajajo HTML datoteke, ki jih želimo indeksirati
  
#### Indeksiranje
Klic skripte za indeksiranje:  `py indexing.py`  

#### Rezultati poizvedb
Pri pridobivanju rezultatov poizvedbe lahko uporabimo pridobivanje s pomočjo baze in predhodnega indeksiranja ali pa
z zaporednim pregledovanjem datotek.  
+ Klic skripte za pridobivanje rezultatov poizvedbe __z uporabo obratnega indeksa__: `py data_retrieval <poizvedba>`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Primer klica za poizvedbo "ministrstvo poročati": `py data_retrieval "ministrstvo poročati"`
+ Klic skripte za pridobivanje rezultatov poizvedbe __brez uporabe obratnega indeksa__: `py data_retrieval <poizvedba> sequential`
