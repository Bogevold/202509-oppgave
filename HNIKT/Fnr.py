import requests

class Fnr:
  #def __init__(self):
  #  self.value = value

  def get(self) -> str:
    url = "https://rekruttering.azurewebsites.net/generate/fnr"
    svar = requests.get(url=url, timeout=4)
    if svar.status_code != 200:
      raise RuntimeError(f"Kunne ikke hente fødselsnummer fra {url}, status={svar.status_code}")
    fnr = svar.text.strip()
    return fnr
  
  def modulus11Ok(self, value: str):
    # Placeholder: ekte modulus-11 sjekk implementeres her
    return True

  def validate(self, value: str) -> bool:
    if not value.isdigit():
      raise ValueError("Fødselsnummer må kun bestå av siffer (0-9).")
    if len(value) != 11:
      raise ValueError("Fødselsnummer må være nøyaktig 11 siffer langt.")
    if not self.modulus11Ok(value):
      raise ValueError("Fødselsnummer passerer ikke modulus kontroll.")
