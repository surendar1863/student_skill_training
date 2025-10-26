"""Student class to represent UG and PG students."""

class Student:
    """Represents a student with their academic level and details."""
    
    def __init__(self, name, student_id, level, branch):
        """
        Initialize a student.
        
        Args:
            name (str): Student's name
            student_id (str): Unique student identifier
            level (str): Academic level - 'UG' for Undergraduate or 'PG' for Postgraduate
            branch (str): Branch/Department (e.g., CSE, ECE, ME)
        """
        self.name = name
        self.student_id = student_id
        self.level = level.upper()
        self.branch = branch
        self.test_scores = {}
        
    def __str__(self):
        return f"Student({self.name}, {self.student_id}, {self.level}, {self.branch})"
    
    def add_test_score(self, test_name, score):
        """Add a test score for the student."""
        self.test_scores[test_name] = score
    
    def get_average_score(self):
        """Calculate and return the average score across all tests."""
        if not self.test_scores:
            return 0
        return sum(self.test_scores.values()) / len(self.test_scores)
    
    def is_eligible_for_placement(self, threshold=60):
        """
        Check if student is eligible for placement based on average score.
        
        Args:
            threshold (int): Minimum average score required (default: 60)
            
        Returns:
            bool: True if eligible, False otherwise
        """
        return self.get_average_score() >= threshold
    
    def get_summary(self):
        """Get a summary of student's performance."""
        avg_score = self.get_average_score()
        eligible = self.is_eligible_for_placement()
        
        summary = f"""
Student Summary:
================
Name: {self.name}
Student ID: {self.student_id}
Level: {self.level}
Branch: {self.branch}
Test Scores: {self.test_scores}
Average Score: {avg_score:.2f}
Placement Eligible: {'Yes' if eligible else 'No'}
"""
        return summary
