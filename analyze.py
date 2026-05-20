#!/usr/bin/env python3
"""Rental property investment analyzer."""

import argparse


def monthly_mortgage_payment(principal: float, annual_rate: float, years: int) -> float:
    r = annual_rate / 100 / 12
    n = years * 12
    if r == 0:
        return principal / n
    return principal * r * (1 + r) ** n / ((1 + r) ** n - 1)


def remaining_loan_balance(principal: float, annual_rate: float, years: int, months_paid: int) -> float:
    r = annual_rate / 100 / 12
    n = years * 12
    if r == 0:
        return principal * (1 - months_paid / n)
    return principal * ((1 + r) ** n - (1 + r) ** months_paid) / ((1 + r) ** n - 1)


def analyze(
    price: float,
    rent: float,
    appreciation: float,
    rate: float,
    down_pct: float,
    utilities: float,
    maintenance_pct: float,
    occupancy: float,
    loan_term: int,
) -> None:
    down = price * down_pct / 100
    loan = price - down
    mortgage = monthly_mortgage_payment(loan, rate, loan_term)

    monthly_maintenance = (price * maintenance_pct / 100) / 12
    effective_rent = rent * occupancy / 100

    monthly_income = effective_rent
    monthly_expenses = mortgage + utilities + monthly_maintenance
    monthly_cash_flow = monthly_income - monthly_expenses
    annual_cash_flow = monthly_cash_flow * 12

    # NOI excludes financing costs
    annual_noi = (effective_rent - utilities - monthly_maintenance) * 12
    cap_rate = annual_noi / price * 100
    cash_on_cash = annual_cash_flow / down * 100
    grm = price / (rent * 12)

    # Break-even occupancy
    monthly_expenses_no_occupancy = mortgage + utilities + monthly_maintenance
    breakeven_occupancy = monthly_expenses_no_occupancy / rent * 100

    # --- Output ---
    sep = "-" * 52
    wide_sep = "=" * 52

    print(wide_sep)
    print("  RENTAL PROPERTY ANALYSIS")
    print(wide_sep)

    print("\n  INPUTS")
    print(sep)
    print(f"  Purchase Price:        ${price:>12,.0f}")
    print(f"  Down Payment ({down_pct:.0f}%):    ${down:>12,.0f}")
    print(f"  Loan Amount:           ${loan:>12,.0f}")
    print(f"  Interest Rate:         {rate:>11.2f}%")
    print(f"  Loan Term:             {loan_term:>11} yrs")
    print(f"  Monthly Rent:          ${rent:>12,.0f}")
    print(f"  Appreciation Rate:     {appreciation:>11.2f}%")
    print(f"  Occupancy Rate:        {occupancy:>11.1f}%")
    print(f"  Monthly Utilities:     ${utilities:>12,.0f}")
    print(f"  Maintenance ({maintenance_pct:.1f}%/yr):  ${monthly_maintenance:>12,.0f}/mo")

    print("\n  MONTHLY CASH FLOW")
    print(sep)
    print(f"  Effective Rent:        ${effective_rent:>12,.0f}")
    print(f"  Mortgage Payment:     -${mortgage:>12,.0f}")
    print(f"  Utilities:            -${utilities:>12,.0f}")
    print(f"  Maintenance:          -${monthly_maintenance:>12,.0f}")
    print(f"  {'─'*38}")
    print(f"  Net Cash Flow:         ${monthly_cash_flow:>+12,.0f}")

    print("\n  KEY METRICS")
    print(sep)
    print(f"  Cap Rate:              {cap_rate:>11.2f}%")
    print(f"  Cash-on-Cash Return:   {cash_on_cash:>11.2f}%")
    print(f"  Gross Rent Multiplier: {grm:>12.1f}x")
    print(f"  Break-even Occupancy:  {breakeven_occupancy:>11.1f}%")
    print(f"  Annual Cash Flow:      ${annual_cash_flow:>+12,.0f}")

    print("\n  PROJECTIONS")
    print(sep)
    print(f"  {'Year':>4}  {'Value':>12}  {'Equity':>12}  {'Cum. CF':>12}  {'Total Return':>12}")
    print(f"  {'─'*4}  {'─'*12}  {'─'*12}  {'─'*12}  {'─'*12}")

    cumulative_cf = 0.0
    prev_yr = 0
    for yr in [1, 2, 3, 5, 10, 20, 30]:
        if yr > loan_term:
            balance = 0.0
        else:
            balance = remaining_loan_balance(loan, rate, loan_term, yr * 12)
        value = price * (1 + appreciation / 100) ** yr
        equity = value - balance
        cumulative_cf += annual_cash_flow * (yr - prev_yr)
        total_return = equity - down + cumulative_cf
        print(f"  {yr:>4}  ${value:>11,.0f}  ${equity:>11,.0f}  ${cumulative_cf:>+11,.0f}  ${total_return:>+11,.0f}")
        prev_yr = yr

    print(wide_sep)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze a rental property investment.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--price", type=float, required=True, help="Purchase price ($)")
    parser.add_argument("--rent", type=float, required=True, help="Monthly rent ($)")
    parser.add_argument("--rate", type=float, required=True, help="Annual mortgage interest rate (%%)")
    parser.add_argument("--appreciation", type=float, default=3.0, help="Annual appreciation rate (%%)")
    parser.add_argument("--down", type=float, default=20.0, help="Down payment (%%)")
    parser.add_argument("--utilities", type=float, default=0.0, help="Monthly utilities paid by owner ($)")
    parser.add_argument("--maintenance", type=float, default=1.0, help="Annual maintenance as %% of property value")
    parser.add_argument("--occupancy", type=float, default=95.0, help="Occupancy rate (%%)")
    parser.add_argument("--loan-term", type=int, default=30, help="Loan term (years)")

    args = parser.parse_args()

    analyze(
        price=args.price,
        rent=args.rent,
        appreciation=args.appreciation,
        rate=args.rate,
        down_pct=args.down,
        utilities=args.utilities,
        maintenance_pct=args.maintenance,
        occupancy=args.occupancy,
        loan_term=args.loan_term,
    )


if __name__ == "__main__":
    main()
