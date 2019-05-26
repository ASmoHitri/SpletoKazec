# SPLETO KAZEC

## Navodila za zagon
+ Requirements: bs4, nltk (glej requirements.txt)
  namestitev: `pip3 install -r requirements.txt`  
  Ker modul nltk nima vključenih slovenskih stopwordov, je pred samim indeksiranjem modulu treba dodati stopworde, ki se 
  nahajajo v *data/slovenian*. (To datoteko se lahko skopira v mapo */Users/\<User>/nltk_data/corpora/stopwords* (macOS) 
  oziroma *C:\Users\\\<user>\AppData\Roaming\nltk_data\corpora\stopwords* (Windows).  
  
Skripti za indeksiranje in pridobivanje rezultatov poizvedb se nahajata v mapi *indexer*.

Pred klicem skripte, je treba preveriti in po potrebi popraviti konfiguracijske vrednosti v *indexer/config.py*. Parametri:
+ *db_file* - pot do datoteke, kamor naj se shranjujejo SQLite podatki  
+ *data_path* - pot do mape, kjer se v podmapah nahajajo HTML datoteke, ki jih želimo indeksirati
  
Klic skripte za indeksiranje:  `py indexing.py`  
Pri pridobivanju rezultatov poizvedbe lahko uporabimo pridobivanje s pomočjo baze in predhodnega indeksiranja ali pa
z zaporednim pregledovanjem datotek.  
+ Klic skripte za pridobivanje rezultatov poizvedbe z uporabo obratnega indeksa: `py data_retrieval <poizvedba>`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Primer klica za poizvedbo "ministrstvo poročati": `py data_retrieval "ministrstvo poročati"`
+ Klic skripte za pridobivanje rezultatov poizvedbe brez uporabe obratnega indeksa: `py data_retrieval <poizvedba> sequential`
