"""Main entry point for Learning Path Analyzer."""

import sys
from pathlib import Path
from analyzer import LearningPathAnalyzer
from utils import load_lms_logs, save_report, export_recommendations


def main():
    """Run the learning path analysis."""
    print("Learning Path Analyzer - Educational Analytics Tool")
    print("=" * 50)

    # Initialize analyzer
    analyzer = LearningPathAnalyzer()

    # Use sample data file
    data_file = Path(__file__).parent.parent / 'data' / 'sample_lms_data.csv'

    if not data_file.exists():
        print(f"Creating sample data file at {data_file}...")
        from utils import create_sample_lms_data
        data_file.parent.mkdir(parents=True, exist_ok=True)
        sample_data = create_sample_lms_data(num_students=15, num_records=100)
        sample_data.to_csv(data_file, index=False)
        print(f"Sample data created: {data_file}")

    # Load data
    print(f"\nLoading data from {data_file}...")
    try:
        analyzer.load_data(str(data_file))
        print(f"Loaded {len(analyzer.df)} activity records from {len(analyzer.df['student_id'].unique())} students")
    except Exception as e:
        print(f"Error loading data: {e}")
        return 1

    # Analyze activity patterns
    print("\nAnalyzing activity patterns...")
    activity_stats = analyzer.analyze_activity_patterns()
    print("Activity Statistics:")
    for activity, stats in activity_stats.items():
        print(f"  - {activity}: {stats['count']} activities, avg grade {stats['avg_grade']}")

    # Profile students
    print("\nProfiling students...")
    profiles = analyzer.profile_students()
    print(f"Profiled {len(profiles)} students")

    # Show engagement levels
    engagement_counts = {}
    for profile in profiles.values():
        level = profile['engagement_level']
        engagement_counts[level] = engagement_counts.get(level, 0) + 1

    print("\nEngagement Levels:")
    for level, count in sorted(engagement_counts.items()):
        print(f"  - {level.capitalize()}: {count} students")

    # Generate recommendations
    print("\nGenerating recommendations...")
    recommendations = analyzer.generate_recommendations()
    print(f"Generated recommendations for {len(recommendations)} students")

    # Get summary report
    print("\nGenerating summary report...")
    report = analyzer.get_summary_report()

    print("\n" + "=" * 50)
    print("ANALYSIS SUMMARY")
    print("=" * 50)
    print(f"Total Students: {report['total_students']}")
    print(f"Total Activities: {report['total_activities']}")
    print(f"Average Class Grade: {report['average_class_grade']}")
    print(f"Analysis Date: {report['analysis_date']}")

    # Show top performers
    if report['high_performers']:
        print("\nTop Performers:")
        for student_id, grade in report['high_performers']:
            print(f"  - {student_id}: {grade:.2f}")

    # Show students needing support
    if report['needs_support']:
        print("\nStudents Needing Support:")
        for student_id, grade in report['needs_support']:
            print(f"  - {student_id}: {grade:.2f}")

    # Save reports
    print("\nSaving reports...")
    reports_dir = Path(__file__).parent.parent / 'reports'
    reports_dir.mkdir(parents=True, exist_ok=True)

    report_file = reports_dir / 'analysis_report.json'
    save_report(report, str(report_file))
    print(f"Report saved to {report_file}")

    recs_file = reports_dir / 'recommendations.txt'
    export_recommendations(recommendations, str(recs_file))
    print(f"Recommendations saved to {recs_file}")

    # Generate visualizations
    print("\nGenerating visualizations...")
    try:
        visualizations = analyzer.generate_all_visualizations()
        for viz_name, filepath in visualizations.items():
            print(f"  ✓ {viz_name}: {filepath}")
    except Exception as e:
        print(f"Warning: Could not generate visualizations: {e}")

    print("\nAnalysis complete!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
