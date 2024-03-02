from flask import Flask, render_template, request, redirect, url_for
from .models import db, Employee

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db.init_app(app)


@app.route('/')
def home():
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)


@app.route('/<int:id>')
def show_employee(id):
    employee = Employee.query.get_or_404(id)
    return render_template('show.html', employee=employee)


@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        salary = request.form['salary']
        new_employee = Employee(name=name, email=email, department=department, salary=salary)
        db.session.add(new_employee)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('add.html')


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_employee(id):
    employee = Employee.query.get_or_404(id)

    if request.method == 'POST':
        employee.name = request.form['name']
        employee.email = request.form['email']
        employee.department = request.form['department']
        employee.salary = request.form['salary']
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('update.html', employee=employee)


@app.route('/delete/<int:id>')
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
