"""Learning Path Analyzer - Main analysis engine."""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from datetime import datetime
from typing import Dict, List, Tuple


class LearningPathAnalyzer:
    """Analyzes student learning paths based on LMS activity logs."""

    def __init__(self):
        """Initialize the analyzer."""
        self.df = None
        self.activity_stats = {}
        self.student_profiles = {}
        self.recommendations = {}

    def load_data(self, filepath: str) -> pd.DataFrame:
        """Load LMS logs from CSV file.

        Args:
            filepath: Path to CSV file with LMS logs

        Returns:
            Loaded DataFrame
        """
        self.df = pd.read_csv(filepath)
        self._validate_data()
        return self.df

    def _validate_data(self) -> None:
        """Validate data structure."""
        required_cols = {'student_id', 'activity_type', 'timestamp', 'grade'}
        if not required_cols.issubset(set(self.df.columns)):
            raise ValueError(f"Missing required columns: {required_cols}")
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])

    def analyze_activity_patterns(self) -> Dict:
        """Analyze activity patterns across all students.

        Returns:
            Dictionary with activity statistics
        """
        if self.df is None:
            raise ValueError("No data loaded. Call load_data() first.")

        activity_stats = {}

        for activity_type in self.df['activity_type'].unique():
            activity_data = self.df[self.df['activity_type'] == activity_type]
            avg_grade = activity_data['grade'].mean()
            count = len(activity_data)
            correlation = activity_data['grade'].corr(activity_data['grade']) * 100

            activity_stats[activity_type] = {
                'count': count,
                'avg_grade': round(avg_grade, 2),
                'effectiveness': round(correlation, 2)
            }

        self.activity_stats = activity_stats
        return activity_stats

    def profile_students(self) -> Dict:
        """Create student learning profiles.

        Returns:
            Dictionary with student profiles
        """
        if self.df is None:
            raise ValueError("No data loaded. Call load_data() first.")

        profiles = {}

        for student_id in self.df['student_id'].unique():
            student_data = self.df[self.df['student_id'] == student_id]
            total_activities = len(student_data)
            avg_grade = student_data['grade'].mean()
            activity_diversity = len(student_data['activity_type'].unique())
            days_active = len(student_data['timestamp'].dt.date.unique())

            # Determine learning style
            activity_pref = student_data['activity_type'].value_counts().index[0]

            profiles[student_id] = {
                'total_activities': total_activities,
                'average_grade': round(avg_grade, 2),
                'activity_diversity': activity_diversity,
                'days_active': days_active,
                'preferred_activity': activity_pref,
                'engagement_level': self._calculate_engagement(student_data)
            }

        self.student_profiles = profiles
        return profiles

    def _calculate_engagement(self, student_data: pd.DataFrame) -> str:
        """Calculate engagement level based on activity data.

        Args:
            student_data: DataFrame with student's activities

        Returns:
            Engagement level: 'high', 'medium', or 'low'
        """
        total_activities = len(student_data)
        avg_grade = student_data['grade'].mean()

        if total_activities > 15 and avg_grade > 70:
            return 'high'
        elif total_activities > 5 or avg_grade > 60:
            return 'medium'
        else:
            return 'low'

    def generate_recommendations(self) -> Dict:
        """Generate recommendations for each student.

        Returns:
            Dictionary with recommendations
        """
        if not self.student_profiles:
            self.profile_students()

        recommendations = {}

        for student_id, profile in self.student_profiles.items():
            recs = []

            if profile['engagement_level'] == 'low':
                recs.append("Increase participation in learning activities")
                recs.append("Set a schedule for regular study sessions")
            elif profile['engagement_level'] == 'medium':
                recs.append("Explore diverse activity types to enhance learning")
                recs.append("Aim to increase consistency in participation")
            else:
                recs.append("Maintain current level of engagement")
                recs.append("Consider peer mentoring to help others")

            if profile['average_grade'] < 60:
                recs.append("Focus on high-effectiveness activities")
                recs.append("Seek help from instructors or tutoring services")

            if profile['activity_diversity'] < 3:
                recs.append(f"Try different activities beyond {profile['preferred_activity']}")

            recommendations[student_id] = recs

        self.recommendations = recommendations
        return recommendations

    def get_summary_report(self) -> Dict:
        """Generate a summary report of the analysis.

        Returns:
            Dictionary containing analysis summary
        """
        if self.df is None:
            raise ValueError("No data loaded. Call load_data() first.")

        total_students = len(self.df['student_id'].unique())
        total_activities = len(self.df)
        avg_class_grade = self.df['grade'].mean()

        return {
            'total_students': total_students,
            'total_activities': total_activities,
            'average_class_grade': round(avg_class_grade, 2),
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'activity_stats': self.activity_stats,
            'high_performers': self._get_top_performers(5),
            'needs_support': self._get_struggling_students(5)
        }

    def _get_top_performers(self, n: int = 5) -> List:
        """Get top performing students.

        Args:
            n: Number of students to return

        Returns:
            List of top performers with their scores
        """
        if not self.student_profiles:
            return []

        sorted_students = sorted(
            self.student_profiles.items(),
            key=lambda x: x[1]['average_grade'],
            reverse=True
        )[:n]
        return [(sid, p['average_grade']) for sid, p in sorted_students]

    def _get_struggling_students(self, n: int = 5) -> List:
        """Get students who need support.

        Args:
            n: Number of students to return

        Returns:
            List of struggling students with their scores
        """
        if not self.student_profiles:
            return []

        sorted_students = sorted(
            self.student_profiles.items(),
            key=lambda x: x[1]['average_grade']
        )[:n]
        return [(sid, p['average_grade']) for sid, p in sorted_students]
