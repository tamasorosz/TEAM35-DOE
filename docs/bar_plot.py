import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'Ubuntu'  # You can change 'Arial' to your desired font
# Data from the three vectors
data = {
    'Case I': [8.84, 15.88, 26.91, 23.45, 6.57, 18.14, 22.69, 8.95, 12.48, 28.67],
    'Case II': [13.68, 15.48, 27.21, 13.20, 14.34, 18.14, 10.13, 18.63, 21.54, 20.71],
    'Case III': [25.48, 15.55, 12.52, 23.31, 5.55, 14.67, 12.38, 17.81, 22.18, 17.18]
}

# Prepare data for plotting
indices = np.arange(len(data['Case I']))  # Turn positions (0, 1, 2, ..., 9)
width = 0.25  # Width of the bars

# Create the plot
plt.figure(figsize=(12, 6))

# Define specific colors for each case
colors = [ 'darkcyan', 'darkgray','navy']

# Create horizontal bars for each case with specified colors
plt.barh(indices - width, data['Case I'], width, label='Case I', color=colors[0])
plt.barh(indices, data['Case II'], width, label='Case II', color=colors[1])
plt.barh(indices + width, data['Case III'], width, label='Case III', color=colors[2])

# Customize the plot
#plt.title('Comparison of Values Across Cases I, II, and III')
plt.xlabel('radii [mm]', fontsize=12)
#plt.ylabel('Turn Number', fontsize=12)
plt.yticks(indices, labels=[f'Turn {i + 1}' for i in indices])  # Rename y-axis ticks
plt.legend(loc='right', fontsize=14)
plt.grid(axis='x')

# Save the plot to a file
plt.savefig("horizontal_bar_plot_custom_colors.png")
