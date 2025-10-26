"""Unit tests for the PlacementSystem class."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
import json
from placement_system import PlacementSystem

class TestPlacementSystem(unittest.TestCase):
    """Test cases for PlacementSystem class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.system = PlacementSystem()
    
    def test_system_initialization(self):
        """Test placement system initialization."""
        self.assertEqual(len(self.system.students), 0)
        self.assertIsNotNone(self.system.evaluator)
    
    def test_register_student(self):
        """Test student registration."""
        student = self.system.register_student("Test Student", "TEST001", "UG", "CSE")
        
        self.assertEqual(len(self.system.students), 1)
        self.assertEqual(student.name, "Test Student")
        self.assertEqual(student.student_id, "TEST001")
        self.assertEqual(student.level, "UG")
    
    def test_register_multiple_students(self):
        """Test registering multiple students."""
        self.system.register_student("Student 1", "S001", "UG", "CSE")
        self.system.register_student("Student 2", "S002", "PG", "ECE")
        
        self.assertEqual(len(self.system.students), 2)
    
    def test_conduct_test(self):
        """Test conducting a single test."""
        from skill_test import TechnicalTest
        
        student = self.system.register_student("Test Student", "TEST001", "UG", "CSE")
        test = TechnicalTest()
        
        score = self.system.conduct_test(student, test)
        
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
        self.assertIn("Technical Test", student.test_scores)
    
    def test_conduct_all_tests(self):
        """Test conducting all tests for a student."""
        student = self.system.register_student("Test Student", "TEST001", "UG", "CSE")
        
        scores = self.system.conduct_all_tests(student)
        
        self.assertEqual(len(scores), 3)
        self.assertIn("Technical Test", scores)
        self.assertIn("Aptitude Test", scores)
        self.assertIn("Coding Test", scores)
    
    def test_conduct_all_tests_pg_student(self):
        """Test that PG students get harder technical tests."""
        pg_student = self.system.register_student("PG Student", "PG001", "PG", "CSE")
        
        scores = self.system.conduct_all_tests(pg_student)
        
        # Verify all tests were conducted
        self.assertEqual(len(scores), 3)
    
    def test_get_eligible_students(self):
        """Test getting eligible students."""
        # Register students and add scores
        student1 = self.system.register_student("Student 1", "S001", "UG", "CSE")
        student1.add_test_score("Test1", 80)
        student1.add_test_score("Test2", 85)
        
        student2 = self.system.register_student("Student 2", "S002", "UG", "ECE")
        student2.add_test_score("Test1", 50)
        student2.add_test_score("Test2", 45)
        
        eligible = self.system.get_eligible_students(60)
        
        self.assertEqual(len(eligible), 1)
        self.assertEqual(eligible[0].student_id, "S001")
    
    def test_generate_report(self):
        """Test report generation."""
        student = self.system.register_student("Test Student", "TEST001", "UG", "CSE")
        student.add_test_score("Test1", 75)
        
        report = self.system.generate_report()
        
        self.assertIn("PLACEMENT SKILL TEST REPORT", report)
        self.assertIn("Test Student", report)
        self.assertIn("Total Students: 1", report)
    
    def test_save_results(self):
        """Test saving results to JSON file."""
        student = self.system.register_student("Test Student", "TEST001", "UG", "CSE")
        student.add_test_score("Test1", 85)
        
        test_filename = 'test_results.json'
        self.system.save_results(test_filename)
        
        # Check if file was created
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        filepath = os.path.join(data_dir, test_filename)
        
        self.assertTrue(os.path.exists(filepath))
        
        # Verify content
        with open(filepath, 'r') as f:
            results = json.load(f)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], "Test Student")
        self.assertEqual(results[0]['student_id'], "TEST001")
        
        # Cleanup
        os.remove(filepath)

if __name__ == '__main__':
    unittest.main()
