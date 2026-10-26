
# Inventory-Aware Market-Making Simulator

## Overview

An educational Python project that simulates a market maker quoting bid and ask prices, trading against a predefined sequence of customer orders, tracking inventory, and calculating mark-to-market profit and loss (P&L).

## Features

- Bid and ask quote construction from a mid-price
- Cash and inventory accounting
- Per-unit transaction fees
- Inventory limits and order rejection
- Mark-to-market portfolio valuation
- Event-by-event reporting
- CSV export of simulation results

## Model

For mid-price `mid` and half-spread `s`:

- `bid = mid - s`
- `ask = mid + s`
- `spread = ask - bid`

Portfolio value is calculated as:

`portfolio value = cash + inventory * mid-price`

P&L is calculated as:

`P&L = portfolio value - initial cash`

## Example configuration

- Initial cash: 10,000
- Half-spread: 0.50
- Transaction fee: 0.02 per executed unit
- Maximum absolute inventory: 3 units

## Example results

- Final cash: 9,805.54
- Final inventory: 2 units
- Final portfolio value: 10,004.34
- Final P&L: +4.34
- Accepted orders: 5
- Rejected orders: 1

These results come from a fixed illustrative sequence of six events.

## Limitations

This is an educational simulation, not a historical backtest. Prices and customer orders are predefined. The model does not include a realistic limit order book, queue position, latency, market impact, or adverse selection.

The positive P&L in the example does not demonstrate that the strategy is profitable in live markets.

## Technologies

- Python
- CSV
