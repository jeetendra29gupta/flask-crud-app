from sqlalchemy.exc import SQLAlchemyError

from database import Session
from models import Student


class StudentService:
    def __init__(self):
        # We could initialize other configurations here if needed
        pass

    @staticmethod
    def _get_db_session():
        """Private method to handle session management using context manager."""
        return Session()

    def add_student(self, full_name, address, city, zip_code):
        """Add a new student to the database."""
        if not full_name or not address or not city or not zip_code:
            return {"status": "Error", "message": "All fields are required"}

        try:
            with self._get_db_session() as db:
                new_student = Student(
                    full_name=full_name,
                    address=address,
                    city=city,
                    zip_code=zip_code
                )
                print(new_student)
                db.add(new_student)
                db.commit()
                return {"status": "Success", "message": "Record successfully added to database"}
        except SQLAlchemyError as e:
            return {"status": "Error", "message": f"Failed to add record: {str(e)}"}

    def get_all_students_paging(self, page=1, per_page=10):
        """Fetch 10 students from the database."""
        try:
            with self._get_db_session() as db:
                students = db.query(Student).limit(per_page).offset((page - 1) * per_page).all()
                total_students = db.query(Student).count()
                total_pages = (total_students // per_page) + (1 if total_students % per_page > 0 else 0)
                return {"status": "Success", "data": students, "total_pages": total_pages, "current_page": page}
        except SQLAlchemyError as e:
            return {"status": "Error", "message": f"Failed to fetch records: {str(e)}"}

    def get_all_students(self):
        """Fetch all students from the database."""
        try:
            with self._get_db_session() as db:
                students = db.query(Student).all()
                return {"status": "Success", "data": students}
        except SQLAlchemyError as e:
            return {"status": "Error", "message": f"Failed to fetch records: {str(e)}"}

    def delete_student(self, roll_number):
        """Delete a student by roll_number."""
        try:
            with self._get_db_session() as db:
                student = db.query(Student).get(roll_number)
                if student:
                    db.delete(student)
                    db.commit()
                    return {"status": "Success", "message": "Record successfully deleted from the database"}
                else:
                    return {"status": "Error", "message": f"Student with roll number {roll_number} not found"}
        except SQLAlchemyError as e:
            return {"status": "Error", "message": f"Failed to delete record: {str(e)}"}

    def get_student_by_id(self, roll_number):
        """Fetch a single student by roll_number."""
        try:
            with self._get_db_session() as db:
                student = db.query(Student).get(roll_number)
                if student:
                    return {"status": "Success", "data": student}
                else:
                    return {"status": "Error", "message": f"Student with roll number {roll_number} not found"}
        except SQLAlchemyError as e:
            return {"status": "Error", "message": f"Error fetching student: {str(e)}"}

    def update_student(self, roll_number, full_name, address, city, zip_code):
        """Update an existing student."""
        if not roll_number or not full_name or not address or not city or not zip_code:
            return {"status": "Error", "message": "All fields are required"}
        try:
            with self._get_db_session() as db:
                student = db.query(Student).get(roll_number)
                if student:
                    student.full_name = full_name
                    student.address = address
                    student.city = city
                    student.zip_code = zip_code
                    db.commit()
                    return {"status": "Success", "message": "Record successfully updated in the database"}
                else:
                    return {"status": "Error", "message": f"Student with roll number {roll_number} not found"}
        except SQLAlchemyError as e:
            return {"status": "Error", "message": f"Failed to update record: {str(e)}"}
