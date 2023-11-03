
# Insurance Risk Monte Carlo Simulation

This project contains a Python script that performs a Monte Carlo simulation to assess insurance risk based on claim frequency, claim severity, premiums, investment returns, and expense rates.

## Description

The script uses a stochastic model to simulate the net outcome of insurance claims and income over a specified number of simulations. It helps in understanding the risk of loss and the variability of results in an insurance company's operations.

## Installation

To run this project, you will need Python and the packages listed in `requirements.txt`. Install them using:

```bash
pip install -r requirements.txt
```

## Usage

To run the simulation, execute the main script:

```bash
python monte_carlo_simulation.py
```

## Output

The script will output the following statistics from the Monte Carlo simulation:

- Mean result of the net outcome
- Standard deviation of the net outcome
- Probability of a loss

These results will be logged to the console.
