# =============================================================
# Spotify Songs Popularity Analysis & BI Dashboard
# Author: Omkar Pallerla | MS Business Analytics, ASU
# =============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

plt.style.use('dark_background')
COLORS = ['#4f9cf9','#06d6a0','#7c3aed','#f59e0b','#ef4444','#ec4899','#14b8a6','#f97316']

# ── 1. GENERATE REALISTIC SPOTIFY DATASET ──────────────────
np.random.seed(42)
n = 5000
genres = ['Pop','Hip-Hop','Rock','Electronic','R&B','Latin','Country','Classical','Jazz','Folk']

df = pd.DataFrame({
    'track_name':        [f'Track_{i}' for i in range(n)],
    'artist':            [f'Artist_{np.random.randint(1,200)}' for _ in range(n)],
    'genre':             np.random.choice(genres, n, p=[0.22,0.18,0.14,0.12,0.10,0.08,0.06,0.04,0.04,0.02]),
    'year':              np.random.choice(range(2018, 2024), n),
    'danceability':      np.random.beta(5, 3, n),
    'energy':            np.random.beta(4, 3, n),
    'loudness':          np.random.normal(-7, 3, n),
    'speechiness':       np.random.beta(1.5, 8, n),
    'acousticness':      np.random.beta(2, 5, n),
    'instrumentalness':  np.random.beta(1, 8, n),
    'liveness':          np.random.beta(2, 7, n),
    'valence':           np.random.beta(3, 3, n),
    'tempo':             np.random.normal(118, 28, n),
    'duration_ms':       np.random.normal(210000, 45000, n),
})

# Popularity formula with realistic noise
df['popularity'] = (
    45
    + 25 * df['danceability']
    + 20 * df['energy']
    + 3  * (df['loudness'] + 10) / 3
    - 30 * df['instrumentalness']
    - 10 * df['acousticness']
    + 8  * df['valence']
    + np.where(df['genre'].isin(['Pop','Hip-Hop']), 8, -3)
    + np.where(df['year'] >= 2022, 5, 0)
    + np.random.normal(0, 8, n)
).clip(0, 100).astype(int)

# ── 2. EXPLORATORY ANALYSIS ──────────────────────────────────
audio_features = ['danceability','energy','valence','loudness','acousticness',
                  'instrumentalness','speechiness','tempo']

corr = df[audio_features + ['popularity']].corr()['popularity'].drop('popularity').sort_values()
print("Correlations with Popularity:\n", corr)

# Genre analysis
genre_stats = df.groupby('genre').agg(
    avg_popularity=('popularity','mean'),
    count=('popularity','count'),
    avg_danceability=('danceability','mean'),
    avg_energy=('energy','mean')
).sort_values('avg_popularity', ascending=False)
print("\nGenre Stats:\n", genre_stats)

# ── 3. ML MODEL ─────────────────────────────────────────────
le = LabelEncoder()
df['genre_enc'] = le.fit_transform(df['genre'])
features = audio_features + ['genre_enc', 'year']
X = df[features]; y = df['popularity']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    'Random Forest':     RandomForestRegressor(n_estimators=200, random_state=42),
    'Gradient Boosting': GradientBoostingRegressor(n_estimators=150, random_state=42),
    'Linear Regression': LinearRegression()
}
for name, model in models.items():
    model.fit(X_train, y_train)
    r2 = r2_score(y_test, model.predict(X_test))
    print(f"{name}: R²={r2:.3f}")

rf = models['Random Forest']
df['predicted_popularity'] = rf.predict(X)
df['hit_score'] = pd.cut(df['predicted_popularity'],
                          bins=[0,40,60,80,100], labels=['Low','Medium','High','Hit'])

df.to_csv('outputs/processed_tracks.csv', index=False)
print("Exported: outputs/processed_tracks.csv")

# ── 4. VISUALIZATIONS ───────────────────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(20, 12))
fig.patch.set_facecolor('#0d1117')

# Correlation heatmap
ax = axes[0, 0]
feat_corr = df[audio_features + ['popularity']].corr()
mask = np.triu(np.ones_like(feat_corr, dtype=bool))
sns.heatmap(feat_corr, mask=mask, cmap='coolwarm', center=0, ax=ax,
            annot=True, fmt='.2f', annot_kws={'size': 7})
ax.set_title('Audio Feature Correlation Matrix', color='white', pad=12)

# Genre popularity
ax = axes[0, 1]
genre_pop = genre_stats['avg_popularity'].sort_values()
colors_g = ['#4f9cf9' if g in ['Pop','Hip-Hop'] else '#7a8499' for g in genre_pop.index]
bars = ax.barh(genre_pop.index, genre_pop.values, color=colors_g)
ax.set_title('Avg Popularity by Genre', color='white', pad=12)
ax.set_xlabel('Average Popularity Score')

# Danceability vs Energy scatter
ax = axes[0, 2]
sc = ax.scatter(df['danceability'], df['energy'], c=df['popularity'],
                cmap='viridis', alpha=0.3, s=8)
plt.colorbar(sc, ax=ax, label='Popularity')
ax.set_xlabel('Danceability'); ax.set_ylabel('Energy')
ax.set_title('Danceability vs Energy vs Popularity', color='white', pad=12)

# Feature importance
ax = axes[1, 0]
feat_imp = pd.Series(rf.feature_importances_, index=features).sort_values(ascending=False)
ax.barh(feat_imp.index[::-1], feat_imp.values[::-1], color='#06d6a0')
ax.set_title('Feature Importance (Random Forest)', color='white', pad=12)

# Year trend
ax = axes[1, 1]
year_trend = df.groupby('year').agg(
    avg_pop=('popularity','mean'),
    avg_dance=('danceability','mean'),
    avg_energy=('energy','mean')
)
ax.plot(year_trend.index, year_trend['avg_pop'], color='#4f9cf9', marker='o', label='Popularity')
ax2 = ax.twinx()
ax2.plot(year_trend.index, year_trend['avg_dance'], color='#06d6a0', linestyle='--', marker='s', label='Danceability')
ax.set_title('Popularity & Danceability Trend by Year', color='white', pad=12)
ax.legend(loc='upper left'); ax2.legend(loc='upper right')

# Hit score distribution
ax = axes[1, 2]
hit_counts = df['hit_score'].value_counts()
colors_h = {'Low':'#ef4444','Medium':'#f59e0b','High':'#4f9cf9','Hit':'#06d6a0'}
ax.pie(hit_counts, labels=hit_counts.index,
       colors=[colors_h[str(h)] for h in hit_counts.index],
       autopct='%1.1f%%', startangle=90)
ax.set_title('Track Hit Score Distribution', color='white', pad=12)

plt.tight_layout()
plt.savefig('outputs/spotify_analysis.png', dpi=150, bbox_inches='tight', facecolor='#0d1117')
print("Saved: outputs/spotify_analysis.png")
plt.show()
