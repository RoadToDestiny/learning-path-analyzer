"""Utility functions for Learning Path Analyzer."""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime


def load_lms_logs(filepath: str) -> pd.DataFrame:
    """Load LMS logs from CSV file.

    Args:
        filepath: Path to CSV file

    Returns:
        Loaded DataFrame

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If CSV format is invalid
    """
    if not Path(filepath).exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    try:
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        raise ValueError(f"Error reading CSV: {str(e)}")


def save_report(report: dict, output_filepath: str) -> None:
    """Save analysis report to JSON file.

    Args:
        report: Report dictionary to save
        output_filepath: Path to save JSON file
    """
    output_path = Path(output_filepath)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2, default=str)


def validate_lms_data(df: pd.DataFrame) -> bool:
    """Validate LMS data structure.

    Args:
        df: DataFrame to validate

    Returns:
        True if valid, raises exception otherwise

    Raises:
        ValueError: If required columns are missing
    """
    required_cols = {'student_id', 'activity_type', 'timestamp', 'grade'}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return True


def create_sample_lms_data(num_students: int = 10, num_records: int = 50) -> pd.DataFrame:
    """Create sample LMS data for testing.

    Args:
        num_students: Number of students
        num_records: Number of activity records

    Returns:
        Sample DataFrame
    """
    import numpy as np
    from datetime import timedelta, datetime as dt

    activity_types = ['quiz', 'assignment', 'forum_post', 'video_watch', 'reading']
    data = []
    start_date = dt(2024, 1, 1)

    for _ in range(num_records):
        record = {
            'student_id': f'STU{np.random.randint(1000, 1000 + num_students)}',
            'activity_type': np.random.choice(activity_types),
            'timestamp': (start_date + timedelta(days=np.random.randint(0, 90))).isoformat(),
            'grade': np.random.uniform(50, 100)
        }
        data.append(record)

    return pd.DataFrame(data)


def export_recommendations(recommendations: dict, output_filepath: str) -> None:
    """Export recommendations to a formatted text file.

    Args:
        recommendations: Dictionary of recommendations by student
        output_filepath: Path to save recommendations file
    """
    output_path = Path(output_filepath)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        f.write("Learning Path Recommendations Report\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")

        for student_id, recs in recommendations.items():
            f.write(f"Student ID: {student_id}\n")
            for i, rec in enumerate(recs, 1):
                f.write(f"  {i}. {rec}\n")
            f.write("\n")
