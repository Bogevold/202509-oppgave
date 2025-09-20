class PasientData:
  def __init__(self, fnr: str):
    self.fnr = fnr

  def get(self) -> str:
    return self.fnr

  def print(self) -> None:
    print(f"HelseData for fnr: {self.fnr.get()}")
