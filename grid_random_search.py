# %pip install numpy
#%pip install matplotlib
import numpy as np
import matplotlib.pyplot as plt

# Parameters
num_periods = 252  # Assume 252 trading days in a year
initial_price = 1000  # Initial stock price
# ばらつき＝標準偏差
volatility = 0.02  # Daily volatility

# # Generate random walk
# prices = [initial_price]
# for _ in range(num_periods):
#     prices.append(prices[-1] + prices[-1] * volatility * np.random.randn())

# # Plot the results
# plt.figure(figsize=(10,6))
# plt.plot(prices)
# plt.title("Random Walk Simulation of Stock Price")
# plt.xlabel("Days")
# plt.ylabel("Stock Price")
# plt.grid(True)
# plt.show()

def simulate_geometric_brownian_motion(num_periods, initial_price, mu, sigma, num_trials):
    dt = 1  # Time increment (1 day)
    all_prices = []
    
    for _ in range(num_trials):
        prices = [initial_price]
        for _ in range(num_periods):
            dS = prices[-1] * (mu * dt + sigma * np.sqrt(dt) * np.random.randn())
            prices.append(prices[-1] + dS)
        all_prices.append(prices)
    
    return all_prices

# Parameters
mu = 0.0005  # Expected daily return (approximate)

# # Parameters
num_trials = 10  # Number of random walk simulations

# Simulate geometric brownian motion
all_prices = simulate_geometric_brownian_motion(num_periods, initial_price, mu, volatility, num_trials)


# %pip install scipy
# %pip install numpy
from scipy.optimize import minimize
import numpy as np

# Step 1: Generate "real" data using geometric brownian motion (as a placeholder for actual data)
real_prices = simulate_geometric_brownian_motion(num_periods, initial_price, 0.0004, 0.02, 1)[0]

# Step 2: Define the objective function
def objective_function(params):
    mu, sigma = params
    simulated_prices = simulate_geometric_brownian_motion(num_periods, initial_price, mu, sigma, 1)[0]
    error = np.sum((np.array(simulated_prices) - np.array(real_prices))**2)
    return error

# Test the objective function
objective_function((0.0005, 0.02))

# Step 3: Parameter search



# Grid Search
mu_values = np.linspace(0.0001, 0.001, 10)
sigma_values = np.linspace(0.01, 0.03, 10)
best_score = float('inf')
best_params = None

for mu in mu_values:
    for sigma in sigma_values:
        score = objective_function((mu, sigma))
        if score < best_score:
            best_score = score
            best_params = (mu, sigma)

grid_search_result = {"mu": best_params[0], "sigma": best_params[1], "score": best_score}

# Random Search (for comparison)
random_search_results = []
num_iterations = 100
for _ in range(num_iterations):
    mu = np.random.uniform(0.0001, 0.001)
    sigma = np.random.uniform(0.01, 0.03)
    score = objective_function((mu, sigma))
    random_search_results.append({"mu": mu, "sigma": sigma, "score": score})

random_search_result = min(random_search_results, key=lambda x: x["score"])

grid_search_result, random_search_result

# Plot the results
plt.figure(figsize=(10,6))
for prices in all_prices:
    plt.plot(prices, alpha=0.6)
plt.title(f"Geometric Brownian Motion Simulations of Stock Price ({num_trials} Trials)")
plt.xlabel("Days")
plt.ylabel("Stock Price")
plt.grid(True)
plt.show()