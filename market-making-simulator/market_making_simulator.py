"""Educational, event-driven market-making simulator.

This model uses a predefined sequence of customer orders. It is a learning
project, not a realistic exchange simulator or a trading recommendation.
"""

import csv
from pathlib import Path


# ------------------------------------------------------------
# 1. SIMULATION SETTINGS
# ------------------------------------------------------------
INITIAL_CASH = 10_000.00
HALF_SPREAD = 0.50       # Quote half-spread; full bid-ask spread is 1.00
FEE_PER_UNIT = 0.02      # Fee charged for each executed unit
MAX_ABS_INVENTORY = 3    # Do not allow inventory above +3 or below -3
OUTPUT_CSV = Path("simulation_results.csv")


# ------------------------------------------------------------
# 2. EXAMPLE CUSTOMER ORDER FLOW
# SELL means the customer sells to the market maker (maker buys).
# BUY means the customer buys from the market maker (maker sells).
# ------------------------------------------------------------
EVENTS = [
    {"time": 1, "mid": 100.00, "customer": "SELL", "qty": 2},
    {"time": 2, "mid": 100.20, "customer": "BUY",  "qty": 1},
    {"time": 3, "mid": 100.60, "customer": "BUY",  "qty": 2},
    {"time": 4, "mid": 100.30, "customer": "SELL", "qty": 1},
    {"time": 5, "mid": 99.70,  "customer": "SELL", "qty": 2},
    {"time": 6, "mid": 99.40,  "customer": "SELL", "qty": 2},
]


def run_simulation(events=EVENTS):
    """Process each event and return the ledger plus final portfolio state."""
    cash = INITIAL_CASH
    inventory = 0
    ledger = []
    accepted_orders = 0
    rejected_orders = 0
    last_mid_price = None

    for event in events:
        time = event["time"]
        mid_price = float(event["mid"])
        customer_side = event["customer"].upper()
        quantity = int(event["qty"])
        last_mid_price = mid_price

        if mid_price <= 0:
            raise ValueError("Mid-price must be greater than zero.")
        if quantity <= 0:
            raise ValueError("Order quantity must be greater than zero.")
        if customer_side not in ("BUY", "SELL"):
            raise ValueError(f"Unknown customer side: {customer_side}")

        bid = mid_price - HALF_SPREAD
        ask = mid_price + HALF_SPREAD
        fill_quantity = 0

        if customer_side == "SELL":
            # Customer sells, so the market maker buys at the bid.
            proposed_inventory = inventory + quantity
            if proposed_inventory <= MAX_ABS_INVENTORY:
                execution_price = bid
                cash -= execution_price * quantity
                cash -= FEE_PER_UNIT * quantity
                inventory = proposed_inventory
                fill_quantity = quantity
                action = f"BUY {quantity} @ {execution_price:.2f}"
                accepted_orders += 1
            else:
                action = "REJECTED: INVENTORY LIMIT"
                rejected_orders += 1

        else:  # customer_side == "BUY"
            # Customer buys, so the market maker sells at the ask.
            proposed_inventory = inventory - quantity
            if proposed_inventory >= -MAX_ABS_INVENTORY:
                execution_price = ask
                cash += execution_price * quantity
                cash -= FEE_PER_UNIT * quantity
                inventory = proposed_inventory
                fill_quantity = quantity
                action = f"SELL {quantity} @ {execution_price:.2f}"
                accepted_orders += 1
            else:
                action = "REJECTED: INVENTORY LIMIT"
                rejected_orders += 1

        # Mark the remaining position to the current mid-price.
        inventory_value = inventory * mid_price
        portfolio_value = cash + inventory_value
        pnl = portfolio_value - INITIAL_CASH

        ledger.append(
            {
                "time": time,
                "mid_price": mid_price,
                "customer_side": customer_side,
                "requested_qty": quantity,
                "bid": bid,
                "ask": ask,
                "action": action,
                "fill_qty": fill_quantity,
                "inventory": inventory,
                "cash": round(cash, 2),
                "inventory_value": round(inventory_value, 2),
                "portfolio_value": round(portfolio_value, 2),
                "pnl": round(pnl, 2),
            }
        )

    if last_mid_price is None:
        raise ValueError("The simulation needs at least one event.")

    final_inventory_value = inventory * last_mid_price
    final_portfolio_value = cash + final_inventory_value
    final_pnl = final_portfolio_value - INITIAL_CASH

    summary = {
        "initial_cash": INITIAL_CASH,
        "final_cash": round(cash, 2),
        "final_inventory": inventory,
        "last_mid_price": round(last_mid_price, 2),
        "final_inventory_value": round(final_inventory_value, 2),
        "final_portfolio_value": round(final_portfolio_value, 2),
        "final_pnl": round(final_pnl, 2),
        "accepted_orders": accepted_orders,
        "rejected_orders": rejected_orders,
    }
    return ledger, summary


def write_csv(ledger, output_path=OUTPUT_CSV):
    """Save the event-by-event simulation ledger as a CSV file."""
    if not ledger:
        return
    fieldnames = list(ledger[0].keys())
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(ledger)


def print_report(ledger, summary):
    """Print a readable event log and final summary."""
    print("\nMARKET-MAKING SIMULATOR — EDUCATIONAL MODEL")
    print("=" * 112)
    print(
        f"{'T':>2} | {'MID':>7} | {'CUSTOMER':>8} | {'QTY':>3} | "
        f"{'MAKER ACTION':<28} | {'INV':>3} | {'CASH':>10} | "
        f"{'PORTFOLIO':>10} | {'P&L':>8}"
    )
    print("-" * 112)

    for row in ledger:
        print(
            f"{row['time']:>2} | {row['mid_price']:>7.2f} | "
            f"{row['customer_side']:>8} | {row['requested_qty']:>3} | "
            f"{row['action']:<28} | {row['inventory']:>3} | "
            f"{row['cash']:>10.2f} | {row['portfolio_value']:>10.2f} | "
            f"{row['pnl']:>8.2f}"
        )

    print("-" * 112)
    print(f"Initial cash:                 {summary['initial_cash']:.2f}")
    print(f"Final cash:                   {summary['final_cash']:.2f}")
    print(f"Final inventory:              {summary['final_inventory']}")
    print(f"Final inventory market value: {summary['final_inventory_value']:.2f}")
    print(f"Final portfolio value:        {summary['final_portfolio_value']:.2f}")
    print(f"Final P&L:                    {summary['final_pnl']:.2f}")
    print(f"Accepted orders:              {summary['accepted_orders']}")
    print(f"Rejected orders:              {summary['rejected_orders']}")


def main():
    ledger, summary = run_simulation()
    print_report(ledger, summary)
    write_csv(ledger)
    print(f"\nEvent ledger saved to: {OUTPUT_CSV.resolve()}")


if __name__ == "__main__":
    main()
