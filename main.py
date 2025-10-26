"""Main application for Student Skill Training and Placement System."""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from placement_system import PlacementSystem

def main():
    """Main function to run the placement skill testing system."""
    print("="*60)
    print("STUDENT SKILL TRAINING & PLACEMENT SYSTEM")
    print("="*60)
    print()
    
    # Initialize the placement system
    system = PlacementSystem()
    
    # Register UG students
    print("Registering UG (Undergraduate) Students...")
    ug_students = [
        system.register_student("Rahul Kumar", "UG001", "UG", "CSE"),
        system.register_student("Priya Sharma", "UG002", "UG", "ECE"),
        system.register_student("Amit Patel", "UG003", "UG", "CSE"),
        system.register_student("Sneha Singh", "UG004", "UG", "ME"),
        system.register_student("Vivek Reddy", "UG005", "UG", "CSE"),
    ]
    print(f"Registered {len(ug_students)} UG students")
    
    # Register PG students
    print("\nRegistering PG (Postgraduate) Students...")
    pg_students = [
        system.register_student("Dr. Anil Kumar", "PG001", "PG", "CSE"),
        system.register_student("Meera Iyer", "PG002", "PG", "ECE"),
        system.register_student("Karthik Rao", "PG003", "PG", "CSE"),
    ]
    print(f"Registered {len(pg_students)} PG students")
    
    print("\n" + "="*60)
    print("CONDUCTING SKILL TESTS")
    print("="*60)
    
    # Conduct tests for all students
    all_students = ug_students + pg_students
    for student in all_students:
        print("\n" + "-"*60)
        print(f"Student: {student.name} ({student.level})")
        print("-"*60)
        system.conduct_all_tests(student)
    
    print("\n" + "="*60)
    print("GENERATING PLACEMENT REPORT")
    print("="*60)
    
    # Generate and display report
    report = system.generate_report()
    print(report)
    
    # Save results to file
    system.save_results()
    
    print("\n" + "="*60)
    print("PLACEMENT PROCESS COMPLETED")
    print("="*60)

if __name__ == "__main__":
    main()
