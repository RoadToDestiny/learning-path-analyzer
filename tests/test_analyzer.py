"""Unit tests for LearningPathAnalyzer."""

import pytest
import pandas as pd
import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analyzer import LearningPathAnalyzer
from src.utils import load_lms_logs, validate_lms_data, create_sample_lms_data


@pytest.fixture
def sample_data():
    """Create sample test data."""
    return pd.DataFrame({
        'student_id': ['STU001', 'STU001', 'STU002', 'STU002', 'STU003', 'STU003'],
        'activity_type': ['quiz', 'assignment', 'forum_post', 'quiz', 'video_watch', 'assignment'],
        'timestamp': [
            '2024-01-01', '2024-01-02', '2024-01-03',
            '2024-01-04', '2024-01-05', '2024-01-06'
        ],
        'grade': [85.0, 90.0, 78.0, 88.0, 92.0, 80.0]
    })


@pytest.fixture
def analyzer():
    """Create analyzer instance."""
    return LearningPathAnalyzer()


def test_analyzer_initialization(analyzer):
    """Test analyzer initialization."""
    assert analyzer.df is None
    assert analyzer.activity_stats == {}
    assert analyzer.student_profiles == {}
    assert analyzer.recommendations == {}


def test_load_data(analyzer, sample_data):
    """Test loading data."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        temp_file = f.name
        sample_data.to_csv(temp_file, index=False)
    
    try:
        result = analyzer.load_data(temp_file)
        assert result is not None
        assert len(result) == 6
    finally:
        Path(temp_file).unlink(missing_ok=True)


def test_analyze_activity_patterns(analyzer, sample_data):
    """Test activity pattern analysis."""
    analyzer.df = sample_data.copy()
    analyzer.df['timestamp'] = pd.to_datetime(analyzer.df['timestamp'])
    stats = analyzer.analyze_activity_patterns()

    assert 'quiz' in stats
    assert 'assignment' in stats
    assert stats['quiz']['count'] == 2
    assert 'avg_grade' in stats['quiz']
    assert 'effectiveness' in stats['quiz']


def test_profile_students(analyzer, sample_data):
    """Test student profiling."""
    analyzer.df = sample_data.copy()
    analyzer.df['timestamp'] = pd.to_datetime(analyzer.df['timestamp'])
    profiles = analyzer.profile_students()

    assert 'STU001' in profiles
    assert 'STU002' in profiles
    assert 'STU003' in profiles
    assert profiles['STU001']['total_activities'] == 2
    assert 'engagement_level' in profiles['STU001']


def test_generate_recommendations(analyzer, sample_data):
    """Test recommendation generation."""
    analyzer.df = sample_data.copy()
    analyzer.df['timestamp'] = pd.to_datetime(analyzer.df['timestamp'])
    analyzer.profile_students()
    recommendations = analyzer.generate_recommendations()

    assert 'STU001' in recommendations
    assert len(recommendations['STU001']) > 0
    assert isinstance(recommendations['STU001'], list)


def test_get_summary_report(analyzer, sample_data):
    """Test summary report generation."""
    analyzer.df = sample_data.copy()
    analyzer.df['timestamp'] = pd.to_datetime(analyzer.df['timestamp'])
    analyzer.analyze_activity_patterns()
    report = analyzer.get_summary_report()

    assert 'total_students' in report
    assert 'total_activities' in report
    assert 'average_class_grade' in report
    assert report['total_students'] == 3
    assert report['total_activities'] == 6


def test_validate_lms_data(sample_data):
    """Test data validation."""
    assert validate_lms_data(sample_data) is True


def test_validate_missing_columns():
    """Test validation with missing columns."""
    bad_data = pd.DataFrame({
        'student_id': [1, 2],
        'name': ['Alice', 'Bob']
    })

    with pytest.raises(ValueError):
        validate_lms_data(bad_data)


def test_create_sample_data():
    """Test sample data creation."""
    data = create_sample_lms_data(num_students=5, num_records=20)
    assert len(data) == 20
    assert set(data.columns) == {'student_id', 'activity_type', 'timestamp', 'grade'}


def test_engagement_level(analyzer, sample_data):
    """Test engagement level calculation."""
    analyzer.df = sample_data.copy()
    analyzer.df['timestamp'] = pd.to_datetime(analyzer.df['timestamp'])
    profiles = analyzer.profile_students()

    for student_id, profile in profiles.items():
        assert profile['engagement_level'] in ['high', 'medium', 'low']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
