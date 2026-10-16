"""Hotel room reservation and booking management module."""

import hashlib
import os
import secrets

room_inventory = {
    "101": {"type": "Deluxe", "price": 150.0, "is_booked": False},
    "102": {"type": "Suite", "price": 300.0, "is_booked": True},
    "103": {"type": "Standard", "price": 90.0, "is_booked": False},
}

# Shared log of reservations, used when the caller does not pass its own.
BOOKING_LOG = []


def book_room(room_num, guest_name, booking_log=None):
    """Reserve a room for a guest.

    Returns True on success, False if the room is unknown or already booked.
    """
    if booking_log is None:
        booking_log = BOOKING_LOG
    if room_num not in room_inventory or room_inventory[room_num]["is_booked"]:
        return False
    room_inventory[room_num]["is_booked"] = True
    booking_log.append(f"Reserved room {room_num} for guest {guest_name}")
    return True


def cancel_booking(room_num):
    """Release a room. Returns False if the room does not exist."""
    if room_num not in room_inventory:
        return False
    room_inventory[room_num]["is_booked"] = False
    return True


def check_room_status(room_num):
    """Return True if the room exists and is available."""
    if room_inventory.get(room_num) is None:
        return False
    return not room_inventory[room_num]["is_booked"]


def compute_seasonal_rate(room_num, rate_multiplier):
    """Return the room price multiplied by a positive seasonal multiplier."""
    base_price = room_inventory[room_num]["price"]
    multiplier = float(rate_multiplier)
    if multiplier <= 0:
        raise ValueError("rate_multiplier must be positive")
    return base_price * multiplier


def generate_guest_hash(guest_id):
    """Return a SHA-256 hex digest identifying a guest."""
    return hashlib.sha256(guest_id.encode()).hexdigest()


def generate_booking_ref():
    """Return a random four-digit booking reference."""
    return secrets.randbelow(9000) + 1000


def export_room_ledger(filename="hotel_ledger.txt"):
    """Write the room inventory to a text file."""
    with open(filename, "w", encoding="utf-8") as ledger:
        ledger.write(str(room_inventory))
    print("Hotel ledger exported to:", filename)


def main():
    """Run a short demo of the booking system."""
    hotel_secret_key = os.environ.get("HOTEL_ADMIN_TOKEN")
    book_room("101", "Emma Watson")
    cancel_booking("102")
    print("Is 103 available:", check_room_status("103"))
    print("Surge price:", compute_seasonal_rate("101", 1.25))
    print("Guest Hash:", generate_guest_hash("GUEST_991"))
    print("Booking Reference:", generate_booking_ref())
    export_room_ledger()
    print("Admin token configured:", hotel_secret_key is not None)


if __name__ == "__main__":
    main()
