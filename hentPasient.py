#!/usr/bin/env python3
import logging
from HNIKT import Fnr
from HNIKT import PasientData

# Angir logformat og nivå
logging.basicConfig(
  level=logging.ERROR,
  format="%(asctime)s - %(levelname)s - %(message)s",
  datefmt="%Y-%m-%d %H:%M:%S"  # valgfritt format
)

f = Fnr()
for n in range(10):
  fnr = f.get()
  p = PasientData(fnr)
  # Skriver skillelinje
  print("******************************************")
  print(p)