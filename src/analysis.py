import pandas as pd


def add_financial_metrics(projects: pd.DataFrame) -> pd.DataFrame:
    data = projects.copy()
    data["cost_overrun_cr"] = data["revised_cost_cr"] - data["planned_cost_cr"]
    data["cost_overrun_pct"] = (
        data["cost_overrun_cr"] / data["planned_cost_cr"] * 100
    ).round(2)
    data["spend_vs_revised_pct"] = (
        data["actual_spend_cr"] / data["revised_cost_cr"] * 100
    ).round(2)
    data["delay_months"] = (
        data["actual_duration_months"] - data["planned_duration_months"]
    )
    data["delay_pct"] = (
        data["delay_months"] / data["planned_duration_months"] * 100
    ).round(2)
    data["risk_score"] = data.apply(_risk_score, axis=1)
    data["risk_level"] = data["risk_score"].apply(_risk_level)
    return data


def _risk_score(row: pd.Series) -> int:
    score = 0

    if row["cost_overrun_pct"] >= 25:
        score += 3
    elif row["cost_overrun_pct"] >= 10:
        score += 2
    elif row["cost_overrun_pct"] > 0:
        score += 1

    if row["delay_pct"] >= 50:
        score += 3
    elif row["delay_pct"] >= 20:
        score += 2
    elif row["delay_pct"] > 0:
        score += 1

    if row["status"].lower() == "ongoing":
        score += 1

    return score


def _risk_level(score: int) -> str:
    if score >= 6:
        return "High"
    if score >= 3:
        return "Medium"
    return "Low"


def sector_summary(projects: pd.DataFrame) -> pd.DataFrame:
    return (
        projects.groupby("sector", as_index=False)
        .agg(
            planned_cost_cr=("planned_cost_cr", "sum"),
            revised_cost_cr=("revised_cost_cr", "sum"),
            actual_spend_cr=("actual_spend_cr", "sum"),
            avg_overrun_pct=("cost_overrun_pct", "mean"),
            project_count=("project_id", "count"),
        )
        .round(2)
        .sort_values("revised_cost_cr", ascending=False)
    )


def top_overruns(projects: pd.DataFrame, limit: int = 5) -> pd.DataFrame:
    return projects.sort_values("cost_overrun_pct", ascending=False).head(limit)

