import hashlib
from datetime import datetime


# Helper function for password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Initial Data
users = {
    "EMP123": {"password": hash_password("password123"), "name": "John Doe"}
}

rides = [
    {"ride_id": 1, "origin": "Station A", "destination": "Station B", "vehicle_type": "2-wheeler", "distance_km": 10, "available": True},
    {"ride_id": 2, "origin": "Station B", "destination": "Station C", "vehicle_type": "4-wheeler", "distance_km": 15, "available": True},
    {"ride_id": 3, "origin": "Station A", "destination": "Station C", "vehicle_type": "2-wheeler", "distance_km": 20, "available": True},
]

active_rides = {}  # Tracks active rides: {employee_id: (ride_id, start_time)}


# Fare rates in INR
FARE_RATES = {
    "2-wheeler": {"per_km": 5, "per_minute": 1},
    "4-wheeler": {"per_km": 12, "per_minute": 2},
}


# Features
def login():
    employee_id = input("Enter Employee ID: ").strip()
    password = input("Enter Password: ").strip()
    hashed_pw = hash_password(password)

    if employee_id in users and users[employee_id]["password"] == hashed_pw:
        print(f"Welcome {users[employee_id]['name']}!")
        return employee_id
    else:
        print("Invalid Employee ID or Password!")
        return None


def show_available_rides():
    print("\nAvailable Rides:")
    for ride in rides:
        if ride["available"]:
            print(
                f"Ride ID: {ride['ride_id']}, Origin: {ride['origin']}, Destination: {ride['destination']}, "
                f"Vehicle Type: {ride['vehicle_type']}, Distance: {ride['distance_km']} km"
            )
    print()


def start_ride(employee_id):
    if employee_id in active_rides:
        print("You already have an active ride. End the current ride first.")
        return

    origin = input("Enter your starting point (origin): ").strip()
    destination = input("Enter your destination: ").strip()

    matching_rides = [
        ride for ride in rides if ride["origin"].lower() == origin.lower() and
                                  ride["destination"].lower() == destination.lower() and
                                  ride["available"]
    ]

    if not matching_rides:
        print("No matching rides available for the specified origin and destination.")
        return

    print("\nMatching Rides:")
    for ride in matching_rides:
        print(
            f"Ride ID: {ride['ride_id']}, Vehicle Type: {ride['vehicle_type']}, Distance: {ride['distance_km']} km"
        )

    ride_id = ride['ride_id']

    for ride in matching_rides:
        if ride["ride_id"] == ride_id:
            ride["available"] = False
            active_rides[employee_id] = (ride_id, datetime.now())
            print(f"Ride {ride_id} started. Drive safely!")
            return

    print("Invalid Ride ID. Please try again.")


def end_ride(employee_id):
    if employee_id not in active_rides:
        print("You don't have an active ride to end.")
        return

    ride_id, start_time = active_rides.pop(employee_id)
    end_time = datetime.now()

    duration_minutes = (end_time - start_time).seconds // 60

    for ride in rides:
        if ride["ride_id"] == ride_id:
            distance_km = ride["distance_km"]
            vehicle_type = ride["vehicle_type"]

            fare = (
                distance_km * FARE_RATES[vehicle_type]["per_km"] +
                duration_minutes * FARE_RATES[vehicle_type]["per_minute"]
            )

            ride["available"] = True  # Make ride available again
            print(f"\nRide {ride_id} ended.")
            print(f"Duration: {duration_minutes} minutes, Distance: {distance_km} km.")
            print(f"Total Fare: ₹{fare:.2f}")
            return


# New function to register a ride
def register_ride():
    origin = input("Enter your starting point (origin): ").strip()
    destination = input("Enter your destination: ").strip()
    vehicle_type = input("Enter vehicle type (2-wheeler or 4-wheeler): ").strip().lower()

    if vehicle_type not in FARE_RATES:
        print("Invalid vehicle type. Please choose between '2-wheeler' or '4-wheeler'.")
        return

    try:
        distance_km = float(input("Enter the distance for this ride in km: ").strip())
    except ValueError:
        print("Invalid distance. Please enter a valid number.")
        return

    ride_id = len(rides) + 1  # Generate new ride ID

    new_ride = {
        "ride_id": ride_id,
        "origin": origin,
        "destination": destination,
        "vehicle_type": vehicle_type,
        "distance_km": distance_km,
        "available": True
    }

    rides.append(new_ride)
    print(f"New ride registered successfully: {new_ride}")


# Main Application Loop
def main():
    while True:
        print("\nCar Sharing App")
        print("1. Login")
        print("2. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            employee_id = login()
            if employee_id:
                while True:
                    print("\nDashboard")
                    print("1. Show Available Rides")
                    print("2. Start a Ride")
                    print("3. End a Ride")
                    print("4. Register a Ride (For Driver)")
                    print("5. Logout")

                    dashboard_choice = input("Enter your choice: ").strip()
                    if dashboard_choice == "1":
                        show_available_rides()
                    elif dashboard_choice == "2":
                        start_ride(employee_id)
                    elif dashboard_choice == "3":
                        end_ride(employee_id)
                    elif dashboard_choice == "4":
                        register_ride()
                    elif dashboard_choice == "5":
                        print("Logging out...")
                        break
                    else:
                        print("Invalid choice. Please try again.")
        
        elif choice == "2":
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
