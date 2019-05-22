import bs4
import nltk
import re
# from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

nltk.download('stopwords')
# v dir /Users/<User>/nltk_data/corpora/stopwords dodaj datoteko slovenian iz folderja data
stop_words_slovene = set(stopwords.words("slovenian")).union(
    {"ter", "nov", "novo", "nova", "zato", "še", "zaradi", "a", "ali", "april", "avgust", "b", "bi", "bil", "bila",
     "bile", "bili", "bilo", "biti", "blizu", "bo", "bodo", "bojo", "bolj", "bom", "bomo", "boste", "bova", "boš", "brez",
     "c", "cel", "cela", "celi", "celo", "d", "da", "daleč", "dan", "danes", "datum", "december", "deset", "deseta",
     "deseti", "deseto", "devet", "deveta", "deveti", "deveto", "do", "dober", "dobra", "dobri", "dobro", "dokler", "dol",
     "dolg", "dolga", "dolgi", "dovolj", "drug", "druga", "drugi", "drugo", "dva", "dve", "e", "eden", "en", "ena", "ene",
     "eni", "enkrat", "eno", "etc.", "f", "februar", "g", "g.", "ga", "ga.", "gor", "gospa", "gospod", "h", "halo",
     "i", "idr.", "ii", "iii", "in", "iv", "ix", "iz", "j", "januar", "jaz", "je", "ji", "jih", "jim", "jo",
     "julij", "junij", "jutri", "k", "kadarkoli", "kaj", "kajti", "kako", "kakor", "kamor", "kamorkoli", "kar",
     "karkoli", "katerikoli", "kdaj", "kdo", "kdorkoli", "ker", "ki", "kje", "kjer", "kjerkoli", "ko", "koder",
     "koderkoli", "koga", "komu", "kot", "kratek", "kratka", "kratke", "kratki", "l", "lahka", "lahke", "lahki",
     "lahko", "le", "lep", "lepa", "lepe", "lepi", "lepo", "leto", "m", "maj", "majhen", "majhna", "majhni",
     "malce", "malo", "manj", "marec", "me", "med", "medtem", "mene", "mesec", "mi", "midva", "midve", "mnogo",
     "moj", "moja", "moje", "mora", "morajo", "moram", "moramo", "morate", "moraš", "morem", "mu", "n", "na", "nad",
     "naj", "najina", "najino", "najmanj", "naju", "največ", "nam", "narobe", "nas", "nato", "nazaj", "naš", "naša",
     "naše", "ne", "nedavno", "nedelja", "nek", "neka", "nekaj", "nekatere", "nekateri", "nekatero", "nekdo",
     "neke", "nekega", "neki", "nekje", "neko", "nekoga", "nekoč", "ni", "nikamor", "nikdar", "nikjer", "nikoli",
     "nič", "nje", "njega", "njegov", "njegova", "njegovo", "njej", "njemu", "njen", "njena", "njeno", "nji",
     "njih", "njihov", "njihova", "njihovo", "njiju", "njim", "njo", "njun", "njuna", "njuno", "no", "nocoj",
     "november", "npr.", "o", "ob", "oba", "obe", "oboje", "od", "odprt", "odprta", "odprti", "okoli", "oktober",
     "on", "onadva", "one", "oni", "onidve", "osem", "osma", "osmi", "osmo", "oz.", "p", "pa", "pet", "peta",
     "petek", "peti", "peto", "po", "pod", "pogosto", "poleg", "poln", "polna", "polni", "polno", "ponavadi",
     "ponedeljek", "ponovno", "potem", "povsod", "pozdravljen", "pozdravljeni", "prav", "prava", "prave", "pravi",
     "pravo", "prazen", "prazna", "prazno", "prbl.", "precej", "pred", "prej", "preko", "pri", "pribl.",
     "približno", "primer", "pripravljen", "pripravljena", "pripravljeni", "proti", "prva", "prvi", "prvo", "r",
     "ravno", "redko", "res", "reč", "s", "saj", "sam", "sama", "same", "sami", "samo", "se", "sebe", "sebi",
     "sedaj", "sedem", "sedma", "sedmi", "sedmo", "sem", "september", "seveda", "si", "sicer", "skoraj", "skozi",
     "slab", "smo", "so", "sobota", "spet", "sreda", "srednja", "srednji", "sta", "ste", "stran", "stvar", "sva",
     "t", "ta", "tak", "taka", "take", "taki", "tako", "takoj", "tam", "te", "tebe", "tebi", "tega", "težak",
     "težka", "težki", "težko", "ti", "tista", "tiste", "tisti", "tisto", "tj.", "tja", "to", "toda", "torek",
     "tretja", "tretje", "tretji", "tri", "tu", "tudi", "tukaj", "tvoj", "tvoja", "tvoje", "u", "v", "vaju", "vam",
     "vas", "vaš", "vaša", "vaše", "ve", "vedno", "velik", "velika", "veliki", "veliko", "vendar", "ves", "več",
     "vi", "vidva", "vii", "viii", "visok", "visoka", "visoke", "visoki", "vsa", "vsaj", "vsak", "vsaka", "vsakdo",
     "vsake", "vsaki", "vsakomur", "vse", "vsega", "vsi", "vso", "včasih", "včeraj", "x", "z", "za", "zadaj",
     "zadnji", "zakaj", "zaprta", "zaprti", "zaprto", "zdaj", "zelo", "zunaj", "č", "če", "često", "četrta",
     "četrtek", "četrti", "četrto", "čez", "čigav", "š", "šest", "šesta", "šesti", "šesto", "štiri", "ž", "že",
     "svoj", "jesti", "imeti", "\u0161e", "iti", "kak", "www", "km", "eur", "pač", "del", "kljub", "šele", "prek",
     "preko", "znova", "morda", "kateri", "katero", "katera", "ampak", "lahek", "lahka", "lahko", "morati", "torej"})


def prepare_tokens(input, html=True):
    # manjka lematizacija, če se sploh da v slovenščini
    if html:
        soup = bs4.BeautifulSoup(open(html), "html.parser")
        # soup = bs4.BeautifulSoup(
        #     open("PA3-data/e-prostor.gov.si/e-prostor.gov.si.1.html"), "html.parser")
        for script in soup(["script", "style"]):
            script.decompose()
        soup = soup.find('body')
        text = soup.get_text(separator=' ')
    else:
        text = input
    # tokenizer = RegexpTokenizer('\w+')
    # tokens = tokenizer.tokenize(text)
    tokens = []
    split_text = text.split()
    # ' '.join(split_text[18-3:18+3])

    # split_text
    # VERI GUD PROPRIETERI TOKENIZAR (Y) <---
    for i in range(len(split_text)):
        cur = re.findall('([a-zA-ZšžčćŠŽĆČ]+)', split_text[i])
        if i == 10:
            print(cur)
        if cur != []:
            for item in cur:
                item = item.lower()
                if item not in stop_words_slovene:
                    tokens.append((item, i))
    # tokens = [(i.lower(), i for i in text.split()]
    # tokens=[s.lower() for s in tokens if s not in stop_words_slovene]
    return tokens
