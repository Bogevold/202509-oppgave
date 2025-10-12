#!/usr/bin/env python3
import argparse
import logging
import os
import sys

from HNIKT import ApiFnr
from HNIKT import Fnr
from HNIKT import PasientData

# Lognavn
script_name = os.path.basename(sys.argv[0])  
if script_name.endswith(".py"):
  log_filename = script_name[:-3] + ".log"
else:
  log_filename = "default.log"

# Logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # logger alt

# --- File handler for alle nivåer ---
file_handler = logging.FileHandler(log_filename)
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter(
  "%(asctime)s - %(levelname)s - %(message)s",
  datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# --- Stream handler til stderr for WARNING og høyere ---
stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setLevel(logging.ERROR)
stderr_formatter = logging.Formatter(
  "%(asctime)s - %(levelname)s - %(message)s",
  datefmt="%Y-%m-%d %H:%M:%S"
)
stderr_handler.setFormatter(stderr_formatter)
logger.addHandler(stderr_handler)

def main():
  parser = argparse.ArgumentParser(description="Hent pasientdata eller PNR")
  parser.add_argument("modus", choices=["pasient", "pnr"], help="Velg modus: pasient eller pnr")
  parser.add_argument("-n", "--antall", type=int, default=1, help="Antall iterasjoner")
  args = parser.parse_args()
  fnr_api = ApiFnr();
  
  # Henter nye fnr inntil et gyldig returneres
  while True:
    fnr_obj = Fnr(fnr_api.get())
    # Sjekker gyldighet og at typen kan være en pasient (Norske fødselsnumre og D-nummer)
    if fnr_obj.gyldig and fnr_obj.type.id in ['N', 'D']:
      break

  for i in range(args.antall):
    fnr = fnr_obj.get()
    print(f"\nIterasjon {i+1}:")
    print(f"PNR: {fnr}") # PNR printes uansett og alene dersom modus er pnr
    if args.modus == "pasient":
      p = PasientData(fnr)
      print(p)
      
if __name__ == "__main__":
  main()