#!/usr/bin/env python3
import logging
from HNIKT import Fnr
from HNIKT import ApiFnr

# Angir logformat og nivå
logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s - %(levelname)s - %(message)s",
  datefmt="%Y-%m-%d %H:%M:%S"  # valgfritt format
)


f = ApiFnr()
for n in range(10):
  fnr = Fnr(f.get())
  print(fnr)