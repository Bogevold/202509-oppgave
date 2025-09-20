import requests
import logging

logger = logging.getLogger(__name__)

class Fnr:
  def get(self) -> str:
    url = "https://rekruttering.azurewebsites.net/generate/fnr"
    # Flagg for å sikre å få gyldige nummer
    ok_fnr = False
    # Repeterer til validering blir korrekt
    while not ok_fnr:
      svar = requests.get(url=url, timeout=4)
      if svar.status_code != 200:
        raise RuntimeError(f"Kunne ikke hente fødselsnummer fra {url}, status={svar.status_code}")
      fnr = svar.text.strip()
      ok_fnr = self.validate(fnr)
    return fnr
  
  def modulus11Ok(self, value: str):
    # Sjekker lendge og siffer da modulus kan kjøres uavhengig av get
    if not (value.isdigit() and len(value) == 11):
      return False
    # Tildeler hvert tegn til sine formel elementer
    d1 = int(value[0])
    d2 = int(value[1])
    m1 = int(value[2])
    m2 = int(value[3])
    å1 = int(value[4])
    å2 = int(value[5])
    i1 = int(value[6])
    i2 = int(value[7])
    i3 = int(value[8])
    # K1 formel: k1 = 11 - ((3 × d1 + 7 × d2 + 6 × m1 + 1 × m2 + 8 × å1 + 9 × å2 + 4 × i1 + 5 × i2 + 2 × i3) mod 11)
    k1 = 11 - ((3 * d1 + 7 * d2 + 6 * m1 + 1 * m2 + 8 * å1 + 9 * å2 + 4 * i1 + 5 * i2 + 2 * i3) % 11)
    # Setter k1 til 0 dersom en treffer spesialtilfellet 11
    k1 = k1 if k1 != 11 else 0
    # K2 formel: k2 = 11 - ((5 × d1 + 4 × d2 + 3 × m1 + 2 × m2 + 7 × å1 + 6 × å2 + 5 × i1 + 4 × i2 + 3 × i3 + 2 × k1) mod 11).
    k2 = 11 - ((5 * d1 + 4 * d2 + 3 * m1 + 2 * m2 + 7 * å1 + 6 * å2 + 5 * i1 + 4 * i2 + 3 * i3 + 2 * k1) % 11)
    # Trenger ikke å kontrollere om kontrollsifrene bli 10 og 11 da de uansett ikke vil påvirke kontrollen
    return k1 == int(value[9]) and k2 == int(value[10])

  def validate(self, value: str) -> bool:
    # Bruker feil telling for å få alle feil i loggen med en gang
    # Logger kun til info da disse er forventede feil som håndteres
    feil = 0
    if not value.isdigit():
      logger.info(f"{value} - Feilet validering - Fødselsnummer må kun bestå av siffer (0-9).")
      feil +=1
    if len(value) != 11:
      logger.info(f"{value} - Feilet validering - Fødselsnummer må være nøyaktig 11 siffer langt.")
      feil +=1  
    if not self.modulus11Ok(value):
      logger.info(f"{value} - Feilet validering - Fødselsnummer passerer ikke modulus kontroll.")
      feil +=1
    return feil == 0
