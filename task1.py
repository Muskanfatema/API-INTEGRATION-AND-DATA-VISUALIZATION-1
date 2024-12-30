#d1gxs1ogryWisE69lG9qux8Xx4PdNpebNhInxYGx
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from wordcloud import WordCloud
from PIL import Image
from io import BytesIO

# Replace with your actual NASA API key
API_KEY = 'd1gxs1ogryWisE69lG9qux8Xx4PdNpebNhInxYGx'

# NASA APOD (Astronomy Picture of the Day) API endpoint
URL = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}"

# Fetch data from the API
response = requests.get(URL)
if response.status_code != 200:
    print("Failed to fetch data. Check your API key or endpoint.")
    exit()

# Parse the JSON data
data = response.json()

# Extract necessary information
date = data.get('date', 'Unknown Date')
title = data.get('title', 'Unknown Title')
explanation = data.get('explanation', 'No Explanation Available')
image_url = data.get('url', '')

# Display fetched information
print(f"Date: {date}")
print(f"Title: {title}")
print(f"Explanation: {explanation[:200]}...")  # Limit displayed explanation
print(f"Image URL: {image_url}")

# Data for visualizations
data_points = {
    "Title Length": len(title),
    "Explanation Length": len(explanation),
    "Date Length": len(date)
}

# ---- INTERACTIVE VISUALIZATIONS ----

# 1. Interactive Bar Chart with Plotly
bar_fig = px.bar(
    x=list(data_points.keys()),
    y=list(data_points.values()),
    color=list(data_points.keys()),
    labels={"x": "Categories", "y": "Character Count"},
    title=f"Data Overview ({date})",
    color_discrete_sequence=px.colors.sequential.Viridis
)
bar_fig.update_layout(title_font_size=18, title_font_color="#2c3e50", font_family="Arial")

# Show Plotly Bar Chart
bar_fig.show()

# ---- STATIC VISUALIZATIONS ----

# Create a dashboard with Matplotlib
fig = plt.figure(figsize=(15, 12))
grid = fig.add_gridspec(2, 2, hspace=0.6, wspace=0.4)

# Custom color palette for the bar plot
palette = sns.color_palette("coolwarm", len(data_points))

# 2. Bar Plot (Static) for Comparison
ax1 = fig.add_subplot(grid[0, 0])
sns.barplot(x=list(data_points.keys()), y=list(data_points.values()), palette=palette, ax=ax1)
ax1.set_title(f"Data Overview ({date})", fontsize=16, fontweight="bold", color="#34495e")
ax1.set_xlabel("Categories", fontsize=12, fontweight="bold")
ax1.set_ylabel("Character Count", fontsize=12, fontweight="bold")
ax1.grid(axis="y", linestyle="--", alpha=0.7)

# 3. WordCloud Visualization: Explanation Text
ax2 = fig.add_subplot(grid[0, 1])
wordcloud = WordCloud(width=800, height=400, background_color='black', colormap="viridis").generate(explanation)
ax2.imshow(wordcloud, interpolation='bilinear')
ax2.axis('off')
ax2.set_title("WordCloud of Explanation", fontsize=16, fontweight="bold", color="#34495e")

# 4. APOD Image (if available)
ax3 = fig.add_subplot(grid[1, :])
if image_url.endswith(('jpg', 'png')):
    img_response = requests.get(image_url)
    if img_response.status_code == 200:
        img = Image.open(BytesIO(img_response.content))
        ax3.imshow(img)
        ax3.axis('off')
        ax3.set_title(f"NASA APOD Image: {title}", fontsize=16, fontweight="bold", color="#34495e")
    else:
        ax3.text(0.5, 0.5, "Failed to load the image.", ha='center', va='center', fontsize=14)
else:
    ax3.text(0.5, 0.5, "No valid image available.", ha='center', va='center', fontsize=14)

# Add a title for the whole dashboard
fig.suptitle("NASA APOD Visualization Dashboard", fontsize=20, fontweight="bold", color="#2c3e50")
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()

# 5. Interactive Word Cloud with Plotly (Alternative)
wordcloud_data = [{"word": word, "count": freq} for word, freq in WordCloud().process_text(explanation).items()]
wc_fig = px.treemap(
    wordcloud_data,
    path=["word"],
    values="count",
    title="Interactive Word Cloud of Explanation",
    color="count",
    color_continuous_scale="Viridis"
)
wc_fig.update_layout(title_font_size=18, title_font_color="#2c3e50", font_family="Arial")
wc_fig.show()