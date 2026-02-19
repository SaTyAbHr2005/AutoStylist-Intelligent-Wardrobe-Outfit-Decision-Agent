import numpy as np
from PIL import Image
from sklearn.cluster import KMeans


def extract_dominant_colors(image_path, k=3):
    img = Image.open(image_path).convert("RGBA")
    data = np.array(img)

    # Separate channels
    r, g, b, a = data.T

    # Keep only visible pixels
    pixels = data[a > 0][:, :3]

    # If too few pixels
    if len(pixels) < 50:
        avg = pixels.mean(axis=0)
        return [tuple(map(int, avg))]

    # Filter out low variance pixels (e.g. background/gray/white/black if not transparent)
    # Check if we have enough pixels before filtering
    if len(pixels) > 0:
        filtered_pixels = pixels[(pixels.std(axis=1) > 5)]
        
        # If filtering removed everything, revert to original pixels
        if len(filtered_pixels) > 0:
            pixels = filtered_pixels

    # Check again if we have valid pixels
    if len(pixels) == 0:
         return [(0,0,0)]

    # KMeans clustering
    # Reduce k if we don't have enough unique pixels
    n_clusters = min(k, len(pixels))
    
    kmeans = KMeans(n_clusters=n_clusters, n_init=10)
    kmeans.fit(pixels)

    colors = kmeans.cluster_centers_

    # Sort by frequency
    labels, counts = np.unique(kmeans.labels_, return_counts=True)
    sorted_colors = [colors[i] for i in counts.argsort()[::-1]]

    return [tuple(map(int, c)) for c in sorted_colors]
