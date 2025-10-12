import pytest

from datetime import date
from unittest.mock import patch
from HNIKT.ApiFnr import ApiFnr
from HNIKT.Fnr import Fnr, Type, DebugInfo
from HNIKT.PasientData import PasientData

# PNR hentet fra api'et for testformål
test_pnr = "08063943003"
test_ok_orgnr = "00924616733"



# --- Tester ApiFnr ---
@patch("HNIKT.ApiFnr.requests.get")
def test_apifnr_get(mock_get):
  mock_get.return_value.status_code = 200
  mock_get.return_value.text = test_pnr
  apifnr = ApiFnr()
  verdi = apifnr.get()
  assert isinstance(verdi, str)
  assert len(verdi) == 11
  assert verdi.isdigit()

def test_fnr_validate_ok():
  fnr = Fnr(test_pnr)
  assert fnr.validate() is True

def test_fnr_validate_feil():
  fnr = Fnr("abc")
  assert fnr.validate() is False
  fnr = Fnr("123")
  assert fnr.validate() is False


# --- Tester Fnr ---
#  1 -------------------------------------------------------------------------
def test_valid_fnr_norsk_personnummer():
  # Gyldig norsk fødselsnummer: 01020312376 (kontrollert med modulus)
  fnr = Fnr(test_pnr)
  assert fnr.gyldig is True
  assert fnr.type.id == "N"
  assert fnr.type.tekst == "Norsk personnummer"
  assert fnr.kjonn == "F"  # 9. siffer = 0 -> oddetall = mann
  assert fnr.fodtDato == date(1939, 6, 8)
  assert fnr.to_dict()["gyldig"] is True

#  2 -------------------------------------------------------------------------
def test_valid_fnr_dnummer():
  # D-nummer: dag + 40 (eks: 410203 -> født 01.02.2003)
  fnr = Fnr("41010000023")
  assert fnr.gyldig is True
  assert fnr.type.id == "D"
  assert fnr.fodtDato == date(1900, 1, 1)

#  3 -------------------------------------------------------------------------
def test_invalid_fnr_too_short():
  fnr = Fnr("12345")
  assert fnr.gyldig is False
  assert "11 siffer langt" in fnr.debugInfo.isLenOk
  assert fnr.type.id == "X"
  assert fnr.kjonn == "N/A"

#  4 -------------------------------------------------------------------------
def test_invalid_fnr_not_digits():
  fnr = Fnr("abcdefghijk")
  assert fnr.gyldig is False
  assert "kun bestå av siffer" in fnr.debugInfo.isDigit

#  5 -------------------------------------------------------------------------
def test_invalid_fnr_modulus_feil():
  fnr = Fnr("01020312345")
  assert fnr.gyldig is False
  assert "modulus" in fnr.debugInfo.isMod11Ok

#  6 -------------------------------------------------------------------------
def test_type_orgnummer():
  # Første to siffer < 1 (00) gir 'O' ifølge koden
  fnr = Fnr(test_ok_orgnr)
  assert fnr.type.id == "O"
  assert fnr.type.tekst == "Organsisasjonsnummer"

#  7 -------------------------------------------------------------------------
def test_type_ugyldig():
  # Starter med 90 -> fanges i siste case
  fnr = Fnr("90000000000")
  assert fnr.type.id == "X"
  assert fnr.type.tekst.startswith("Ugyldig")

#  8 -------------------------------------------------------------------------
def test_to_dict_inneholder_forventede_nokler():
  fnr = Fnr("01020312376")
  d = fnr.to_dict()
  for key in ["fnr", "gyldig", "fødtselsdato", "kjønn", "type", "debugInfo"]:
    assert key in d
  assert isinstance(d["type"], dict)
  assert isinstance(d["debugInfo"], dict)

#  9 -------------------------------------------------------------------------
def test_str_returnerer_json():
  fnr = Fnr("01020312376")
  s = str(fnr)
  assert s.startswith("{")
  assert '"fnr": "01020312376"' in s


# --- Tester PasientData ---
@patch("HNIKT.PasientData.requests.post")
def test_pasientdata_get(mock_post):
  mock_post.return_value.status_code = 200
  mock_post.return_value.json.return_value = {"fnr": test_pnr, "navn": "Test Testesen"}
  p = PasientData(test_pnr)
  data = p.get()
  assert "fnr" in data
  assert data["fnr"] == test_pnr

@patch("HNIKT.PasientData.requests.post")
def test_pasientdata_validate_feil(mock_post):
  mock_post.return_value.status_code = 200
  mock_post.return_value.json.return_value = {"fnr": test_pnr, "navn": "Test Testesen"}
  with pytest.raises(RuntimeError):
    p = PasientData("ugyldig")