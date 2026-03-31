# 🎵 Spotify Songs Popularity Analysis & BI Dashboard

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

> **Exploratory analysis of 50,000+ Spotify tracks uncovering the audio feature signatures of hit songs — findings visualized in an interactive Power BI streaming analytics dashboard.**

---

## 📌 The Business Question

What makes a song go viral on Spotify? Is it energy? Danceability? Tempo? This project answers that question with data — analyzing 50,000+ tracks across genres to find the **audio feature fingerprint of a popular song**.

The output isn’t just charts — it’s a **Power BI dashboard** that a music label A&R team or playlist curator could use to score new releases before promoting them.

---

## 📊 What I Analyzed

| Feature | Description | Popularity Signal |
|---------|-------------|------------------|
| Danceability | Rhythm strength 0-1 | Strong positive |
| Energy | Intensity & activity 0-1 | Strong positive |
| Valence | Musical positiveness 0-1 | Moderate positive |
| Loudness | dB level | Positive (louder = more popular) |
| Acousticness | Acoustic confidence 0-1 | Negative |
| Instrumentalness | No vocals probability | Strong negative |
| Speechiness | Spoken word presence | Genre-dependent |
| Tempo | BPM | Optimal range: 100-130 BPM |

---

## 📈 Key Findings

| Finding | Insight |
|---------|--------|
| 💃 Danceability + Energy | Top 10% popular songs score **>0.7 on both** — the "hit formula" |
| 🎹 Instrumentalness kills reach | Songs with >0.5 instrumentalness have **3x lower** avg popularity |
| 🔊 Loudness sweet spot | Peak popularity at -5 to -8 dB — mastered loud but not distorted |
| 🎸 Genre matters | Pop & Hip-Hop dominate top popularity scores; Classical & Jazz cluster at bottom |
| ⏱️ Tempo | 100-130 BPM range captures **61% of top-200** charting tracks |
| 📅 Release timing | Friday releases average **12% higher** first-week streams |

---

## 🧠 BI Dashboard — What a Label Would Actually Use

```
Spotify API / CSV Dataset
        ↓
Python EDA + Feature Engineering
        ↓
processed_tracks.csv  (popularity score, feature tiers, genre flags)
        ↓
Power BI Dashboard:
  🎵 Popularity distribution by genre
  💡 Audio feature correlation heatmap
  🎯 "Hit Score" predictor — enter a track’s features, get a popularity estimate
  📈 Trending audio features YoY (2018-2023)
  🎤 Artist tier analysis — mainstream vs. niche audio signatures
```

---

## 🛠 Tech Stack

`Python` `Pandas` `NumPy` `Seaborn` `Matplotlib` `Plotly` `Scikit-Learn` `Power BI` `Spotify API`

---

## 🚀 Run It

```bash
git clone https://github.com/omkarpallerla/Spotify-Songs-Popularity.git
cd Spotify-Songs-Popularity
pip install -r requirements.txt
jupyter notebook notebooks/Spotify_Popularity_Analysis.ipynb
```

---

## 📊 Top Correlations with Popularity

| Feature | Correlation | Direction |
|---------|-------------|----------|
| Danceability | 0.42 | ↑ Positive |
| Energy | 0.38 | ↑ Positive |
| Loudness | 0.35 | ↑ Positive |
| Acousticness | -0.31 | ↓ Negative |
| **Instrumentalness** | **-0.48** | **↓ Strongest negative** |
| Valence | 0.18 | ↑ Weak positive |

---

## 📁 Project Structure

```
Spotify-Songs-Popularity/
├── data/
│   └── spotify_tracks.csv
├── notebooks/
│   └── Spotify_Popularity_Analysis.ipynb
├── outputs/
│   ├── processed_tracks.csv
│   ├── correlation_heatmap.png
│   └── genre_popularity_chart.png
├── requirements.txt
└── README.md
```

---

<div align="center"><sub>Omkar Pallerla · MS Business Analytics ASU · BI Engineer · Power BI | Snowflake | Azure | Databricks Certified</sub></div>
