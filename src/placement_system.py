"""Placement system to manage students and conduct skill tests."""

from student import Student
from skill_test import TechnicalTest, AptitudeTest, CodingTest, TestEvaluator
import json
import os

class PlacementSystem:
    """Manages the entire placement skill testing system."""
    
    def __init__(self):
        """Initialize the placement system."""
        self.students = []
        self.evaluator = TestEvaluator()
        
    def register_student(self, name, student_id, level, branch):
        """
        Register a new student in the system.
        
        Args:
            name (str): Student's name
            student_id (str): Unique student identifier
            level (str): Academic level - 'UG' or 'PG'
            branch (str): Branch/Department
            
        Returns:
            Student: The registered student object
        """
        student = Student(name, student_id, level, branch)
        self.students.append(student)
        return student
    
    def conduct_test(self, student, test):
        """
        Conduct a skill test for a student.
        
        Args:
            student: Student object
            test: SkillTest object
            
        Returns:
            int: Score achieved by the student
        """
        print(f"\nConducting {test.name} for {student.name}...")
        print(f"Number of questions: {test.get_question_count()}")
        print(f"Maximum score: {test.max_score}")
        
        score = self.evaluator.evaluate_test(student, test)
        print(f"Score achieved: {score}/{test.max_score}")
        
        return score
    
    def conduct_all_tests(self, student):
        """
        Conduct all skill tests for a student.
        
        Args:
            student: Student object
            
        Returns:
            dict: Dictionary of test names and scores
        """
        # Create tests based on student level
        if student.level == 'PG':
            technical_test = TechnicalTest(difficulty='hard')
        else:
            technical_test = TechnicalTest(difficulty='medium')
        
        aptitude_test = AptitudeTest()
        coding_test = CodingTest()
        
        # Conduct all tests
        self.conduct_test(student, technical_test)
        self.conduct_test(student, aptitude_test)
        self.conduct_test(student, coding_test)
        
        return student.test_scores
    
    def get_eligible_students(self, threshold=60):
        """
        Get list of students eligible for placement.
        
        Args:
            threshold (int): Minimum average score required
            
        Returns:
            list: List of eligible students
        """
        eligible = []
        for student in self.students:
            if student.is_eligible_for_placement(threshold):
                eligible.append(student)
        return eligible
    
    def generate_report(self):
        """Generate a comprehensive placement report."""
        report = "="*60 + "\n"
        report += "PLACEMENT SKILL TEST REPORT\n"
        report += "="*60 + "\n\n"
        
        ug_students = [s for s in self.students if s.level == 'UG']
        pg_students = [s for s in self.students if s.level == 'PG']
        
        report += f"Total Students: {len(self.students)}\n"
        report += f"UG Students: {len(ug_students)}\n"
        report += f"PG Students: {len(pg_students)}\n\n"
        
        eligible_students = self.get_eligible_students()
        report += f"Eligible for Placement: {len(eligible_students)}\n"
        report += f"Eligibility Rate: {(len(eligible_students)/len(self.students)*100):.1f}%\n\n"
        
        report += "="*60 + "\n"
        report += "INDIVIDUAL STUDENT REPORTS\n"
        report += "="*60 + "\n"
        
        for student in sorted(self.students, key=lambda s: s.get_average_score(), reverse=True):
            report += student.get_summary()
            report += "-"*60 + "\n"
        
        return report
    
    def save_results(self, filename='placement_results.json'):
        """
        Save placement results to a JSON file.
        
        Args:
            filename (str): Name of the file to save results
        """
        results = []
        for student in self.students:
            results.append({
                'name': student.name,
                'student_id': student.student_id,
                'level': student.level,
                'branch': student.branch,
                'test_scores': student.test_scores,
                'average_score': student.get_average_score(),
                'placement_eligible': student.is_eligible_for_placement()
            })
        
        # Create data directory if it doesn't exist
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        filepath = os.path.join(data_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=4)
        
        print(f"\nResults saved to {filepath}")
