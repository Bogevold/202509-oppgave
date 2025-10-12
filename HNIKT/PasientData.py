import requests
import logging
import pprint

from .Fnr import Fnr


logger = logging.getLogger(__name__)

class PasientData:
  def __init__(self, fnr: str):
    self.fnr = fnr
    self.fnrObj = Fnr(fnr)
    if not self.fnrObj.validate():
      msg = f"FNR: {fnr} - validerer ikke"
      # Logger ikke da validate allerede logger tilstrekkelig
      raise RuntimeError(msg)
    url = "https://rekruttering.azurewebsites.net/generate/patient"
    headers = {
      "accept": "application/json",
      "Content-Type": "application/json"
    }
    data = {"fnr": fnr}
    svar = requests.post(url=url, headers=headers, json=data, timeout=4)
    if svar.status_code != 200:
      raise RuntimeError(f"Kunne ikke hente data fra {url}, status={svar.status_code}")
    if svar.json()['fnr'] != fnr:
      logger.error("Mottat fnr korresponderer ikke med forespurt returnerer tomt resultat")
      self.pasientRecord = None
    else:
      self.pasientRecord = svar.json()
    
  def get(self) -> str:
    return self.pasientRecord


  def __str__(self):
    # Bruk pprint.pformat for pen JSON-lignende string
    return pprint.pformat(self.pasientRecord, indent=2)
