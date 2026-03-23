import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings("ignore")

# ── Load data ─────────────────────────────────────────────────
df = pd.read_csv("netflix_titles.csv")
print(f"✅ Dataset loaded: {len(df)} titles")
print(f"   Movies: {(df.type=='Movie').sum()}")
print(f"   TV Shows: {(df.type=='TV Show').sum()}")
print(f"   Years: {df.year_added.min()} – {df.year_added.max()}")
print(f"   Countries: {df.country.nunique()}")
print()

# ── Color palette ─────────────────────────────────────────────
RED    = "#E50914"   # Netflix red
DARK   = "#141414"   # Netflix black
GREY   = "#564D4D"
WHITE  = "#FFFFFF"
LGREY  = "#B3B3B3"
GOLD   = "#F5C518"

plt.rcParams.update({
    "figure.facecolor": DARK,
    "axes.facecolor":   DARK,
    "axes.edgecolor":   GREY,
    "axes.labelcolor":  WHITE,
    "xtick.color":      LGREY,
    "ytick.color":      LGREY,
    "text.color":       WHITE,
    "grid.color":       GREY,
    "grid.alpha":       0.3,
    "font.family":      "sans-serif",
    "font.size":        10,
})

fig = plt.figure(figsize=(20, 14), facecolor=DARK)
fig.suptitle("🎬  Netflix Content Analysis Dashboard",
             fontsize=22, fontweight="bold", color=RED, y=0.98)

# ── 1. Content added per year ─────────────────────────────────
ax1 = fig.add_subplot(3, 3, 1)
by_year = df.groupby(["year_added","type"]).size().unstack(fill_value=0)
years = by_year.index
x = range(len(years))
w = 0.4
ax1.bar([i-w/2 for i in x], by_year.get("Movie",   pd.Series(0,index=years)),
        width=w, color=RED,   label="Movie",   alpha=0.9)
ax1.bar([i+w/2 for i in x], by_year.get("TV Show", pd.Series(0,index=years)),
        width=w, color=GOLD,  label="TV Show", alpha=0.9)
ax1.set_xticks(list(x))
ax1.set_xticklabels([str(y) for y in years], rotation=45, fontsize=8)
ax1.set_title("Content Added Per Year", color=WHITE, fontweight="bold", pad=10)
ax1.set_ylabel("Number of Titles")
ax1.legend(framealpha=0)
ax1.grid(axis="y")

# ── 2. Movies vs TV Shows donut ───────────────────────────────
ax2 = fig.add_subplot(3, 3, 2)
split = df.groupby("type").size()
colors_donut = [RED, GOLD]
wedges, texts, autotexts = ax2.pie(
    split, labels=split.index, autopct="%1.1f%%",
    colors=colors_donut, startangle=90,
    wedgeprops={"width":0.55, "edgecolor": DARK, "linewidth":2},
    textprops={"color": WHITE})
for at in autotexts:
    at.set_fontsize(11); at.set_fontweight("bold")
ax2.set_title("Movies vs TV Shows", color=WHITE, fontweight="bold", pad=10)

# ── 3. Top 10 genres ─────────────────────────────────────────
ax3 = fig.add_subplot(3, 3, 3)
genre_rows = []
for _, row in df.iterrows():
    for g in str(row["listed_in"]).split(","):
        genre_rows.append(g.strip())
genre_series = pd.Series(genre_rows).value_counts().head(10)
bars = ax3.barh(genre_series.index[::-1], genre_series.values[::-1],
                color=RED, alpha=0.85)
for bar, val in zip(bars, genre_series.values[::-1]):
    ax3.text(bar.get_width()+20, bar.get_y()+bar.get_height()/2,
             str(val), va="center", color=LGREY, fontsize=8)
ax3.set_title("Top 10 Genres", color=WHITE, fontweight="bold", pad=10)
ax3.set_xlabel("Number of Titles")
ax3.grid(axis="x")

# ── 4. Top 10 countries ───────────────────────────────────────
ax4 = fig.add_subplot(3, 3, 4)
top_c = df.groupby("country").size().sort_values(ascending=False).head(10)
bar_colors = [RED if c=="United States" else GREY for c in top_c.index]
bars4 = ax4.bar(range(len(top_c)), top_c.values, color=bar_colors, alpha=0.9)
ax4.set_xticks(range(len(top_c)))
ax4.set_xticklabels([c[:10] for c in top_c.index], rotation=45, fontsize=8, ha="right")
ax4.set_title("Top 10 Countries", color=WHITE, fontweight="bold", pad=10)
ax4.set_ylabel("Number of Titles")
for bar in bars4:
    ax4.text(bar.get_x()+bar.get_width()/2, bar.get_height()+10,
             str(bar.get_height()), ha="center", color=LGREY, fontsize=8)
ax4.grid(axis="y")

# ── 5. Monthly content additions ─────────────────────────────
ax5 = fig.add_subplot(3, 3, 5)
monthly = df.groupby("month_added").size()
month_names = ["Jan","Feb","Mar","Apr","May","Jun",
               "Jul","Aug","Sep","Oct","Nov","Dec"]
ax5.plot(range(1,13), [monthly.get(m,0) for m in range(1,13)],
         color=RED, linewidth=2.5, marker="o", markersize=7,
         markerfacecolor=WHITE, markeredgecolor=RED, markeredgewidth=2)
ax5.fill_between(range(1,13), [monthly.get(m,0) for m in range(1,13)],
                 alpha=0.15, color=RED)
ax5.set_xticks(range(1,13))
ax5.set_xticklabels(month_names, fontsize=9)
ax5.set_title("Content Added by Month", color=WHITE, fontweight="bold", pad=10)
ax5.set_ylabel("Titles Added")
ax5.grid(axis="y")

# ── 6. Ratings breakdown ─────────────────────────────────────
ax6 = fig.add_subplot(3, 3, 6)
top_ratings = df.groupby("rating").size().sort_values(ascending=False).head(8)
colors_r = [RED, GOLD, "#FF6B6B","#FFD700","#FF4444","#FFC125","#CC0000","#B8860B"]
ax6.bar(top_ratings.index, top_ratings.values,
        color=colors_r[:len(top_ratings)], alpha=0.9, edgecolor=DARK)
ax6.set_title("Content Ratings Breakdown", color=WHITE, fontweight="bold", pad=10)
ax6.set_ylabel("Number of Titles")
ax6.set_xlabel("Rating")
for i, (idx, val) in enumerate(top_ratings.items()):
    ax6.text(i, val+20, str(val), ha="center", color=LGREY, fontsize=8)
ax6.grid(axis="y")

# ── 7. Cumulative content growth ─────────────────────────────
ax7 = fig.add_subplot(3, 3, 7)
cum = df.groupby(["year_added","type"]).size().unstack(fill_value=0).cumsum()
ax7.fill_between(cum.index, cum.get("Movie",0),   color=RED,  alpha=0.6, label="Movies")
ax7.fill_between(cum.index, cum.get("TV Show",0), color=GOLD, alpha=0.6, label="TV Shows")
ax7.set_title("Cumulative Content Growth", color=WHITE, fontweight="bold", pad=10)
ax7.set_ylabel("Total Titles")
ax7.set_xlabel("Year")
ax7.legend(framealpha=0)
ax7.grid(axis="y")

# ── 8. Movies duration distribution ──────────────────────────
ax8 = fig.add_subplot(3, 3, 8)
movie_dur = df[df.type=="Movie"]["duration"].str.extract(r"(\d+)").astype(float).dropna()
ax8.hist(movie_dur, bins=30, color=RED, alpha=0.85, edgecolor=DARK)
ax8.axvline(movie_dur.mean().iloc[0], color=GOLD, linestyle="--",
            linewidth=2, label=f"Avg: {movie_dur.mean().iloc[0]:.0f} min")
ax8.set_title("Movie Duration Distribution", color=WHITE, fontweight="bold", pad=10)
ax8.set_xlabel("Duration (minutes)")
ax8.set_ylabel("Number of Movies")
ax8.legend(framealpha=0)
ax8.grid(axis="y")

# ── 9. KPI summary box ───────────────────────────────────────
ax9 = fig.add_subplot(3, 3, 9)
ax9.axis("off")
total        = len(df)
movies       = (df.type=="Movie").sum()
tv_shows     = (df.type=="TV Show").sum()
countries    = df.country.nunique()
top_genre    = pd.Series(genre_rows).value_counts().index[0]
top_country  = df.country.value_counts().index[0]
avg_dur_val  = movie_dur.mean().iloc[0]

kpis = [
    ("Total Titles",      f"{total:,}",         RED),
    ("Movies",            f"{movies:,}",         RED),
    ("TV Shows",          f"{tv_shows:,}",       GOLD),
    ("Countries",         f"{countries}",        LGREY),
    ("Top Genre",         top_genre,             LGREY),
    ("Top Country",       top_country,           LGREY),
    ("Avg Movie Length",  f"{avg_dur_val:.0f} min", LGREY),
]

ax9.set_xlim(0,1); ax9.set_ylim(0,1)
ax9.text(0.5, 0.97, "📊 Key Stats", ha="center", va="top",
         fontsize=13, fontweight="bold", color=WHITE)
for i, (label, value, color) in enumerate(kpis):
    y = 0.85 - i*0.115
    ax9.text(0.05, y,   label+":", color=LGREY,  fontsize=9,  va="center")
    ax9.text(0.95, y,   value,     color=color,  fontsize=10,
             fontweight="bold", ha="right", va="center")
    ax9.axhline(y-0.055, color=GREY, linewidth=0.5, alpha=0.5)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("netflix_dashboard.png", dpi=150,
            bbox_inches="tight", facecolor=DARK)
print("✅ Dashboard saved as netflix_dashboard.png!")
plt.close()

# ── Print key insights ────────────────────────────────────────
print()
print("=" * 50)
print("📊 KEY INSIGHTS FROM NETFLIX DATA")
print("=" * 50)
print(f"1. Total content:    {total:,} titles")
print(f"2. Movies vs TV:     {movies/total*100:.0f}% Movies | {tv_shows/total*100:.0f}% TV Shows")
print(f"3. Top genre:        {top_genre}")
print(f"4. Top country:      {top_country}")
print(f"5. Avg movie length: {avg_dur_val:.0f} minutes")
peak_year = df.groupby("year_added").size().idxmax()
print(f"6. Peak growth year: {peak_year}")
print("=" * 50)
