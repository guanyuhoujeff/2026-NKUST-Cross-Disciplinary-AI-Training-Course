# -*- coding: utf-8 -*-
"""
生成 Lab4 多模態 AI 用的虛構「宏圖飲料」金融圖表（PNG）。
🚨 金融鐵則：全部虛構、明標 sample / fictional，不寫真實行情。
圖用英文標題（避免 matplotlib 中文豆腐字）；notebook 內問句用中文。

用法：python3 _make_figs.py
產出：fig1_gross_margin.png（毛利率趨勢，主示範）
      fig2_revenue_margin.png（營收+毛利率雙軸，較難的圖）
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
BLUE = "#4C78A8"
ORANGE = "#E45756"

# ---------- fig1：毛利率趨勢長條圖（Q1-Q4：38/36/35/33，下降）----------
quarters = ["Q1", "Q2", "Q3", "Q4"]
gross_margin = [38, 36, 35, 33]

fig, ax = plt.subplots(figsize=(6.4, 4.2))
bars = ax.bar(quarters, gross_margin, color=BLUE, width=0.6)
ax.set_title("Hongtu Beverage 2025 - Gross Margin %  (sample, fictional)",
             fontsize=11)
ax.set_ylabel("Gross Margin (%)")
ax.set_ylim(0, 45)
for b, v in zip(bars, gross_margin):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.6, f"{v}%",
            ha="center", fontsize=10)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig1_gross_margin.png"), dpi=110)
plt.close(fig)
print("已存 fig1_gross_margin.png")

# ---------- fig2：營收(長條,上升) + 毛利率(折線,下降) 雙軸 ----------
revenue = [100, 120, 135, 150]          # 億元，上升
margin2 = [38, 36, 35, 33]              # %，下降

fig, ax1 = plt.subplots(figsize=(6.8, 4.4))
bars = ax1.bar(quarters, revenue, color=BLUE, width=0.55, label="Revenue")
ax1.set_ylabel("Revenue (NT$ 100M)", color=BLUE)
ax1.set_ylim(0, 180)
ax1.tick_params(axis="y", labelcolor=BLUE)
for b, v in zip(bars, revenue):
    ax1.text(b.get_x() + b.get_width() / 2, v + 3, str(v),
             ha="center", fontsize=9, color=BLUE)

ax2 = ax1.twinx()
line = ax2.plot(quarters, margin2, color=ORANGE, marker="o",
                linewidth=2.5, label="Gross Margin %")
ax2.set_ylabel("Gross Margin (%)", color=ORANGE)
ax2.set_ylim(0, 45)
ax2.tick_params(axis="y", labelcolor=ORANGE)
for i, v in enumerate(margin2):
    ax2.text(i, v - 3, f"{v}%", ha="center", fontsize=9, color=ORANGE)

ax1.set_title("Hongtu Beverage 2025 - Revenue vs Gross Margin  (sample, fictional)",
              fontsize=11)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig2_revenue_margin.png"), dpi=110)
plt.close(fig)
print("已存 fig2_revenue_margin.png")
