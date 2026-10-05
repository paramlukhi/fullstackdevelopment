"""Beginner-friendly monthly electricity bill calculator."""

import math
import sys
from datetime import date


# Keep all business rules together so they are easy to change later.
SLABS = [
    (100, 2.50, "First 100 units"),
    (200, 4.00, "Next 200 units"),
    (300, 5.50, "Next 300 units"),
    (None, 7.00, "Above 600 units"),
]
FIXED_MONTHLY_FEE = 75.00
DISCOUNT_THRESHOLD = 100
DISCOUNT_RATE = 0.05
HIGH_USAGE_THRESHOLD = 600
SURCHARGE_RATE = 0.10
RUPEE_SYMBOL = "₹"


def calculate_energy_charge(units):
    """Return each slab's units and cost, plus the total energy charge."""
    remaining_units = units
    slab_details = []

    for limit, rate, description in SLABS:
        if remaining_units <= 0:
            break

        units_in_slab = remaining_units if limit is None else min(remaining_units, limit)
        slab_details.append(
            {
                "description": description,
                "units": units_in_slab,
                "rate": rate,
                "cost": round(units_in_slab * rate, 2),
            }
        )
        remaining_units -= units_in_slab

    total_energy_charge = round(sum(item["cost"] for item in slab_details), 2)
    return slab_details, total_energy_charge


def calculate_adjustment(units, energy_charge):
    """Return the adjustment label and amount applied to the energy charge."""
    if units < DISCOUNT_THRESHOLD:
        return "Discount", round(energy_charge * DISCOUNT_RATE, 2)
    if units > HIGH_USAGE_THRESHOLD:
        return "Surcharge", round(energy_charge * SURCHARGE_RATE, 2)
    return "No adjustment", 0.00


def generate_bill(customer_name, customer_id, units):
    """Build all bill components and calculate the final payable amount."""
    slab_details, energy_charge = calculate_energy_charge(units)
    adjustment_label, adjustment_amount = calculate_adjustment(units, energy_charge)
    adjustment_value = (
        -adjustment_amount if adjustment_label == "Discount" else adjustment_amount
    )
    final_amount = round(
        energy_charge + FIXED_MONTHLY_FEE + adjustment_value,
        2,
    )

    return {
        "customer_name": customer_name,
        "customer_id": customer_id,
        "bill_date": date.today().strftime("%d-%m-%Y"),
        "units": units,
        "slab_details": slab_details,
        "energy_charge": energy_charge,
        "fixed_fee": FIXED_MONTHLY_FEE,
        "adjustment_label": adjustment_label,
        "adjustment_amount": adjustment_amount,
        "final_amount": final_amount,
    }


def display_bill(bill):
    """Print a clear bill from the values stored in the bill dictionary."""
    print("\n" + "=" * 64)
    print("                  MONTHLY ELECTRICITY BILL")
    print("=" * 64)
    print(f"Customer name : {bill['customer_name']}")
    print(f"Customer ID   : {bill['customer_id']}")
    print(f"Bill date     : {bill['bill_date']}")
    print(f"Units consumed: {bill['units']:.2f}")
    print("-" * 64)
    print("                         BILL BREAKDOWN")
    print("-" * 64)
    print(f"{'Slab':<22}{'Units':>10}{'Rate':>12}{'Cost':>12}")
    print("-" * 64)

    if bill["slab_details"]:
        for slab in bill["slab_details"]:
            print(
                f"{slab['description']:<22}{slab['units']:>10.2f}"
                f"{(RUPEE_SYMBOL + format(slab['rate'], '.2f')):>12}"
                f"{(RUPEE_SYMBOL + format(slab['cost'], '.2f')):>12}"
            )
    else:
        print(
            f"{'No energy units':<22}{0:>10.2f}"
            f"{RUPEE_SYMBOL + '0.00':>12}{RUPEE_SYMBOL + '0.00':>12}"
        )

    print("-" * 64)
    print(
        f"{'Total energy charges':<44}"
        f"{RUPEE_SYMBOL}{bill['energy_charge']:>9.2f}"
    )
    print(f"{'Fixed monthly fee':<44}{RUPEE_SYMBOL}{bill['fixed_fee']:>9.2f}")
    print(
        f"{bill['adjustment_label']:<44}"
        f"{RUPEE_SYMBOL}{bill['adjustment_amount']:>9.2f}"
    )
    print("=" * 64)
    print(
        f"{'FINAL AMOUNT PAYABLE':<44}"
        f"{RUPEE_SYMBOL}{bill['final_amount']:>9.2f}"
    )
    print("=" * 64)


def read_required_text(prompt):
    """Keep asking until the user enters non-empty text."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Error: this field cannot be empty. Please try again.")


def read_menu_choice():
    """Read one of the two available menu options."""
    while True:
        print("\n1. Calculate New Bill")
        print("2. Exit")
        choice = input("Enter your choice: ").strip()
        if choice in {"1", "2"}:
            return choice
        print("Error: please enter 1 to calculate a bill or 2 to exit.")


def read_yes_no(prompt):
    """Read a yes or no response."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Error: please enter yes or no.")


def read_units():
    """Read a non-negative number of units without crashing on bad input."""
    while True:
        raw_units = input("Total units consumed: ").strip()
        try:
            units = float(raw_units)
        except ValueError:
            print("Error: enter a numeric unit value, such as 250 or 250.5.")
            continue

        if not math.isfinite(units) or units < 0:
            print("Error: units must be a finite, non-negative number.")
            continue
        return units


def run_manual_tests():
    """Check normal, boundary, zero, and invalid-input-related cases."""
    expected_energy = {
        0: 0.00,
        50: 125.00,
        100: 250.00,
        250: 850.00,
        600: 2_700.00,
        601: 2_707.00,
    }

    for units, expected_charge in expected_energy.items():
        _, energy_charge = calculate_energy_charge(units)
        assert energy_charge == expected_charge, (units, energy_charge)

    assert calculate_adjustment(50, 125.00) == ("Discount", 6.25)
    assert calculate_adjustment(600, 2_700.00) == ("No adjustment", 0.00)
    assert calculate_adjustment(601, 2_707.00) == ("Surcharge", 270.70)

    zero_bill = generate_bill("Test Customer", "TEST-0", 0)
    assert zero_bill["final_amount"] == 75.00
    assert zero_bill["bill_date"] == date.today().strftime("%d-%m-%Y")

    # Input validation is performed by read_units; negative/text cases retry.
    print("All manual calculation tests passed.")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_manual_tests()
        return

    print("\n" + "=" * 40)
    print("       ELECTRICITY BILL CALCULATOR")
    print("=" * 40)

    while True:
        if read_menu_choice() == "2":
            print("Thank you for using the Electricity Bill Calculator.")
            break

        customer_name = read_required_text("Customer name: ")
        customer_id = read_required_text("Customer ID or account number: ")
        units = read_units()
        display_bill(generate_bill(customer_name, customer_id, units))

        if not read_yes_no("Do you want to calculate another bill? (yes/no): "):
            print("Thank you for using the Electricity Bill Calculator.")
            break


if __name__ == "__main__":
    main()