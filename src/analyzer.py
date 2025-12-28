"""Learning Path Analyzer - Main analysis engine."""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from datetime import datetime
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


class LearningPathAnalyzer:
    """Analyzes student learning paths based on LMS activity logs."""

    def __init__(self):
        """Initialize the analyzer."""
        self.df = None
        self.activity_stats = {}
        self.student_profiles = {}
        self.recommendations = {}
        
        # Ensure reports directory exists
        Path('reports').mkdir(exist_ok=True)
        
        # Set up matplotlib style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)
        plt.rcParams['font.size'] = 10

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

    def visualize_activity_distribution(self) -> str:
        """Create histogram of activity distribution.

        Returns:
            Path to saved visualization
        """
        if not self.activity_stats:
            self.analyze_activity_patterns()

        activities = list(self.activity_stats.keys())
        counts = [self.activity_stats[a]['count'] for a in activities]

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(activities, counts, color='steelblue', edgecolor='navy', alpha=0.7)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontweight='bold')
        
        ax.set_xlabel('Activity Type', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Activities', fontsize=12, fontweight='bold')
        ax.set_title('Distribution of Learning Activities', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        filepath = 'reports/activity_distribution.png'
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath

    def visualize_average_grades(self) -> str:
        """Create bar chart of average grades by activity type.

        Returns:
            Path to saved visualization
        """
        if not self.activity_stats:
            self.analyze_activity_patterns()

        activities = list(self.activity_stats.keys())
        grades = [self.activity_stats[a]['avg_grade'] for a in activities]

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(activities, grades, color='mediumseagreen', edgecolor='darkgreen', alpha=0.7)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}',
                   ha='center', va='bottom', fontweight='bold')
        
        # Add a horizontal line for class average
        class_avg = self.df['grade'].mean()
        ax.axhline(y=class_avg, color='red', linestyle='--', linewidth=2, 
                   label=f'Class Average: {class_avg:.1f}')
        
        ax.set_xlabel('Activity Type', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Grade', fontsize=12, fontweight='bold')
        ax.set_title('Average Grade by Activity Type', fontsize=14, fontweight='bold')
        ax.set_ylim(0, 100)
        ax.grid(axis='y', alpha=0.3)
        ax.legend(loc='upper right')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        filepath = 'reports/average_grades.png'
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath

    def visualize_engagement_distribution(self) -> str:
        """Create pie chart of student engagement levels.

        Returns:
            Path to saved visualization
        """
        if not self.student_profiles:
            self.profile_students()

        engagement_counts = {'high': 0, 'medium': 0, 'low': 0}
        for profile in self.student_profiles.values():
            level = profile['engagement_level']
            engagement_counts[level] += 1

        levels = list(engagement_counts.keys())
        counts = list(engagement_counts.values())
        colors = {'high': '#2ecc71', 'medium': '#f39c12', 'low': '#e74c3c'}
        color_list = [colors[level] for level in levels]

        fig, ax = plt.subplots(figsize=(10, 8))
        wedges, texts, autotexts = ax.pie(counts, labels=levels, autopct='%1.1f%%',
                                           colors=color_list, startangle=90,
                                           textprops={'fontsize': 12, 'fontweight': 'bold'})
        
        # Enhance the percentage text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(11)
            autotext.set_fontweight('bold')
        
        # Add count labels
        legend_labels = [f'{level.capitalize()}: {counts[i]} students' 
                        for i, level in enumerate(levels)]
        ax.legend(legend_labels, loc='upper left', bbox_to_anchor=(0.85, 1))
        
        ax.set_title('Student Engagement Distribution', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        filepath = 'reports/engagement_distribution.png'
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath

    def generate_all_visualizations(self) -> Dict[str, str]:
        """Generate all visualizations.

        Returns:
            Dictionary with visualization file paths
        """
        visualizations = {
            'activity_distribution': self.visualize_activity_distribution(),
            'average_grades': self.visualize_average_grades(),
            'engagement_distribution': self.visualize_engagement_distribution()
        }
        return visualizations
