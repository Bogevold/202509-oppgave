import logging
import json

from datetime import date

logger = logging.getLogger(__name__)

class Type:
  def __init__(self, id=None, tekst=None):
    self.id = id
    self.tekst = tekst
  def to_dict(self):
    return self.__dict__

class DebugInfo:
  def __init__(self, isDigit="True", isLenOk="True", isMod11Ok="True"):
    self.isDigit=isDigit
    self.isLenOk=isLenOk
    self.isMod11Ok=isMod11Ok
  def to_dict(self):
    return self.__dict__


class Fnr:
  def __init__(self, fnr):
    self.fnr = fnr
    self.debugInfo = DebugInfo()
    self.gyldig = self.validate()
    self.fodtDato = None
    self.type = Type()
    if self.gyldig:
      if len(self.fnr) == 9:
        self.type.id = 'O'
        self.type.tekst = 'Organsisasjonsnummer'
      else:
        match int(self.fnr[0:2]):
          case x if x < 1:
            self.type.id = 'O'
            self.type.tekst = 'Organsisasjonsnummer'
          case x if x <= 31: # Her bør en sjekke at det er en gyldig dato også 3102 er ikke gyldig
            self.type.id = 'N'
            self.type.tekst = 'Norsk personnummer'
            self.setFodtDato()
          case x if x <= 71: # Sjekk også at x -40 + mnd er en gyldig dag
            self.type.id = 'D'
            self.type.tekst = 'D-Nummer'
            self.setFodtDato()
          case _:
            self.type.id = 'X'
            self.type.tekst = 'Ugyldig eller syntetisk personummer'
    else:
      self.type.id = 'X'
      self.type.tekst = 'Ugyldig eller syntetisk personummer'

    if self.type.id in ['N', 'D']:
      self.kjonn = 'M' if bool(int(self.fnr[8])%2) else 'F'
    else:
      self.kjonn = 'N/A'

  def to_dict(self):
    return {
      "fnr": self.fnr,
      "gyldig": self.gyldig,
      "fødtselsdato": self.fodtDato.isoformat() if self.fodtDato else "N/A",
      "kjønn": self.kjonn,
      "type": self.type.to_dict(),
      "debugInfo": self.debugInfo.to_dict()
    }

#  def getType(self):
#    return self.type

  def getFnr(self) -> str:
    return self.fnr
  
  def modulus11Ok(self) -> bool:
    value = self.fnr
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

  def validate(self) -> bool:
    value = self.fnr
    # Bruker feil telling for å få alle feil i loggen med en gang
    # Logger kun til info da disse er forventede feil som håndteres
    feil = 0
    if not value.isdigit():
      self.debugInfo.isDigit = f"{value} - Feilet validering - Fødselsnummer må kun bestå av siffer (0-9)."
      logger.info(self.debugInfo.isDigit)
      feil +=1
    if len(value) not in [9,11]:
      self.debugInfo.isLenOk = f"{value} - Feilet validering - Fødselsnummer må være nøyaktig 11 siffer langt, orgnr må være 9."
      logger.info(self.debugInfo.isLenOk)
      feil +=1  
    if (len(value) == 9 or (len(value) == 11 and value.startswith("00"))):
      if not self.modulus11_orgnr_ok():
        self.debugInfo.isMod11Ok = f"{value} - Feilet validering - Orgnummer passerer ikke modulus11."
        feil += 1
    else:
      if not self.modulus11Ok():
        self.debugInfo.isMod11Ok = f"{value} - Feilet validering - Fødselsnummer passerer ikke modulus11."
        feil += 1
    return feil == 0

  def __str__(self):
    #return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    return json.dumps(self.to_dict(), ensure_ascii=False)

  def setFodtDato(self):
    day = int(self.fnr[0:2])
    if self.type.id == 'D':
      day = day - 40 # tar høyde for dnr
    month = int(self.fnr[2:4])
    year_suffix = int(self.fnr[4:6])
    indiv = int(self.fnr[6:9])
    # Bestem århundre
    if 0 <= indiv <= 499:
      century = 1900
    elif 500 <= indiv <= 749 and year_suffix >= 54:
      century = 1800
    elif 500 <= indiv <= 999 and year_suffix <= 39:
      century = 2000
    elif 900 <= indiv <= 999 and year_suffix >= 40:
      century = 1900
    else:
      raise ValueError("Ugyldig individnummer for fødselsdato")
    year = century + year_suffix
    self.fodtDato = date(year, month, day)

  def modulus11_orgnr_ok(self) -> bool:
    value = self.fnr
    # Orgnummer kan være 9 siffer, eller 11 siffer som starter med "00"
    if not value.isdigit():
      return False
    if len(value) == 11 and value.startswith("00"):
      value = value[2:]  # Fjern prefiks "00"
    if len(value) != 9:
      return False

    weights = [3, 2, 7, 6, 5, 4, 3, 2]
    total = sum(int(value[i]) * weights[i] for i in range(8))
    k = 11 - (total % 11)
    if k == 11:
      k = 0
    if k == 10:
      return False
    return k == int(value[8])
