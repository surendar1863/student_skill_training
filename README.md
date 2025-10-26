# Student Skill Training System

A comprehensive skill testing system for UG (Undergraduate) and PG (Postgraduate) students for placement preparation.

## Features

- **Student Management**: Register and manage UG and PG students
- **Multiple Test Types**:
  - Technical Test (with difficulty levels)
  - Aptitude Test (logical and analytical skills)
  - Coding Test (programming skills)
- **Automated Evaluation**: Automatic scoring and evaluation system
- **Placement Eligibility**: Determine placement eligibility based on performance
- **Comprehensive Reports**: Generate detailed placement reports
- **Data Export**: Save results to JSON format

## Installation

This project requires Python 3.6 or higher. No external dependencies are needed.

```bash
# Clone the repository
git clone https://github.com/surendar1863/student_skill_training.git
cd student_skill_training

# No pip install needed - uses only Python standard library
```

## Usage

### Running the Application

```bash
python main.py
```

This will:
1. Register sample UG and PG students
2. Conduct all skill tests (Technical, Aptitude, Coding)
3. Generate a comprehensive placement report
4. Save results to `data/placement_results.json`

### Running Tests

```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_student
python -m unittest tests.test_skill_test
python -m unittest tests.test_placement_system
```

## Project Structure

```
student_skill_training/
├── main.py                 # Main application entry point
├── src/
│   ├── student.py         # Student class implementation
│   ├── skill_test.py      # Skill test classes and evaluator
│   └── placement_system.py # Placement management system
├── tests/
│   ├── test_student.py    # Student class tests
│   ├── test_skill_test.py # Skill test classes tests
│   └── test_placement_system.py # Placement system tests
├── data/                   # Output directory for results
├── requirements.txt        # Project dependencies
└── README.md              # This file
```

## Classes

### Student
- Represents UG or PG students
- Tracks test scores and calculates averages
- Determines placement eligibility

### SkillTest (Base Class)
- Base class for all skill tests
- Manages questions and scoring

### TechnicalTest
- Technical knowledge assessment
- Difficulty levels: easy, medium, hard
- PG students get harder tests

### AptitudeTest
- Logical and analytical skills assessment
- Quantitative aptitude questions

### CodingTest
- Programming skills assessment
- Language-specific problems

### PlacementSystem
- Manages the entire placement process
- Registers students
- Conducts tests
- Generates reports

## Sample Output

The system generates:
- Console output showing test progress
- Detailed placement report with individual student summaries
- JSON file with exportable results

## License

MIT License
