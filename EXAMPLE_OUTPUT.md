# Example Output from Learning Path Analyzer

## Command Line Output

When you run `python src/main.py`, you'll see output similar to this:

```bash
$ python src/main.py
Learning Path Analyzer - Educational Analytics Tool
==================================================

Loading data from data/sample_lms_data.csv...
Loaded 100 activity records from 15 students

Analyzing activity patterns...
Activity Statistics:
  - quiz: 20 activities, avg grade 84.25
  - assignment: 20 activities, avg grade 80.0
  - forum_post: 20 activities, avg grade 81.0
  - video_watch: 20 activities, avg grade 93.0
  - reading: 20 activities, avg grade 82.5

Profiling students...
Profiled 15 students

Engagement Levels:
  - high: 5 students
  - medium: 7 students
  - low: 3 students

==================================================
ANALYSIS SUMMARY
==================================================
Total Students: 15
Total Activities: 100
Average Class Grade: 84.15
Analysis Date: 2025-12-28 18:03:45

Top Performers:
  - STU007: 97.00
  - STU003: 92.33
  - STU010: 90.00
  - STU001: 88.75
  - STU005: 86.40

Students Needing Support:
  - STU006: 57.50
  - STU002: 71.67
  - STU004: 67.50
  - STU009: 65.00
  - STU014: 63.33

Saving reports...
Report saved to reports/analysis_report.json
Recommendations saved to reports/recommendations.txt

Generating visualizations...
  ✓ activity_distribution: reports/activity_distribution.png
  ✓ average_grades: reports/average_grades.png
  ✓ engagement_distribution: reports/engagement_distribution.png

Analysis complete!
```

## Generated Files

After running the analysis, you'll find these files in the `reports/` directory:

### 1. **analysis_report.json** (JSON Data)

```json
{
  "total_students": 15,
  "total_activities": 100,
  "average_class_grade": 84.15,
  "analysis_date": "2025-12-28 18:03:45",
  "activity_stats": {
    "quiz": {
      "count": 20,
      "avg_grade": 84.25,
      "effectiveness": 100.0
    },
    "assignment": {
      "count": 20,
      "avg_grade": 80.0,
      "effectiveness": 100.0
    },
    "video_watch": {
      "count": 20,
      "avg_grade": 93.0,
      "effectiveness": 100.0
    },
    "forum_post": {
      "count": 20,
      "avg_grade": 81.0,
      "effectiveness": 100.0
    },
    "reading": {
      "count": 20,
      "avg_grade": 82.5,
      "effectiveness": 100.0
    }
  },
  "high_performers": [
    ["STU007", 97.0],
    ["STU003", 92.33],
    ["STU010", 90.0],
    ["STU001", 88.75],
    ["STU005", 86.4]
  ],
  "needs_support": [
    ["STU006", 57.5],
    ["STU002", 71.67],
    ["STU004", 67.5],
    ["STU009", 65.0],
    ["STU014", 63.33]
  ]
}
```

### 2. **recommendations.txt** (Text Recommendations)

```
=== LEARNING PATH RECOMMENDATIONS ===

STU001:
- Maintain current level of engagement
- Consider peer mentoring to help others

STU002:
- Increase participation in learning activities
- Set a schedule for regular study sessions
- Focus on high-effectiveness activities
- Seek help from instructors or tutoring services

STU003:
- Maintain current level of engagement
- Consider peer mentoring to help others

STU004:
- Increase participation in learning activities
- Set a schedule for regular study sessions
- Focus on high-effectiveness activities
- Seek help from instructors or tutoring services

STU005:
- Explore diverse activity types to enhance learning
- Aim to increase consistency in participation

STU006:
- Increase participation in learning activities
- Set a schedule for regular study sessions
- Focus on high-effectiveness activities
- Seek help from instructors or tutoring services
- Try different activities beyond quiz

STU007:
- Maintain current level of engagement
- Consider peer mentoring to help others

STU009:
- Increase participation in learning activities
- Set a schedule for regular study sessions
- Focus on high-effectiveness activities
- Seek help from instructors or tutoring services

STU010:
- Maintain current level of engagement
- Consider peer mentoring to help others

STU014:
- Increase participation in learning activities
- Set a schedule for regular study sessions
- Focus on high-effectiveness activities
- Seek help from instructors or tutoring services
```

### 3. **activity_distribution.png** (Histogram)

This visualization shows the distribution of activities by type:

```
┌─────────────────────────────────────────┐
│  Activity Distribution Histogram         │
│                                         │
│  20  ┌────┐                            │
│  19  │    │                            │
│  18  │    │                            │
│  17  │    │                            │
│  16  │    │                            │
│  15  │    │  ┌────┐  ┌────┐  ┌────┐   │
│  14  │    │  │    │  │    │  │    │   │
│  13  │    │  │    │  │    │  │    │   │
│  12  │    │  │    │  │    │  │    │   │
│   0  └────┘──┴────┴──┴────┴──┴────┴   │
│      quiz  assignment  forum  video    │
│                       reading         │
└─────────────────────────────────────────┘

Key Statistics:
- Quiz: 20 activities (20% of total)
- Assignment: 20 activities (20% of total)
- Forum Post: 20 activities (20% of total)
- Video Watch: 20 activities (20% of total)
- Reading: 20 activities (20% of total)
```

**Color**: Steel Blue with value labels on top of each bar
**Resolution**: 300 DPI
**Format**: PNG

### 4. **average_grades.png** (Bar Chart)

This visualization shows the average grade by activity type:

```
┌─────────────────────────────────────────┐
│  Average Grade by Activity Type         │
│                                         │
│ 100  ┌─────────────────────────────     │
│  95  │          ┌────────────────┐      │
│  90  │          │   93.0 (Video) │      │
│  85  │ ┌────┐   │                │      │
│  84  │ │84.3│   │                │      │
│  82  │ │(Q) │   │                │      │
│  81  │ │    │   │   ┌────┐   ┌──┤      │
│  80  │ │    │   │   │81.0│   │82│      │
│   0  │ └────┘───┴───┴────┴───┴──┤      │
│     └─────────────────────────────────  │
│      Class Average: 84.15 (red line)    │
│                                         │
│      Quiz: 84.25  │  Assignment: 80.0  │
│      Video: 93.0  │  Forum: 81.0       │
│      Reading: 82.5                     │
└─────────────────────────────────────────┘
```

**Color**: Medium Sea Green with class average line
**Resolution**: 300 DPI
**Format**: PNG

### 5. **engagement_distribution.png** (Pie Chart)

This visualization shows student engagement distribution:

```
┌─────────────────────────────────────────┐
│  Student Engagement Distribution        │
│                                         │
│           ╔═══════════╗                 │
│         ╱             ╲                 │
│       ╱       HIGH       ╲  33.3%       │
│      │   (5 students)    │              │
│      │     [Green]       │              │
│       ╲                ╱                 │
│        ╚═╗           ╱╝                 │
│          │  MEDIUM  │   46.7%           │
│          │ (7 stud) │   [Orange]        │
│          │          │                   │
│           ╲       ╱                      │
│            ╚════╝                       │
│           ╱     ╲                       │
│          │  LOW   │  20.0%              │
│          │(3 std) │  [Red]              │
│           ╲     ╱                       │
│            ╚════╝                       │
│                                         │
│  Legend:                                │
│  🟢 High: 5 students (33.3%)            │
│  🟡 Medium: 7 students (46.7%)          │
│  🔴 Low: 3 students (20.0%)             │
└─────────────────────────────────────────┘
```

**Colors**:
- 🟢 High: Green (#2ecc71)
- 🟡 Medium: Orange (#f39c12)
- 🔴 Low: Red (#e74c3c)

**Resolution**: 300 DPI
**Format**: PNG

## Running Analysis Programmatically

```python
from src.analyzer import LearningPathAnalyzer
from src.utils import save_report, export_recommendations

# Initialize analyzer
analyzer = LearningPathAnalyzer()

# Load data
analyzer.load_data('data/lms_logs.csv')

# Run analysis
activity_stats = analyzer.analyze_activity_patterns()
student_profiles = analyzer.profile_students()
recommendations = analyzer.generate_recommendations()
report = analyzer.get_summary_report()

# Save reports
save_report(report, 'reports/analysis_report.json')
export_recommendations(recommendations, 'reports/recommendations.txt')

# Generate visualizations
visualizations = analyzer.generate_all_visualizations()
print(f"Generated visualizations:")
for name, path in visualizations.items():
    print(f"  - {name}: {path}")

# Output:
# Generated visualizations:
#   - activity_distribution: reports/activity_distribution.png
#   - average_grades: reports/average_grades.png
#   - engagement_distribution: reports/engagement_distribution.png
```

## Sample Student Profile

```json
{
  "STU001": {
    "total_activities": 7,
    "average_grade": 88.75,
    "activity_diversity": 5,
    "days_active": 7,
    "preferred_activity": "quiz",
    "engagement_level": "high"
  }
}
```

This indicates:
- **Total Activities**: 7 learning activities
- **Average Grade**: 88.75 out of 100
- **Activity Diversity**: Uses 5 different types of activities
- **Days Active**: Participated on 7 different days
- **Preferred Activity**: Prefers quizzes
- **Engagement Level**: High engagement

---

## Key Metrics Explained

### Engagement Levels

- **High**: total_activities > 15 AND avg_grade > 70
- **Medium**: total_activities > 5 OR avg_grade > 60
- **Low**: Everything else

### Activity Effectiveness

Measured by correlation of activity grade with overall grade.
Higher values indicate more effective activity types.

### Average Grade

Calculated as mean of all grades for that activity type.
Used to identify which activities correlate with better performance.

---

For more information, see [README.md](README.md)
