import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the CSV file
strategy_stats = pd.read_csv('decrypted_data/release_3611.csv')


# Step 2: Calculate the mean returns of each strategy
# The column headings are the strategy names, and the rows are the historical returns.
strategy_means = strategy_stats.mean()


def monte_carlo_portfolio_simulation(strategy_means, max_exposure=0.1, num_simulations=1000):
    n_strategies = len(strategy_means)
    portfolio_returns = []
    portfolio_allocations = []

    # Run simulations
    for _ in range(num_simulations):
        # Generate random portfolio weights (between 0 and max_exposure for each strategy)
        weights = np.random.uniform(0, max_exposure, n_strategies)

        # Normalize the weights so that they sum to 1 (fully invested portfolio)
        weights /= np.sum(weights)

        # Create a dictionary of the portfolio allocation using strategy names as keys
        allocation_dict = {f"strat_{i+1}": float(weight) for i, weight in enumerate(weights)}

        # Calculate portfolio return for the current set of weights
        portfolio_return = sum(weights[i] * strategy_means[i] for i in range(len(strategy_means)))

        # Store the portfolio return and allocation dictionary
        portfolio_returns.append(portfolio_return)
        portfolio_allocations.append(allocation_dict)

    # Return the portfolio returns and the portfolio allocations
    return portfolio_returns, portfolio_allocations

# Step 4: Run the Monte Carlo simulation
num_simulations = 1000  # Number of simulations to run
portfolio_returns, portfolio_allocations = monte_carlo_portfolio_simulation(strategy_means, num_simulations=num_simulations)

# Step 5: Find the best portfolio allocation (highest expected return)
best_return_index = np.argmax(portfolio_returns)
best_allocation = portfolio_allocations[best_return_index]

# Step 6: Create the final dictionary with strategy names and their weightings
final_allocation_dict = best_allocation  # The best allocation is already in the required dictionary form
final_allocation_dict['team_name'] = 'flatbros'
final_allocation_dict['passcode'] = '6hours'

# Step 7: Display the best portfolio allocation
print("Best Portfolio Allocation (Highest Return):")
print(final_allocation_dict)
print(f"Best Portfolio Return: {portfolio_returns[best_return_index]}")