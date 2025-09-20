# HNIKT-prosjektet

Dette prosjektet demonstrerer et enkelt Python-oppsett for å hente og validere fødselsnummer (FNR) og bygge pasientdataobjekter basert på dem.

Her har jeg valgt en løsning hvor jeg samler funksjonalitet i klasser. 
Dette valget er tatt for å forsøke å samle lik funksjonalitet, og gjøre feilsøking enklere.

Jeg har valgt en iterativ tilnærming, med i utgangspunktet enkle tester som gjør reelle kall på apiet. For å ha muligheten til å teste feil bruk og andre elementer innførte jeg pytest for å kunne bygge testene gradvis bedre etterhvert som nye momenter påtreffes.

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
```

- **Fnr**: Klasse som henter fødselsnummer fra API og validerer dem (siffer, lengde, modulus-11).
- **PasientData**: Klasse som bygger et pasientobjekt basert på ` FNR og tilbyr validering og pen utskrift.
- **hniktTool**: Kommandolinjeskript som benytter klassene over.
- **hentFnr**: Enkelt integrasjons testskript for manuelle tester (10 iterasjoner)
- **hentPasient**: Enkelt integrasjons testskript for manuelle tester (10 iterasjoner)

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

```
pip install -r requirements_dev.txt
pytest -v # Må stå i prosjektkatalogen
```

## Forbedringer som kan vurderes

- Muligheter for å returnere data som json til videre bruk
- Bedre formatering av __str__ i PasientData for bruk i output
- Bruk av feilkoder kun ved "kritiske" feil.
- Utvide håndterbare feil for å generer minimalt med støy