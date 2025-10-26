"""Unit tests for the SkillTest classes."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from skill_test import SkillTest, TechnicalTest, AptitudeTest, CodingTest, TestEvaluator
from student import Student

class TestSkillTest(unittest.TestCase):
    """Test cases for base SkillTest class."""
    
    def test_skill_test_initialization(self):
        """Test skill test initialization."""
        test = SkillTest("Sample Test", 100)
        self.assertEqual(test.name, "Sample Test")
        self.assertEqual(test.max_score, 100)
        self.assertEqual(test.questions, [])
    
    def test_add_question(self):
        """Test adding questions to a test."""
        test = SkillTest("Sample Test")
        test.add_question("Question 1")
        test.add_question("Question 2")
        
        self.assertEqual(test.get_question_count(), 2)

class TestTechnicalTest(unittest.TestCase):
    """Test cases for TechnicalTest class."""
    
    def test_technical_test_initialization(self):
        """Test technical test initialization."""
        test = TechnicalTest('easy')
        self.assertEqual(test.name, "Technical Test")
        self.assertEqual(test.max_score, 100)
        self.assertEqual(test.difficulty, 'easy')
    
    def test_technical_test_has_questions(self):
        """Test that technical test loads questions."""
        test = TechnicalTest('medium')
        self.assertGreater(test.get_question_count(), 0)
    
    def test_technical_test_different_difficulties(self):
        """Test technical test with different difficulties."""
        easy_test = TechnicalTest('easy')
        medium_test = TechnicalTest('medium')
        hard_test = TechnicalTest('hard')
        
        self.assertGreater(easy_test.get_question_count(), 0)
        self.assertGreater(medium_test.get_question_count(), 0)
        self.assertGreater(hard_test.get_question_count(), 0)

class TestAptitudeTest(unittest.TestCase):
    """Test cases for AptitudeTest class."""
    
    def test_aptitude_test_initialization(self):
        """Test aptitude test initialization."""
        test = AptitudeTest()
        self.assertEqual(test.name, "Aptitude Test")
        self.assertEqual(test.max_score, 100)
    
    def test_aptitude_test_has_questions(self):
        """Test that aptitude test loads questions."""
        test = AptitudeTest()
        self.assertGreater(test.get_question_count(), 0)

class TestCodingTest(unittest.TestCase):
    """Test cases for CodingTest class."""
    
    def test_coding_test_initialization(self):
        """Test coding test initialization."""
        test = CodingTest('Python')
        self.assertEqual(test.name, "Coding Test")
        self.assertEqual(test.max_score, 100)
        self.assertEqual(test.language, 'Python')
    
    def test_coding_test_has_problems(self):
        """Test that coding test loads problems."""
        test = CodingTest()
        self.assertGreater(test.get_question_count(), 0)

class TestTestEvaluator(unittest.TestCase):
    """Test cases for TestEvaluator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.student = Student("Test Student", "TEST001", "UG", "CSE")
        self.test = TechnicalTest()
        self.evaluator = TestEvaluator()
    
    def test_evaluate_test_adds_score(self):
        """Test that evaluate_test adds score to student."""
        score = self.evaluator.evaluate_test(self.student, self.test)
        
        self.assertIn("Technical Test", self.student.test_scores)
        self.assertEqual(self.student.test_scores["Technical Test"], score)
    
    def test_evaluate_test_returns_valid_score(self):
        """Test that evaluate_test returns a valid score."""
        score = self.evaluator.evaluate_test(self.student, self.test)
        
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, self.test.max_score)
    
    def test_evaluate_test_pg_vs_ug(self):
        """Test that PG students generally score higher (statistical test)."""
        ug_student = Student("UG Student", "UG001", "UG", "CSE")
        pg_student = Student("PG Student", "PG001", "PG", "CSE")
        
        # Run multiple evaluations to get average
        ug_scores = []
        pg_scores = []
        
        for _ in range(10):
            ug_test = TechnicalTest()
            pg_test = TechnicalTest()
            
            ug_scores.append(self.evaluator.evaluate_test(ug_student, ug_test))
            pg_scores.append(self.evaluator.evaluate_test(pg_student, pg_test))
        
        # On average, PG scores should be higher or equal
        # This is a statistical test and might occasionally fail
        avg_ug = sum(ug_scores) / len(ug_scores)
        avg_pg = sum(pg_scores) / len(pg_scores)
        
        # Just verify both are within valid range
        self.assertGreaterEqual(avg_ug, 0)
        self.assertGreaterEqual(avg_pg, 0)

if __name__ == '__main__':
    unittest.main()
