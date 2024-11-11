from flask import Blueprint, render_template, request, redirect, url_for, flash

from student_service import StudentService

student_router = Blueprint('student', __name__)
student_service = StudentService()


@student_router.route("/")
@student_router.route("/students")
def students():
    page = request.args.get('page', 1, type=int)  # Get current page from query string (defaults to 1)
    result = student_service.get_all_students_paging(page=page, per_page=5)

    if result["status"] == "Success":
        students_list = result["data"]
        total_pages = result["total_pages"]
        current_page = result["current_page"]
        return render_template('students.html', students_list=students_list, total_pages=total_pages,
                               current_page=current_page, header="Flask Application with CRUD Operations")
    else:
        flash(result["message"], 'Error')
        return render_template('students.html', students_list=[], total_pages=0,
                               current_page=0, header="Flask Application with CRUD Operations")


@student_router.route("/add_student", methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        full_name = request.form['full_name']
        address = request.form['address']
        city = request.form['city']
        zip_code = request.form['zip_code']

        response = student_service.add_student(full_name, address, city, zip_code)
        flash(response["message"], response["status"])
        return redirect(url_for('student.students'))

    return render_template("add_student.html", header="Flask Application with CRUD Operations")


@student_router.route("/delete_student/<int:roll_number>")
def delete_student(roll_number):
    response = student_service.delete_student(roll_number)
    flash(response["message"], response["status"])
    return redirect(url_for('student.students'))


@student_router.route("/edit_student/<int:roll_number>")
def edit_student(roll_number):
    response = student_service.get_student_by_id(roll_number)
    if response["status"] == "Error":
        flash(response["message"], response["status"])
        return redirect(url_for('student.students'))

    return render_template("edit_student.html", header="Flask Application with CRUD Operations",
                           student=response["data"])


@student_router.route("/update_student", methods=['POST'])
def update_student():
    if request.method == 'POST':
        roll_number = request.form['roll_number']
        full_name = request.form['full_name']
        address = request.form['address']
        city = request.form['city']
        zip_code = request.form['zip_code']

        response = student_service.update_student(roll_number, full_name, address, city, zip_code)
        flash(response["message"], response["status"])
        return redirect(url_for('student.students'))
