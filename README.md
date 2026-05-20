# Real Estate Rental Check

Analyze a rental property investment from the command line. Models monthly cash flow, key return metrics, and 30-year projections.

## Requirements

Python 3.6+. No third-party packages needed.

## Usage

```bash
python3 analyze.py --price <purchase_price> --rent <monthly_rent> --rate <interest_rate> [options]
```

### Required arguments

| Flag | Description |
|---|---|
| `--price` | Purchase price ($) |
| `--rent` | Monthly rent ($) |
| `--rate` | Annual mortgage interest rate (%) |

### Optional arguments

| Flag | Default | Description |
|---|---|---|
| `--appreciation` | 3.0 | Annual property appreciation rate (%) |
| `--down` | 20.0 | Down payment (%) |
| `--utilities` | 0 | Monthly utilities paid by owner ($) |
| `--maintenance` | 1.0 | Annual maintenance as % of property value |
| `--occupancy` | 95.0 | Expected occupancy rate (%) |
| `--loan-term` | 30 | Loan term in years |

## Example

```bash
python3 analyze.py \
  --price 400000 \
  --rent 2500 \
  --rate 6.5 \
  --appreciation 3.0 \
  --down 20 \
  --utilities 150 \
  --maintenance 1.0 \
  --occupancy 95
```

Output:

```
====================================================
  RENTAL PROPERTY ANALYSIS
====================================================

  INPUTS
----------------------------------------------------
  Purchase Price:        $     400,000
  Down Payment (20%):    $      80,000
  Loan Amount:           $     320,000
  Interest Rate:                6.50%
  Loan Term:                      30 yrs
  Monthly Rent:          $       2,500
  Appreciation Rate:            3.00%
  Occupancy Rate:               95.0%
  Monthly Utilities:     $         150
  Maintenance (1.0%/yr):  $         333/mo

  MONTHLY CASH FLOW
----------------------------------------------------
  Effective Rent:        $       2,375
  Mortgage Payment:     -$       2,023
  Utilities:            -$         150
  Maintenance:          -$         333
  ──────────────────────────────────────
  Net Cash Flow:         $        -131

  KEY METRICS
----------------------------------------------------
  Cap Rate:                     5.67%
  Cash-on-Cash Return:         -1.96%
  Gross Rent Multiplier:         13.3x
  Break-even Occupancy:        100.2%
  Annual Cash Flow:      $      -1,571

  PROJECTIONS
----------------------------------------------------
  Year         Value        Equity       Cum. CF  Total Return
  ────  ────────────  ────────────  ────────────  ────────────
     1  $    412,000  $     95,577  $     -1,571  $    +14,005
     2  $    424,360  $    111,753  $     -3,143  $    +28,610
     3  $    437,091  $    128,556  $     -4,714  $    +43,841
     5  $    463,710  $    164,155  $     -7,857  $    +76,297
    10  $    537,567  $    266,283  $    -15,714  $   +170,569
    20  $    722,444  $    544,316  $    -31,428  $   +432,887
    30  $    970,905  $    970,905  $    -47,142  $   +843,763
====================================================
```

## Metrics explained

- **Cap Rate** — Net operating income (before financing) as a % of purchase price. Higher is better; 5–8% is typical for rentals.
- **Cash-on-Cash Return** — Annual cash flow as a % of cash invested (down payment). Measures actual return on your out-of-pocket money.
- **Gross Rent Multiplier (GRM)** — Purchase price divided by annual gross rent. Lower means cheaper relative to rent; under 15x is generally favorable.
- **Break-even Occupancy** — The occupancy rate at which cash flow equals zero. Below your expected occupancy means positive cash flow.
- **Total Return** — Equity gained (appreciation + principal paydown) plus cumulative cash flow, minus initial down payment.
