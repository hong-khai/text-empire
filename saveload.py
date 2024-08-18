import json
from typing import Optional
from game import Game

class SaveLoad:
    def __init__(self) -> None:
        self.game: Optional[Game] = None

    def generate_key(self) -> str:
        data = {
            "balance": self.game.balance,
            "taxis": self.game.taxis,
            "buses": self.game.buses,
            "trains": self.game.trains,
            "cf_loans": self.game.cf_loans,
            "cs_loans": self.game.cs_loans,
            "gl_loans": self.game.gl_loans,
            "taxi_stations": self.game.taxi_stations,
            "bus_stations": self.game.bus_stations,
            "train_stations": self.game.train_stations,
            "stations": self.game.stations,
            "redeemable": self.game.redeemable,
            "empire_info": self.game.empire_info,
            "shares": self.game.shares
        }
        return json.dumps(data)

    def load_variables(self, key: str) -> bool:
        try:
            data = json.loads(key)
            self.game.balance = data["balance"]
            self.game.taxis = data["taxis"]
            self.game.buses = data["buses"]
            self.game.trains = data["trains"]
            self.game.cf_loans = data["cf_loans"]
            self.game.cs_loans = data["cs_loans"]
            self.game.gl_loans = data["gl_loans"]
            self.game.taxi_stations = data["taxi_stations"]
            self.game.bus_stations = data["bus_stations"]
            self.game.train_stations = data["train_stations"]
            self.game.stations = data["stations"]
            self.game.redeemable = data["redeemable"]
            self.game.empire_info = data["empire_info"]
            self.game.shares = data["shares"]
            return True
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error loading variables: {e}")
            return False