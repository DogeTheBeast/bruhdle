import pandas as pd
import matplotlib.pyplot as plt

# Read the .txt file
file_path = 'trials_count.txt'  # Replace with your actual file path
data = pd.read_csv(file_path, header=None, names=[
                   'Date', 'Amount of tries'], sep=',')

# Convert the Date column to datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Set the Date column as the index
data.set_index('Date', inplace=True)

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data['Amount of tries'], marker='o')
plt.title('Date vs Amount of tries to guess the correct word')
plt.xlabel('Date')
plt.ylabel('Amount of tries')
plt.ylim(0, 7)
# plt.grid(True)

# Export the plot to a PNG file
output_file_path = './assets/daily.png'
plt.savefig(output_file_path)
