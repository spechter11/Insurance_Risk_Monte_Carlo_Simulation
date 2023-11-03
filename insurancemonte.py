import logging
from scipy.stats import lognorm
import numpy as np

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def validate_parameters(freq_rate, prem, invest_return, exp_rate):
    """
    Validate the input parameters for the Monte Carlo simulation.

    Parameters:
    freq_rate (float): Frequency rate of claims, must be non-negative.
    prem (float): Premium amount, must be positive.
    invest_return (float): Investment return rate, must be between 0 and 1.
    exp_rate (float): Expense rate, must be between 0 and 1.

    Raises:
    ValueError: If any of the parameters are out of their expected range.
    """
    if freq_rate < 0:
        raise ValueError("Frequency rate must be non-negative")
    if prem <= 0:
        raise ValueError("Premiums must be positive")
    if not (0 <= invest_return <= 1):
        raise ValueError("Investment return rate must be between 0 and 1")
    if not (0 <= exp_rate <= 1):
        raise ValueError("Expense rate must be between 0 and 1")
    logging.info("All parameters are valid.")

def run_monte_carlo_simulation(num_simulations, freq_rate, mu_severity, sigma_severity, prem, invest_return, exp_rate):
    """
    Run a Monte Carlo simulation for insurance risk assessment.

    Parameters:
    num_simulations (int): Number of simulations to run.
    freq_rate (float): Frequency rate of claims.
    mu_severity (float): Mean of the log-normal distribution for claim severity.
    sigma_severity (float): Standard deviation of the log-normal distribution for claim severity.
    prem (float): Premium amount.
    invest_return (float): Investment return rate.
    exp_rate (float): Expense rate.

    Returns:
    np.array: Array of net outcomes from each simulation.

    Raises:
    Exception: Propagates any exceptions that occur during the simulation.
    """
    try:
        validate_parameters(freq_rate, prem, invest_return, exp_rate)
        results = []
        for _ in range(num_simulations):
            num_claims = np.random.poisson(freq_rate)
            total_claims = (sum(lognorm(s=sigma_severity, scale=np.exp(mu_severity)).rvs(num_claims))
                            if num_claims > 0 else 0)
            investment_income = prem * invest_return
            expenses = prem * exp_rate
            net_outcome = prem + investment_income - total_claims - expenses
            results.append(net_outcome)
        return np.array(results)
    except Exception as e:
        logging.error(f"An error occurred during simulation: {e}")
        raise

def main():
    """
    Main function to run the Monte Carlo simulation for insurance risk.
    """
    # Set the parameters
    freq_rate = 2  # Average number of claims per year
    median_sev = 5000  # Median of the claim severity
    coef_var = 1.0  # Coefficient of variation for the severity distribution
    prem = 50000  # Total annual premium
    invest_return = 0.05  # Investment return rate
    exp_rate = 0.10  # Expense rate
    num_simulations = 10000  # Number of Monte Carlo simulations

    logging.info("Starting the Monte Carlo simulation for insurance risk.")

    # Calculate the parameters for the log-normal severity distribution
    mu_severity = np.log(median_sev)  # Convert median to mean of the underlying normal distribution
    sigma_severity = np.sqrt(np.log(coef_var**2 + 1))  # Convert CV to standard deviation of the underlying normal distribution

    # Run the simulation
    simulation_results = run_monte_carlo_simulation(num_simulations, freq_rate, mu_severity, sigma_severity, prem, invest_return, exp_rate)

    # Calculate and print the results
    mean_result = np.mean(simulation_results)
    std_dev_result = np.std(simulation_results)
    probability_of_loss = np.mean(simulation_results < 0)
    logging.info(f"Mean result: {mean_result}")
    logging.info(f"Standard deviation: {std_dev_result}")
    logging.info(f"Probability of loss: {probability_of_loss}")

if __name__ == "__main__":
    main()
