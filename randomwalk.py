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

# Plot the results
plt.figure(figsize=(10,6))
for prices in all_prices:
    plt.plot(prices, alpha=0.6)
plt.title(f"Geometric Brownian Motion Simulations of Stock Price ({num_trials} Trials)")
plt.xlabel("Days")
plt.ylabel("Stock Price")
plt.grid(True)
plt.show()

# # Simulate random walks
# all_prices = simulate_random_walk(num_periods, initial_price, volatility, num_trials)

# # Plot the results
# plt.figure(figsize=(10,6))
# for prices in all_prices:
#     plt.plot(prices, alpha=0.6)
# plt.title(f"Random Walk Simulations of Stock Price ({num_trials} Trials)")
# plt.xlabel("Days")
# plt.ylabel("Stock Price")
# plt.grid(True)
# plt.show()
