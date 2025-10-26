"""Skill test classes for different types of assessments."""

import random

class SkillTest:
    """Base class for skill tests."""
    
    def __init__(self, name, max_score=100):
        """
        Initialize a skill test.
        
        Args:
            name (str): Name of the test
            max_score (int): Maximum possible score
        """
        self.name = name
        self.max_score = max_score
        self.questions = []
    
    def add_question(self, question):
        """Add a question to the test."""
        self.questions.append(question)
    
    def get_question_count(self):
        """Return the number of questions in the test."""
        return len(self.questions)


class TechnicalTest(SkillTest):
    """Technical skill test for placement preparation."""
    
    def __init__(self, difficulty='medium'):
        """
        Initialize technical test.
        
        Args:
            difficulty (str): Test difficulty level - 'easy', 'medium', or 'hard'
        """
        super().__init__("Technical Test", max_score=100)
        self.difficulty = difficulty
        self._load_sample_questions()
    
    def _load_sample_questions(self):
        """Load sample technical questions based on difficulty."""
        questions = {
            'easy': [
                "What is the time complexity of binary search?",
                "What is polymorphism in OOP?",
                "What is the difference between stack and queue?",
                "What is a primary key in database?",
                "What is HTTP protocol?"
            ],
            'medium': [
                "Explain the difference between process and thread.",
                "What is virtual memory?",
                "Explain normalization in databases.",
                "What is RESTful API?",
                "Explain MVC architecture."
            ],
            'hard': [
                "Explain CAP theorem in distributed systems.",
                "What is dynamic programming? Give examples.",
                "Explain blockchain technology.",
                "What is machine learning pipeline?",
                "Explain microservices architecture."
            ]
        }
        self.questions = questions.get(self.difficulty, questions['medium'])


class AptitudeTest(SkillTest):
    """Aptitude test for logical and analytical skills."""
    
    def __init__(self):
        super().__init__("Aptitude Test", max_score=100)
        self._load_sample_questions()
    
    def _load_sample_questions(self):
        """Load sample aptitude questions."""
        self.questions = [
            "If 5 men can complete a work in 10 days, how many days will 10 men take?",
            "What is the next number in the series: 2, 4, 8, 16, ?",
            "If A is 25% more than B, then B is what percent less than A?",
            "A train travels 60 km/h. How long will it take to travel 180 km?",
            "The average of 5 numbers is 30. If one number is excluded, average becomes 25. What is the excluded number?"
        ]


class CodingTest(SkillTest):
    """Coding test for programming skills."""
    
    def __init__(self, language='Python'):
        """
        Initialize coding test.
        
        Args:
            language (str): Programming language for the test
        """
        super().__init__("Coding Test", max_score=100)
        self.language = language
        self._load_sample_problems()
    
    def _load_sample_problems(self):
        """Load sample coding problems."""
        self.questions = [
            "Write a function to reverse a string.",
            "Implement a function to find the factorial of a number.",
            "Write a function to check if a number is prime.",
            "Implement bubble sort algorithm.",
            "Write a function to find the Fibonacci series up to n terms."
        ]


class TestEvaluator:
    """Evaluates test performance and generates scores."""
    
    @staticmethod
    def evaluate_test(student, test, answers=None):
        """
        Evaluate a student's test performance.
        
        Args:
            student: Student object
            test: SkillTest object
            answers: List of student answers (optional, for demo generates random score)
            
        Returns:
            int: Score achieved by the student
        """
        # For demonstration, generate a realistic score
        # In a real system, this would evaluate actual answers
        if answers:
            # Actual evaluation logic would go here
            score = len([a for a in answers if a]) * (test.max_score // len(test.questions))
        else:
            # Generate realistic score based on level
            if student.level == 'PG':
                # PG students typically score higher
                score = random.randint(60, 95)
            else:
                # UG students have more variability
                score = random.randint(50, 90)
        
        student.add_test_score(test.name, score)
        return score
