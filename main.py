import threading
import time
import random
import json
from typing import Dict, List, Union, Optional

class Tools:
    def __init__(self) -> None:
        self.first_names: List[str] = [
            "Emma", "Olivia", "Ava", "Isabella", "Sophia",
            "Liam", "Noah", "William", "James", "Logan"
        ]
        self.last_names: List[str] = [
            "Smith", "Johnson", "Williams", "Brown", "Jones",
            "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"
        ]
        self.place_adjectives: List[str] = [
            'Mystic', 'Forgotten', 'Enchanted', 'Lost', 'Ancient',
            'Whispering', 'Ethereal', 'Silent', 'Celestial', 'Hidden',
            'Glowing', 'Secret', 'Twilight', 'Emerald', 'Frozen',
            'Divine', 'Moonlit', 'Golden', 'Sapphire', 'Starlit'
        ]
        self.place_nouns: List[str] = [
            'Valley', 'Forest', 'Island', 'Mountains', 'Canyon',
            'Labyrinth', 'Cave', 'Grove', 'Lake', 'Ruins',
            'Waterfall', 'Citadel', 'Garden', 'Desert', 'Oasis',
            'Temple', 'Castle', 'Peak', 'Spires', 'Meadow'
        ]
        self.empire_prefixes: List[str] = [
            "Galactic", "Celestial", "Stellar", "Cosmic",
            "Universal", "Interstellar"
        ]
        self.empire_suffixes: List[str] = [
            "Empire", "Dominion", "Federation", "Union",
            "Consortium", "Alliance"
        ]

    def generate_name(self) -> str:
        return f"{random.choice(self.first_names)} {random.choice(self.last_names)}"

    def generate_place(self) -> str:
        return f"{random.choice(self.place_adjectives)} {random.choice(self.place_nouns)}"

    def generate_empire(self) -> str:
        return f"{random.choice(self.empire_prefixes)} {random.choice(self.empire_suffixes)}"


class SaveLoad:
    def __init__(self) -> None:
        self.game: Optional['Game'] = None

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


class Game:
    def __init__(self) -> None:
        self.balance: int = 250
        self.taxis: int = 0
        self.buses: int = 0
        self.trains: int = 0
        self.cf_loans: int = 0
        self.cs_loans: int = 0
        self.gl_loans: int = 0
        self.special_loan_amount: int = 0
        self.taxi_stations: int = 0
        self.bus_stations: int = 0
        self.train_stations: int = 0
        self.add_dividend_interval: int = 0
        self.tools: Tools = Tools()
        self.saveload: SaveLoad = SaveLoad()
        self.saveload.game = self
        self.separator: str = '-' * 30
        self.stations: List[str] = []
        self.redeemable: List[bool] = [True] * 5

        self.empire_info: Dict[str, str] = {
            "name": self.tools.generate_empire(),
            "monarch": self.tools.generate_name()
        }
        self.loan_types: Dict[str, Dict[str, Union[int, str]]] = {
            "a": {
                "amount": 500,
                "flag": "cf_loans",
                "message": "Community Fund"
            },
            "b": {
                "amount": 1000,
                "flag": "cs_loans",
                "message": "City Support"
            },
            "c": {
                "amount": 2500,
                "flag": "gl_loans",
                "message": "Grand Loan"
            }
        }

        self.vehicle_costs: Dict[str, Dict[str, Union[int, str]]] = {
            "a": {
                "cost": 100,
                "station": "bus_stations",
                "type": "Bus"
            },
            "b": {
                "cost": 40,
                "station": "taxi_stations",
                "type": "Taxi"
            },
            "c": {
                "cost": 200,
                "station": "train_stations",
                "type": "Train"
            }
        }

        self.station_costs: Dict[str, Dict[str, Union[int, str]]] = {
            "a": {
                "cost": 10,
                "type": "Taxi"
            },
            "b": {
                "cost": 25,
                "type": "Bus"
            },
            "c": {
                "cost": 50,
                "type": "Train"
            }
        }

        self.shares: Dict[str, Dict[str, int]] = {
            "a": {
                "name": "Horizon Industries",
                "price": 0,
                "value": 0,
                "dividend_yield": 0,
                "amount": 0
            },
            "b": {
                "name": "Summit Securities",
                "price": 0,
                "value": 0,
                "dividend_yield": 0,
                "amount": 0
            },
            "c": {
                "name": "Crestline Holdings",
                "price": 0,
                "value": 0,
                "dividend_yield": 0,
                "amount": 0
            },
            "d": {
                "name": "Cascade Ventures",
                "price": 0,
                "value": 0,
                "dividend_yield": 0,
                "amount": 0
            },
            "e": {
                "name": "Panorama Industries",
                "price": 0,
                "value": 0,
                "dividend_yield": 0,
                "amount": 0
            },
            "f": {
                "name": "Vanguard Corporation",
                "price": 0,
                "value": 0,
                "dividend_yield": 0,
                "amount": 0
            },
            "g": {
                "name": "Apex Dynamics",
                "price": 0,
                "value": 0,
                "dividend_yield": 0,
                "amount": 0
            },
            "h": {   
                "name": "Zenith Ventures",
                "price": 0,
                "value": 0,
                "dividend_yield": 0,
                "amount": 0
            },
            "i": {   
                "name": "Crestview Holdings",
                "price": 0,
                "value": 0,
                "dividend_yield": 0,
                "amount": 0
            },
            "j": {   
                "name": "Brick Corporation",
                "price": 0,
                "value": 0,
                "dividend_yield": 0,
                "amount": 0
            }
        }

    def make_payment(self, price: int, number_needed: int, vehicle_type: str) -> None:
        if self.balance >= price:
            self.balance -= price
            setattr(self, vehicle_type + 's', getattr(self, vehicle_type + 's') + number_needed)
        else:
            print("You do not have enough money!")

    def show_empire_info(self) -> None:
        print(f"""Empire Name: {self.empire_info["name"]}
Empire Monarch: {self.empire_info["monarch"]}
Empire Treasury: {self.balance}
Taxis: {self.taxis}
Buses: {self.buses}
Trains: {self.trains}
Taxi Stations: {self.taxi_stations}
Bus Stations: {self.bus_stations}
Train Stations: {self.train_stations}""")

    def edit_empire(self) -> None:
        new_empire_name: str = input("Enter your new empire name (leave blank to skip): ")
        new_empire_monarch: str = input("Enter your new monarch name (leave blank to skip): ")
        if new_empire_name:
            self.empire_info["name"] = new_empire_name
        if new_empire_monarch:
            self.empire_info["monarch"] = new_empire_monarch

    def buy_vehicle(self, vehicle_type: str, number_needed: int) -> None:
        if number_needed < 1:
            print("Negative numbers and zero are not allowed.")
            return

        vehicle_type = vehicle_type.strip().lower()

        vehicle_mapping = {
            "bus": "a",
            "taxi": "b",
            "train": "c"
        }

        key = vehicle_mapping.get(vehicle_type)

        if not key:
            print("Invalid vehicle type! Please choose from 'bus', 'taxi', or 'train'.")
            return

        cost_info = self.vehicle_costs.get(key)
        if not cost_info:
            print("Error retrieving vehicle cost information.")
            return

        station_name = cost_info["station"]
        if getattr(self, station_name) <= 0:
            print(f"No {cost_info['type']} station available.")
            return

        price = cost_info["cost"] * number_needed
        if self.balance < price:
            print("You do not have enough money!")
            return

        vehicle_attr = vehicle_type + "s"
        if not hasattr(self, vehicle_attr):
            vehicle_attr = vehicle_type + "es"

        current_count = getattr(self, vehicle_attr)
        setattr(self, vehicle_attr, current_count + number_needed)
        self.balance -= price

        print(f"Successfully bought {number_needed} {vehicle_type}(s).")

    def handle_loan(self, loan_type: str, action: int) -> None:
        if loan_type == "d":
            self.handle_special_loan(action)
        elif loan_type in self.loan_types:
            self.handle_standard_loan(loan_type, action)
        else:
            print("Invalid loan type!")
    
    def handle_special_loan(self, action: int) -> None:
        if action != 0:
            if self.balance >= self.special_loan_amount:
                self.special_loan_amount = 0
            else:
                print("Not enough money!")
        elif self.special_loan_amount == 0:
            print("The bank has been making low profits these weeks. They are interested in your offer.")
            try:
                self.special_loan_amount = int(input("Name a price: "))
                if self.special_loan_amount < 1:
                    print("Negative numbers and zero are not allowed.")
                    return
                if self.balance < self.special_loan_amount / 100:
                    print("")
            except ValueError:
                print("Invalid number.")
                return
            
            if random.randint(0, 1) == 1:
                print(f"The bank is interested in your offer. It has been accepted. You have received a loan of ${self.special_loan_amount}.")
            else:
                print("The bank is not available. Your offer has been declined.")
        else:
            print("You already have a customized loan with the bank. You can request a new one once you pay the customized loan back.")

    def handle_standard_loan(self, loan_type: str, action: int) -> None:
        loan_info = self.loan_types[loan_type]
        if getattr(self, loan_info["flag"]) == action:
            amount = loan_info["amount"]
            if action == 0:
                self.balance += amount
                print("Loan received successfully.")
            else:
                if self.balance >= amount:
                    self.balance -= amount
                    print("Loan paid off successfully.")
                else:
                    print("Not enough money!")
            setattr(self, loan_info["flag"], action ^ 1)
        else:
            print("Loan already processed.")
    
    def purchase_shares(self, alphic_shares_choice: str) -> None:
        share: str = self.shares[alphic_shares_choice]["name"]
        price_per_share: int = self.shares[alphic_shares_choice]["price"]

        print(f"""The price of one share in {share} is ${price_per_share}
Enter the amount of shares you want to buy. To calculate the price, type in "calculator".""")
        
        shares_choice: str = input().strip().lower()
        if shares_choice == "calculator":
            try:
                shares_to_calculate = int(input("Enter the amount of shares you want to calculate the price of: "))
            except ValueError:
                print("Invalid number.")
                return

            if shares_to_calculate < 1:
                print("Negative numbers and zero are not allowed.")
                return

            cost_of_shares: int = shares_to_calculate * price_per_share
            print(f"The price of {shares_to_calculate} shares in {share} is ${cost_of_shares}.")

        else:
            try:
                cost_of_shares: int = int(shares_choice) * price_per_share
            except ValueError:
                print("Invalid number.")
                return
            
            if self.balance < cost_of_shares:
                print("Not enough money!")
                return
            
            self.balance -= cost_of_shares
            self.shares[alphic_shares_choice]["amount"] += int(shares_choice)

            print(f"Sucessfully bought {shares_choice} shares in {share}.")
    
    def sell_shares(self, alphic_shares_choice: str) -> None:
        share: str = self.shares[alphic_shares_choice]["name"]
        if self.shares[alphic_shares_choice]["amount"] == "0":
            print(f"You do not own any shares in {share}.")
            return
        shares_to_sell = input("Enter the amount of shares you want to sell: ")
        self.balance += self.shares[alphic_shares_choice]["value"] * shares_to_sell
    
    def view_share_market(self) -> None:
        print(f"""{self.separator}
Share Market
{self.separator}""")
        for share in self.shares:
            share_name: str = self.shares[share]["name"]
            print(f"""Price of one share in {share_name}: ${self.shares[share]["price"]}
Value of one share in {share_name}: ${self.shares[share]["value"]}
Dividend yield of {share_name}: {self.shares[share]["dividend_yield"] * 100}%
{self.separator}""")
    
    def print_share_choices(self) -> None:
        for share in self.shares:
            print(f"{share}) {self.shares[share]["name"]}")
        
    def create_station(self, station_type: str) -> None:
        if station_type in self.station_costs:
            cost_info = self.station_costs[station_type]
            if self.balance > cost_info["cost"] - 1:
                self.balance -= cost_info["cost"]
                self.check_station_exists()
                self.stations.append(self.station_name + f" {cost_info['type']} Station")
                print(f"{cost_info['type']} station created successfully!")
                setattr(self, cost_info["type"].lower() + "_stations", getattr(self, cost_info["type"].lower() + "_stations") + 1)
            else:
                print("Not enough money!")
        else:
            print("Invalid station type!")

    def check_station_exists(self) -> None:
        station_name: str = self.tools.generate_place()
        extra_station_name: int = 1
        while station_name in self.stations:
            station_name = f"{station_name} {extra_station_name}"
            extra_station_name += 1
        self.station_name = station_name

    def print_all_stations(self) -> None:
        print("Stations:")
        for station in self.stations:
            print(station)

    def rename_station(self) -> None:
        self.print_all_stations()
        old_name: str = input("Enter the name of the station you want to rename: ")
        if old_name in self.stations:
            new_name: str = input("Enter the new name for the station: ")
            if new_name:
                index: int = self.stations.index(old_name)
                self.stations[index] = new_name
                print(f"Station renamed from '{old_name}' to '{new_name}'.")
            else:
                print("New name cannot be empty.")
        else:
            print("Station not found.")

    def load_game_from_file(self) -> None:
        if len(self.game_info) < 2:
            print("Error finding saved game.")
        else:
            if self.saveload.load_variables(self.game_info[1]):
                print("Game loaded successfully.")
                self.start_game_loop()
    
    def get_game_info(self) -> None:
        with open("game_info.txt", "r") as file:
            self.game_info = file.readlines()
            
    def start_game(self) -> None:
        print("""Welcome to TextEmpire - A text-adventure transport tycoon game.
Main Menu:
a) Tutorial
b) Create Game
c) Load Game
d) Exit""")

        while True:
            choice: str = input("Enter your choice: ").strip().lower()

            if choice == "a":
                self.display_tutorial()
            elif choice == "b":
                print("New game created.")
                with open("game_info.txt", 'a+') as file:
                    file.seek(0)
                    self.game_info = file.read()
                    if not self.game_info:
                        file.write("\n")
                self.start_game_loop()
            elif choice == "c":
                print("""How do you want to load your game?
a) Game key
b) Saved key in file""")
                load_choice = input().strip().lower()
                if load_choice == "a":
                    key: str = input("Enter your game key: ").strip()
                    if self.saveload.load_variables(key):
                        print("Game loaded successfully.")
                        self.start_game_loop()
                    else:
                        print("Failed to load game. Please check your key and try again.")
                elif load_choice == "b":
                    try:
                        self.load_game_from_file()
                    except AttributeError:
                        self.get_game_info()
                        self.load_game_from_file()
            elif choice == "d":
                print("Exiting game...")
                break
            else:
                print("Invalid option!")

    def display_tutorial(self) -> None:
        print(f"""{self.separator}
[OVERVIEW]
Buy vehicles to earn money.
Taxis cost $40 each. Buses cost $100 each. Trains cost $200 each.
To purchase vehicles, create stations.
Taxi stations cost $10 each. Bus stations cost $25 each. Train stations cost $50 each.
The more stations you have, the more money you make!
Get loans if needed.
[COMMANDS]
/empireinfo - View empire info
/editempire - Edit empire name and monarch
/savegame - Save your game
/buyvehicle - Purchase vehicles
/getloan - Get a loan
/payloan - Pay a loan
/buyshares - Purchase shares
/sellshares - Sell your shares
/sharemarket - View the share market
/createstation - Create a new station
/stations - View all stations
/renamestation - Rename a station
/achievements - View achievements and rewards
/exit - Exit game or main menu
[WARNINGS]
Do not modify game_info.txt as it may corrupt game data.
{self.separator}""")
        
    def start_game_loop(self) -> None:
        threading.Thread(target=self.update_game, daemon=True).start()

        while True:
            command: str = input("Command: ").strip().lower()

            if command == "/empireinfo":
                self.show_empire_info()
            elif command == "/editempire":
                self.edit_empire()
            elif command == "/savegame":
                try:
                    with open("game_info.txt", "r") as file:
                        self.game_info = file.readlines()
                        if len(self.game_info) < 2:
                            any_saved_game: bool = False
                except FileNotFoundError:
                    any_saved_game: bool = False

                print("""How do you want to save your game?
a) Get game key
b) Save game in file""")
                save_choice: str = input().strip().lower()

                if save_choice == "a":
                    print(f"Game Key: {self.saveload.generate_key()}. Save it securely.")
                elif save_choice == "b":
                    if any_saved_game == True:
                        print("""You already have a saved game. Do you want to overwrite it?
a) Yes
b) No""")
                        overwrite_saved = input("You already have a saved game. Do you want to overwrite it?").strip().lower()
                        if overwrite_saved == "a":
                            self.write_game_key()
                        elif overwrite_saved == "b":
                            print(f"Game Key: {self.saveload.generate_key()}. Save it securely.")
                        else:
                            print("Not a valid option.")
                    else:
                        self.write_game_key()
                else:
                    print("Not a valid option.")
            elif command == "/buyvehicle":
                print("""Pick a vehicle to buy. (bus, taxi or train)""")
                vehicle_type: str = input().strip().lower()
                try:
                    number_needed = int(input("How many? "))
                    self.buy_vehicle(vehicle_type, number_needed)
                except ValueError:
                    print("Invalid number.")
            elif command == "/getloan":
                print("""Which loan do you want?
a) Community Fund - $500
b) City Support - $1000
c) Grand Loan - $2500
d) Request a customized loan from the bank""")
                loan_needed: str = input().strip().lower()
                self.handle_loan(loan_needed, 0)
            elif command == "/payloan":
                print("""Which loan to pay?
a) Community Fund - $500
b) City Support - $1000
c) Grand Loan - $2500""")
                loan_paying: str = input().strip().lower()
                self.handle_loan(loan_paying, 1)
            elif command == "/buyshares":
                print("Which share do you want to invest in?")
                self.print_share_choices()
                new_share: str = input().strip().lower()
                self.purchase_shares(new_share)
            elif command == "/sellshares":
                print("Which share do you want to sell?")
                self.print_share_choices()
                share_to_sell: str = input().strip().lower()
                self.sell_shares(share_to_sell)
            elif command == "/sharemarket":
                self.view_share_market()
            elif command == "/createstation":
                print("""What type of station?
a) Taxi
b) Bus
c) Train""")
                new_station: str = input().strip().lower()
                self.create_station(new_station)
            elif command == "/stations":
                self.print_all_stations()
            elif command == "/renamestation":
                self.rename_station()
            elif command == "/exit":
                print("""Exit to:
a) Main Menu
b) Exit game""")
                exit_action: str = input().strip().lower()
                if not exit_action == "":
                    print("You are about to exit your game. Please make sure to save your game.")
                    save = input("If you hadn't already saved your game, please type \"save\". : ").strip().lower()
                    if save == "save":
                        print(f"Game Key: {self.saveload.generate_key()}. Save it securely.")
                if exit_action == "a":
                    print("Returning to main menu...")
                    self.__init__()
                    self.start_game()
                elif exit_action == "b":
                    print("Exiting game...")
                    break
                else:
                    print("Invalid option.")
            elif command == "/achievements":
                self.check_achievements()
            elif command == "/redeem":
                self.redeem_passkey()
            elif not command:
                continue
            else:
                print("Unknown command.")

    def check_achievements(self) -> None:
        if self.balance > self.high_score and self.redeemable[1]:
            with open("game_info.txt", "w") as file:
                file.write(str(self.balance))
            print("Achievement: Beaten high score! Passkey: t5m7pk8")
        elif self.balance % 2500 == 0 and self.redeemable[2]:
            print("Achievement: $2500 earned! Passkey: ut6gp9s")
        elif self.gl_loans == 1 and self.redeemable[3]:
            print("Achievement: First grand loan! Passkey: po31u5b")
        elif self.buses + self.trains + self.taxis == 20 and self.redeemable[4]:
            print("Achievement: 20 vehicles! Passkey: 5rop05b")
        else:
            print("No achievements found.")

    def redeem_passkey(self) -> None:
        passkey = input("Enter passkey: ").strip()
        rewards = {
            "t5m7pk8": ("2 trains", lambda: setattr(self, 'trains', self.trains + 2)),
            "ut6gp9s": ("$500", lambda: setattr(self, 'balance', self.balance + 500)),
            "po31u5b": ("$250", lambda: setattr(self, 'balance', self.balance + 250)),
            "5rop05b": ("10 buses", lambda: setattr(self, 'buses', self.buses + 10))
        }
        reward = rewards.get(passkey)
        if reward:
            print(f"Redeemed prize of {reward[0]}.")
            reward[1]()
            self.redeemable[list(rewards.keys()).index(passkey) + 1] = False
        else:
            print("Invalid passkey.")

    def write_game_key(self) -> None:
        try:
            with open("game_info.txt", "r") as file:
                pass
        except FileNotFoundError:
            self.game_info = [''] * 2

        if len(self.game_info) < 2:
            self.game_info.extend([''] * (2 - len(self.game_info)))

        self.game_info[1] = self.saveload.generate_key() + '\n'

        with open("game_info.txt", 'w') as file:
            file.writelines(self.game_info)
    
    def update_balance(self) -> None:
        balance_delta: int = (int(self.buses) * 10 * int(self.bus_stations) +
                                int(self.taxis) * 5 * int(self.taxi_stations) +
                                int(self.trains) * 25 * int(self.train_stations))
        balance_delta -= (int(self.cf_loans) * int(20) + 
                            int(self.cs_loans) * int(35) + 
                            int(self.gl_loans) * int(50))
        
        if self.special_loan_amount != 0:
            balance_delta -= self.special_loan_amount * 100

        self.add_dividend_interval += 1
        if self.add_dividend_interval == 100:
            for share in self.shares:
                total_investment_value = self.shares[share]["amount"] * self.shares[share]["price"]
                balance_delta += total_investment_value * self.shares[share]["dividend_yield"]
        
        self.balance = int(self.balance)
        self.balance += balance_delta

    def update_high_scores(self) -> None:
        try:
            self.get_game_info()

            high_scores_str: str = self.game_info[0]
            self.high_score = high_scores_str if high_scores_str else 0
        except FileNotFoundError:
            self.high_score = 0
            with open("game_info.txt", "w") as file:
                file.write("0\n")

        if str(self.balance) > self.high_score:
            self.high_score = self.balance
            with open("game_info.txt", "w") as file:
                file.write(str(self.high_score) + "\n")
    
    def update_share_values(self) -> None:
        for share in self.shares:
            self.shares[share]["value"] = random.randint(-500, 500)

    def update_share_prices(self) -> None:
        for share in self.shares:
            self.shares[share]["price"] = self.shares[share]["value"] + random.randint(-250, 250)
            if self.shares[share]["price"] < 1:
                self.shares[share]["price"] = random.randint(0, abs(self.shares[share]["price"]))

    def update_share_dividend_yield(self) -> None:
        for share in self.shares:
            self.shares[share]["dividend_yield"] = round(random.uniform(0, 0.05), 3)

    def update_game(self) -> None:
        while True:
            self.update_share_values()
            self.update_share_prices()
            self.update_share_dividend_yield()
            self.update_balance()
            self.update_high_scores()
            
            time.sleep(3)

if __name__ == "__main__":
    game = Game()
    game.start_game()
