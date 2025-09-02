#!/usr/bin/env python3

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create Base (parent class for all ORM models)
Base = declarative_base()

# ------------------------
# Models (child classes)
# ------------------------

class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)

    # Relationship: one department has many students
    students = relationship("Student", back_populates="department")

    def __repr__(self):
        return f"<Department id={self.id} name='{self.name}'>"


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)
    department_id = Column(Integer(), ForeignKey('departments.id'))

    # Relationship: each student belongs to one department
    department = relationship("Department", back_populates="students")

    def __repr__(self):
        return f"<Student id={self.id} name='{self.name}' department_id={self.department_id}>"


# ------------------------
# Script entrypoint
# ------------------------
if __name__ == "__main__":
    # Create engine (SQLite database)
    engine = create_engine("sqlite:///university.db")

    # Create tables
    Base.metadata.create_all(engine)

    # Create a session (for CRUD operations)
    Session = sessionmaker(bind=engine)
    session = Session()

    # --- Insert sample data ---
    cs = Department(name="Computer Science")
    math = Department(name="Mathematics")

    session.add_all([cs, math])
    session.commit()

    alice = Student(name="Alice", department=cs)
    bob = Student(name="Bob", department=math)
    charlie = Student(name="Charlie", department=cs)

    session.add_all([alice, bob, charlie])
    session.commit()

    # --- Query data ---
    print("\nAll Departments:")
    for dept in session.query(Department).all():
        print(dept)

    print("\nAll Students:")
    for student in session.query(Student).all():
        print(student)

    print("\nStudents in Computer Science:")
    for student in cs.students:
        print(student)

    # Close session
    session.close()
