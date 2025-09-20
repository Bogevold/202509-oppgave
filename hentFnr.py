#!/usr/bin/env python3
import logging
from HNIKT import Fnr

# Angir logformat og nivå
logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s - %(levelname)s - %(message)s",
  datefmt="%Y-%m-%d %H:%M:%S"  # valgfritt format
)

f = Fnr()
fnr = f.get()
print(f"Validert fnr fra api: {fnr}")