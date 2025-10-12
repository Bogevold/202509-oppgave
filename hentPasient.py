#!/usr/bin/env python3
from HNIKT import ApiFnr
from HNIKT import Fnr
from HNIKT import PasientData


f = ApiFnr()
for n in range(10):
  fnr = Fnr(f.get())
  if fnr.gyldig:
    p = PasientData(fnr)
    # Skriver skillelinje
    print("******************************************")
    print(p)