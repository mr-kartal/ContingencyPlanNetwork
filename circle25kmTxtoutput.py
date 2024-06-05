import pandas as pd
from geopy.distance import geodesic
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import geopandas as gpd

# Koordinatları okuma
file_path = 'coordinate-numbers.txt'  # Koordinatların bulunduğu dosya

# Her satırın iki değerden oluştuğundan emin olarak okuyalım
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

coordinates = []
for line in lines:
    parts = line.strip().split(',')
    if len(parts) == 2:
        try:
            lat = float(parts[0])
            lon = float(parts[1])
            coordinates.append((lat, lon))
        except ValueError:
            print(f"Geçersiz koordinat satırı atlandı: {line}")

# Koordinatları DataFrame'e dönüştürme
coords = pd.DataFrame(coordinates, columns=["latitude", "longitude"])

# Daireler oluşturma fonksiyonu
def create_circles(coords, radius):
    selected_points = []  # Seçilen noktalar
    remaining_points = coords.copy()  # Kapsanmayan noktalar

    while len(remaining_points) > 0:
        # Rastgele bir nokta seç
        index = random.randint(0, len(remaining_points) - 1)
        center_point = remaining_points.iloc[index]
        selected_points.append(center_point)

        # Merkez noktasına göre daire oluştur
        daire = Circle((center_point['longitude'], center_point['latitude']), radius / 111, edgecolor='r', facecolor='none', lw=2)

        # Daireyi çizdir
        ax.add_patch(daire)
        plt.scatter(center_point['longitude'], center_point['latitude'], color='blue')

        # Daireyi kapsayan diğer noktaları seç
        covered_points_index = []
        for idx, point in remaining_points.iterrows():
            if geodesic((center_point['latitude'], center_point['longitude']), (point['latitude'], point['longitude'])).kilometers <= radius:
                covered_points_index.append(idx)

        # Seçilen noktaları listeden çıkar
        remaining_points = remaining_points.drop(covered_points_index)

    return selected_points

# Dairelerin oluşturulması
fig, ax = plt.subplots(figsize=(10, 10))
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world.boundary.plot(ax=ax)

selected_circles = create_circles(coords, 25)

plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('25 km Yarıçapında Daireler ile Tüm Alanın Taranması')
plt.show()

# Seçilen nokta sayısını yazdırma
print("Seçilen nokta sayısı:", len(selected_circles))

# Seçilen noktaları dosyaya yazma
output_file_path = 'selected-coordinate-numbers.txt'
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for point in selected_circles:
        output_file.write(f"{point['latitude']}, {point['longitude']}\n")

print(f"Seçilen noktalar {output_file_path} dosyasına yazıldı.")