import random
import json

# List of different categories of items
item_categories = {
    "electronics": [
        "Laptop", "Smartphone", "Tablet", "Smartwatch", "Camera", "Headphones", "Bluetooth Speaker",
        "Drone", "VR Headset", "Portable Charger"
    ],
    "home_appliances": [
        "Smart Oven", "Smart Microwave", "Smart Fan", "Smart Air Conditioner", "Smart Heater",
        "Smart Dishwasher", "Electric Fireplace", "Smart Security System", "Smart Lighting Kit", "Smart Blinds"
    ],
    "fitness": [
        "Treadmill", "Smart Weighing Scale", "Fitness Tracker", "Smart Water Bottle", "Yoga Mat", 
        "Exercise Bike", "Rowing Machine", "Resistance Bands", "Smart Jump Rope", "Smart Gym Mirror"
    ],
    "office_supplies": [
        "Wireless Keyboard", "Ergonomic Chair", "Desk Lamp", "Smart Desk", "Monitor", "Standing Desk",
        "Laptop Stand", "Noise Cancelling Headphones", "Webcam", "Smart Notepad"
    ],
    "kitchen_appliances": [
        "Smart Air Fryer", "Smart Pressure Cooker", "Smart Coffee Maker", "Blender", "Smart Toaster",
        "Smart Kettle", "Induction Cooktop", "Microwave Oven", "Smart Fridge", "Smart Wine Cooler"
    ]
}

# Function to generate random transactions
def generate_transactions(start_id, num_transactions, items_list):
    transactions = []
    current_amount = 100  # Starting amount
    for i in range(num_transactions):
        transaction_id = str(start_id + i)
        item = items_list[i % len(items_list)]  # Cycle through the items list
        transaction = {
            "transaction_id": transaction_id,
            "amount": current_amount,
            "item": item
        }
        transactions.append(transaction)
        current_amount += random.randint(10, 50)  # Increment amount randomly between 10 to 50
    return transactions

# Function to create files with transactions for different categories
def create_transaction_files():
    for category, items in item_categories.items():
        transactions = generate_transactions(1, 100, items)
        filename = f"{category}_transactions.json"
        with open(filename, "w") as f:
            json.dump(transactions, f, indent=4)
        print(f"{filename} created successfully.")

# Generate files
create_transaction_files()