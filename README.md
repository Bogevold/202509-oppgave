# HNIKT-prosjektet

Dette prosjektet demonstrerer et enkelt Python-oppsett for å hente og validere fødselsnummer (FNR) og pasientdataobjekter (json).

Her har jeg valgt en løsning hvor jeg samler funksjonalitet i klasser. 
Dette valget er tatt for å forsøke å samle lik funksjonalitet, og gjøre feilsøking enklere.

Jeg har valgt en iterativ tilnærming, med i utgangspunktet enkle tester som gjør reelle kall på apiet. For å ha muligheten til å teste feil bruk og andre elementer innførte jeg pytest for å kunne bygge testene gradvis bedre etterhvert som nye momenter påtreffes.

Litt morsom oppgave da eg var med på en publikasjon om, aldersverifikasjon på internet i 2008. Der var en av momentene å vise hvor enkelt det er å forfalske personnummer. Publikasjonen ser ut til å være vanskelig å finne, men den er omtalt [her](https://godejord.blogspot.com/2008/)

## Struktur

```bash
HNIKT/
├── __init__.py
├── Fnr.py
├── PasientData.py
tests/
├── __init__.py
├── test_hnikt.py
hniktTool.py
hentFnr.py
hentPasient.py
requirements_dev.txt
requirements.txt
```

- **Fnr**: Klasse som henter fødselsnummer fra API og validerer dem (siffer, lengde, modulus-11).
- **PasientData**: Klasse som bygger et pasientobjekt basert på ` FNR og tilbyr validering og pen utskrift.
- **hniktTool**: Kommandolinjeskript som benytter klassene over.
- **hentFnr**: Enkelt integrasjons testskript for manuelle tester (10 iterasjoner)
- **hentPasient**: Enkelt integrasjons testskript for manuelle tester (10 iterasjoner)
- **test_hnikt**: Testoppsett via pytest for enhetstester.
- **requirements_dev**: Avhengigheter for å kjøre pytest.
- **requirements**: Avhengigheter for vanlig bruk.

## Forutsetninger

Utvikling og testing har foregått på Fedora 41 med python 3.13.
Har forsøkt å bruke minst mulig pakker og biblioteker som ikke følger med i standard python installasjoner, men har lagt med avhengighetsfiler for å lette installasjon om nødvending.

Alt i `requirements.txt` er normalt sett installert men ved feil kan dette installeres med:

```bash
pip install -r requirements_dev.txt
```


## Bruk

Kjør skriptet fra terminalen:

```bash
./hniktTool.py pnr
./hniktTool.py pasient

```

### Flere iterasjoner

Med `-n` eller `--antall` kan du hente ut flere pasienter eller personnummer.

```bash
./hniktTool.py pasient -n 5
``` 

## Logging

Prosjektet bruker pythons standard logging-bibliotek.

- Kritiske feilmeldinger sendes til `stderr`
- Alle logger skrives til .log fil med samme navn som hovedskriptet

## Testing

Tester kjøres med pytest.

```bash
pip install -r requirements_dev.txt
pytest -v # Må stå i prosjektkatalogen
```

Det er også 2 testskript som kjører mot integrasjonspunktene i 10 iterasjoner. 
Tanken her er å kjøre ende-til-ende tester.

```bash

```

## Forbedringer som kan vurderes

- Muligheter for å returnere data som json til videre bruk
- Bedre formatering av __str__ i PasientData for bruk i output
- Bruk av feilkoder kun ved "kritiske" feil.
- Utvide håndterbare feil for å generer minimalt med støy
- Henting/validering av kjønn basert på pnr 
- Henting av fødselsdato fra pnr, århundre basert på nummerseriene i individsifrene
- Flagging av D-nummer (fødselsdag mellom 41 og 71)