import pytest
from unittest.mock import patch
from HNIKT.Fnr import Fnr
from HNIKT.PasientData import PasientData

# PNR hentet fra api'et for testformål
test_pnr = "08063943003"

# --- Tester Fnr ---
@patch("HNIKT.Fnr.requests.get")
def test_fnr_get(mock_get):
  mock_get.return_value.status_code = 200
  mock_get.return_value.text = test_pnr
  fnr = Fnr()
  verdi = fnr.get()
  assert isinstance(verdi, str)
  assert len(verdi) == 11
  assert verdi.isdigit()

def test_fnr_validate_ok():
  fnr = Fnr()
  assert fnr.validate(test_pnr) is True

def test_fnr_validate_feil():
  fnr = Fnr()
  assert fnr.validate("abc") is False
  assert fnr.validate("123") is False

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