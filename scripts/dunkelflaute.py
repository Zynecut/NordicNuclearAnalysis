
'''
Description:
This script allows the user to select regions, technologies, and aggregation periods (e.g., 1–14 days)
to identify the three lowest average renewable production periods for each interval. Results are saved
to an Excel file named accordingly.
'''

import pandas as pd

# === INPUT ===
file_path = r"C:\Users\einar\NTNU\MSc. - Kjernekraft og PowerGAMA - General\TET4900\Data\timeseries_profiles_stock.csv"
region = ["DK1", "DK2", "SE4", "DE", "NL", "PL"]
tech = ["windoff", "windon", "solar"]
aggregation_days_list = list(range(1, 15))  # eller f.eks. [3, 4, 5]

df = pd.read_csv(file_path)
df["time"] = pd.to_datetime(df["time"], utc=True)
df.set_index("time", inplace=True)

def extract_columns(df, regions, techs):
    return [
        col for col in df.columns
        if any(col.startswith(t + "_") and col.split("_")[-1] in regions for t in techs)
    ]

selected_cols = extract_columns(df, region, tech)
df_filtered = df[selected_cols].copy()

results = []
for days in aggregation_days_list:
    rule = f"{days}D"
    df_agg = df_filtered.resample(rule).mean()
    df_mean = df_agg.mean(axis=1).sort_values().head(3)  # Tre laveste perioder

    for timestamp, value in df_mean.items():
        results.append({
            "aggregation_days": days,
            "start_date": timestamp,
            "mean_value": value
        })

result_df = pd.DataFrame(results)
result_df["start_date"] = result_df["start_date"].dt.tz_localize(None)

region_label = "_".join(region)
tech_label = "_".join(tech)
filename = f"low_inflow_periods_{region_label}_{tech_label}.xlsx"
result_df.to_excel(filename, index=False)

print(f"✅ Lagret til: {filename}")

# %% Identify dry, wet, normal years in large dataset

import pandas as pd

# === INPUT ============================================================================================================
file_path = r"C:\Users\einar\NTNU\MSc. - Kjernekraft og PowerGAMA - General\TET4900\Data\timeseries_profiles_stock.csv"
inflow_selection = "all"  # inflow_selection = "all"
# === END OF INPUT =====================================================================================================

df = pd.read_csv(file_path)
df["time"] = pd.to_datetime(df["time"], utc=True)
df.set_index("time", inplace=True)
def extract_inflow_columns(df, inflow_zones="all", zone_col="zone"):
    if inflow_zones == "all":
        inflow_cols = [col for col in df.columns if col.startswith("inflow_")]
    else:
        inflow_cols = [f"inflow_{zone}" for zone in inflow_zones if f"inflow_{zone}" in df.columns]
    return inflow_cols + [zone_col] if zone_col in df.columns else inflow_cols
selected_cols = extract_inflow_columns(df, inflow_selection)
df_selected = df[selected_cols]

df_selected = df[selected_cols].copy()
df_selected["year"] = df_selected.index.year
summary = df_selected.groupby("year").agg(["sum", "mean"])

# Fjerner multiindeks (kolonne-nivåer) for klarhet
summary.columns = ['_'.join(col).strip() for col in summary.columns]
summary.reset_index(inplace=True)

inflow_sum_cols = [col for col in summary.columns if col.endswith("_sum")]
inflow_mean_cols = [col for col in summary.columns if col.endswith("_mean")]

summary["total_inflow_sum"] = summary[inflow_sum_cols].sum(axis=1)
summary["total_inflow_mean"] = summary[inflow_mean_cols].mean(axis=1)

total_summary = summary[["year", "total_inflow_sum", "total_inflow_mean"]].copy()
total_summary.sort_values(by="total_inflow_sum", ascending=False, inplace=True)

total_summary.reset_index(drop=True, inplace=True)

highest_year = total_summary.iloc[0]
lowest_year = total_summary.iloc[-1]
middle_year = total_summary.iloc[len(total_summary) // 2]

representative_years = pd.DataFrame([highest_year, middle_year, lowest_year])










