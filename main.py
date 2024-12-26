from menu import MENU

COMMANDS = ["espresso", "latte", "cappuccino", "report", "off"]

def command_handler(input_string):
  while True:
    response = input(input_string)
    if response.lower() in COMMANDS:
      return response.lower()
    print("Unknown command")

resources = {
  "water": 300,
  "milk": 200,
  "coffee": 100,
}

resources_output = {
  "water": lambda: f"{resources["water"]}ml",
  "milk": lambda: f"{resources["milk"]}ml",
  "coffee": lambda: f"{resources["coffee"]}g",
  "money": lambda: f"${resources["money"]:.2f}",
}  

def print_report():
  for resource in resources:
    print(f"{resource.title()}: {resources_output[resource]()}")

def check_resources(drink):
  sufficient_resources = True
  for ingredient in drink["ingredients"]:
    required = drink["ingredients"][ingredient]
    supply = resources[ingredient]
    if required > supply:
      sufficient_resources = False
      print(f"Sorry, there is not enough {ingredient} to meet your request")
  return sufficient_resources

currency = {
  "quarters": 0.25,
  "dimes": 0.1,
  "nickels": 0.05,
  "pennies": 0.01,
}

def coin_handler(input_string):
  while True:
    try:
      response = int(input(input_string))
      return response
    except ValueError:
      print("Please enter a number")

def process_drink(selected_drink):
  drink = MENU[selected_drink]
  if not check_resources(drink):
    return
  print(f"{selected_drink.title()}: ${drink["cost"]:.2f}")
  print("Insert coins:")
  inserted_money = 0
  for coins in currency:
    input_string = f"How many {coins}?: "
    coin_amount = coin_handler(input_string)
    inserted_money += coin_amount * currency[coins]
  if inserted_money >= drink["cost"]:
    change = inserted_money - drink["cost"]
    if change:
      print(f"Here is ${change:.2f} dollars in change.")
  else:
    print("Sorry that's not enough money. Money refunded.")
    return
  resources["money"] = resources.get("money", 0) + drink["cost"]
  for ingredient in drink["ingredients"]:
    resources[ingredient] -= drink["ingredients"][ingredient]
  print(f"Here is your {selected_drink}. Enjoy!")

ON = True
def turn_off():
  global ON
  ON = False

COMMAND_FUNCTIONS = {
  "off": turn_off,
  "report": print_report,
}

drinks = ["espresso", "latte", "cappuccino"]
COMMAND_FUNCTIONS.update({ drink: process_drink for drink in drinks })

while ON:
  user_selection = command_handler(" What would you like? (espresso/latte/cappuccino): ")
  if user_selection in drinks:
    COMMAND_FUNCTIONS[user_selection](user_selection)
  else:
    COMMAND_FUNCTIONS[user_selection]()
