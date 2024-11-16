import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv('decrypted_data/release_3611.csv')

# Step 2: Calculate historical statistics
strategy_stats = df.describe().T[['mean', 'std']]

# Step 3: Monte Carlo Simulation
num_simulations = 10000
time_horizon = 12  # Months

results = {}
np.random.seed(42)  # For reproducibility

for strategy in strategy_stats.index():
    mean = strategy_stats.loc[strategy, 'mean']
    std_dev = strategy_stats.loc[strategy, 'std']
    
    # Simulate returns for the strategy
    simulated_returns = np.random.normal(mean, std_dev, (num_simulations, time_horizon))
    
    # Calculate cumulative returns for each simulation
    cumulative_returns = np.cumprod(1 + simulated_returns, axis=1)[:, -1]
    results[strategy] = cumulative_returns

results_df = pd.DataFrame(results)

# Summary Statistics
summary_stats = results_df.describe()
print(summary_stats)

# # Calculate the average for each strat column (ignoring NaN)
# average_values = df.mean(axis=0, skipna=True)

# # Convert to a DataFrame for filtering and sorting
# average_df = average_values.reset_index()
# average_df.columns = ['Strat', 'Average Entry Value']

# # Filter for columns starting with 'strat_'
# average_df = average_df[average_df['Strat'].str.startswith('strat_')]

# # Sort by 'Average Entry Value' in ascending order
# average_df = average_df.sort_values(by='Average Entry Value')

# # Create a dictionary with strat names as keys and averages as values
# average_dict = dict(zip(average_df['Strat'], average_df['Average Entry Value']))
# average_dict['team_name'] = 'flatbros'
# average_dict['passcode'] = '6hours'


