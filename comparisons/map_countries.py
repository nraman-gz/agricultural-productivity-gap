import geopandas as gpd
import matplotlib.pyplot as plt
from employment_data import merged_data

# Get country codes
iso_codes = merged_data['ISO'].unique()

# Load shapefile
world = gpd.read_file("ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp")
world['highlight'] = world['ADM0_A3'].isin(iso_codes)
world = world[world['ADM0_A3'] != 'ATA'] 

# Plot
plt.rcParams['font.family'] = 'Palatino'
fig, ax = plt.subplots(figsize=(8, 4))
world.plot(ax=ax, color='lightgray', edgecolor='black', linewidth=0.4)
world[world['highlight']].plot(ax=ax, color='skyblue', edgecolor='black', linewidth=0.4)

# Add title and remove axes
# ax.set_title('Highlighted Countries by ISO Code', fontsize=16)
ax.axis('off')

# Save the map
plt.savefig("figures/highlighted_world_map.png")
plt.show()
