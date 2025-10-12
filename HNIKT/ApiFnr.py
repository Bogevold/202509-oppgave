import requests
import logging

logger = logging.getLogger(__name__)

class ApiFnr:
  def __init__(self):
    self.url = "https://rekruttering.azurewebsites.net/generate/fnr"
  
  def get(self) -> str:
    svar = requests.get(url=self.url, timeout=4)
    if svar.status_code != 200:
      raise RuntimeError(f"Kunne ikke hente fødselsnummer fra {self.url}, status={svar.status_code}")
    return svar.text.strip()
