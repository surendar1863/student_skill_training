"""Unit tests for the Student class."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from student import Student

class TestStudent(unittest.TestCase):
    """Test cases for Student class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ug_student = Student("Test Student", "TEST001", "UG", "CSE")
        self.pg_student = Student("Test PG Student", "TEST002", "PG", "ECE")
    
    def test_student_initialization(self):
        """Test student object initialization."""
        self.assertEqual(self.ug_student.name, "Test Student")
        self.assertEqual(self.ug_student.student_id, "TEST001")
        self.assertEqual(self.ug_student.level, "UG")
        self.assertEqual(self.ug_student.branch, "CSE")
        self.assertEqual(self.ug_student.test_scores, {})
    
    def test_level_uppercase_conversion(self):
        """Test that level is converted to uppercase."""
        student = Student("Test", "T001", "ug", "CSE")
        self.assertEqual(student.level, "UG")
        
        student2 = Student("Test2", "T002", "pg", "ECE")
        self.assertEqual(student2.level, "PG")
    
    def test_add_test_score(self):
        """Test adding test scores."""
        self.ug_student.add_test_score("Technical Test", 85)
        self.assertEqual(self.ug_student.test_scores["Technical Test"], 85)
        
        self.ug_student.add_test_score("Aptitude Test", 90)
        self.assertEqual(len(self.ug_student.test_scores), 2)
    
    def test_get_average_score_no_tests(self):
        """Test average score calculation with no tests."""
        avg = self.ug_student.get_average_score()
        self.assertEqual(avg, 0)
    
    def test_get_average_score_with_tests(self):
        """Test average score calculation with tests."""
        self.ug_student.add_test_score("Technical Test", 80)
        self.ug_student.add_test_score("Aptitude Test", 90)
        self.ug_student.add_test_score("Coding Test", 85)
        
        avg = self.ug_student.get_average_score()
        self.assertEqual(avg, 85.0)
    
    def test_is_eligible_for_placement_default_threshold(self):
        """Test placement eligibility with default threshold."""
        self.ug_student.add_test_score("Test1", 70)
        self.ug_student.add_test_score("Test2", 80)
        
        self.assertTrue(self.ug_student.is_eligible_for_placement())
    
    def test_is_not_eligible_for_placement(self):
        """Test placement ineligibility."""
        self.ug_student.add_test_score("Test1", 50)
        self.ug_student.add_test_score("Test2", 55)
        
        self.assertFalse(self.ug_student.is_eligible_for_placement())
    
    def test_is_eligible_custom_threshold(self):
        """Test placement eligibility with custom threshold."""
        self.ug_student.add_test_score("Test1", 75)
        
        self.assertTrue(self.ug_student.is_eligible_for_placement(70))
        self.assertFalse(self.ug_student.is_eligible_for_placement(80))
    
    def test_get_summary(self):
        """Test student summary generation."""
        self.ug_student.add_test_score("Technical Test", 85)
        summary = self.ug_student.get_summary()
        
        self.assertIn("Test Student", summary)
        self.assertIn("TEST001", summary)
        self.assertIn("UG", summary)
        self.assertIn("CSE", summary)
        self.assertIn("85.00", summary)
    
    def test_str_representation(self):
        """Test string representation of student."""
        str_repr = str(self.ug_student)
        self.assertIn("Test Student", str_repr)
        self.assertIn("TEST001", str_repr)
        self.assertIn("UG", str_repr)
        self.assertIn("CSE", str_repr)

if __name__ == '__main__':
    unittest.main()
