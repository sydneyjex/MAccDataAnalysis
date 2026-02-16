from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


INPUT_FILE = Path("2024 MAcc Results Sydney.xlsx")
OUTPUT_DIR = Path("outputs")
OUTPUT_CSV = OUTPUT_DIR / "rank_order.csv"
OUTPUT_PNG = OUTPUT_DIR / "rank_order.png"
CORE_PROMPT_PREFIX = "Please place each MAcc CORE course into rank order"


def clean_course_name(column_name: str) -> str:
    """Extract the course name from a Qualtrics export column label."""
    return column_name.split(" - ", 1)[-1].strip()


def find_core_columns(columns: list[str]) -> list[str]:
    """Identify columns that contain the CORE ranking prompt."""
    return [col for col in columns if isinstance(col, str) and col.startswith(CORE_PROMPT_PREFIX)]


def build_rank_table(df: pd.DataFrame, core_columns: list[str]) -> pd.DataFrame:
    """Compute mean ranking and final order for CORE courses."""
    numeric_rankings = df[core_columns].apply(pd.to_numeric, errors="coerce")

    rank_table = (
        pd.DataFrame(
            {
                "Course name": [clean_course_name(col) for col in core_columns],
                "Mean rank": numeric_rankings.mean(axis=0, skipna=True).to_list(),
            }
        )
        .sort_values(by=["Mean rank", "Course name"], ascending=[True, True])
        .reset_index(drop=True)
    )

    rank_table["Final rank position"] = rank_table.index + 1
    rank_table["Mean rank"] = rank_table["Mean rank"].round(3)
    return rank_table


def create_chart(rank_table: pd.DataFrame) -> None:
    """Create a horizontal bar chart of course mean ranks."""
    plt.figure(figsize=(11, 6))
    plt.barh(rank_table["Course name"], rank_table["Mean rank"], color="#2f6f95")
    plt.xlabel("Mean rank (1 = most beneficial, 8 = least beneficial)")
    plt.ylabel("CORE course")
    plt.title("2024 MAcc Exit Survey: CORE Courses Ranked by Mean Student Benefit")
    plt.gca().invert_yaxis()
    plt.grid(axis="x", linestyle="--", alpha=0.35)
    plt.tight_layout()
    plt.savefig(OUTPUT_PNG, dpi=200)
    plt.close()


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Row 2 of the sheet contains the human-readable survey prompts used as headers.
    raw = pd.read_excel(INPUT_FILE, header=1)

    # Row 3 contains ImportId metadata and is removed from analysis.
    responses = raw[~raw.iloc[:, 0].astype(str).str.startswith('{"ImportId"')].copy()

    core_columns = find_core_columns(list(responses.columns))
    if not core_columns:
        raise ValueError("No CORE ranking columns were found in the workbook.")

    rank_table = build_rank_table(responses, core_columns)
    rank_table.to_csv(OUTPUT_CSV, index=False)
    create_chart(rank_table)


if __name__ == "__main__":
    main()
