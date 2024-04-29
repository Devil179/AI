import csv
import matplotlib.pyplot as plt
from datetime import datetime

department_files = {} # Dictionary to store CSV files for different departments

def authenticate(): # Define functions for the payroll system
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        username = input("Enter username: ")
        password = input("Enter password: ")
        
        if username == "admin" and password == "password":
            return True
        else:
            print(f"Invalid credentials! Attempts remaining: {max_attempts - attempt}")
    
    print("Authentication failed. Exiting.")
    return False

def select_department():
    print("Select Department:")
    print("1. IT Department")
    print("2. HR Department")
    department_choice = input("Enter the department number: ")
    
    if department_choice == "1":
        return "IT"
    elif department_choice == "2":
        return "HR"
    else:
        print("Invalid department choice. Defaulting to IT Department.")
        return "IT"

def initialize_csv(department):
    csv_file = f'payroll_{department.lower()}.csv'
    department_files[department] = csv_file

    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["First Name", "Last Name", "Position", "Base Salary", "Increment", "Deductions", "Bonus", "Classification", "Start Date", "Hours Worked", "Performance Reviews"])

def read_csv(department):
    csv_file = department_files.get(department)
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data

def write_csv(department, data):
    csv_file = department_files.get(department)
    with open(csv_file, mode='w', newline='') as file:
        fieldnames = ["First Name", "Last Name", "Position", "Base Salary", "Increment", "Deductions", "Bonus", "Classification", "Start Date", "Hours Worked", "Performance Reviews"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def add_employee(department, first_name, last_name, position, base_salary, increment_percentage, deductions=0, bonus=0, classification="Full-Time"):
    increment = (base_salary * increment_percentage) / 100
    start_date = datetime.now().strftime("%Y-%m-%d")
    
    data = read_csv(department)
    data.append({
        "First Name": first_name,
        "Last Name": last_name,
        "Position": position,
        "Base Salary": str(base_salary),
        "Increment": str(increment),
        "Deductions": str(deductions),
        "Bonus": str(bonus),
        "Classification": classification,
        "Start Date": start_date,
        "Hours Worked": "0",  # Initial hours worked set to 0
        "Performance Reviews": []  # Empty list for performance reviews
    })
    write_csv(department, data)
    print("Employee added successfully!")

def view_employees(department):
    data = read_csv(department)
    for employee in data:
        total_salary = float(employee["Base Salary"]) + float(employee["Increment"]) - float(employee["Deductions"]) + float(employee["Bonus"]) - float(employee["Pension"])
        print("First Name: {}, Last Name: {}, Position: {}, Base Salary: ${:.2f}, Increment: ${:.2f}, Deductions: ${:.2f}, Bonus: ${:.2f}, Pension: ${:.2f}, Total Salary: ${:.2f}".format(
            employee["First Name"], employee["Last Name"], employee["Position"],
            float(employee["Base Salary"]), float(employee["Increment"]), float(employee["Deductions"]),
            float(employee["Bonus"]), float(employee["Pension"]), total_salary
        ))
        print("Hours Worked: {}, Performance Reviews: {}".format(employee["Hours Worked"], employee["Performance Reviews"]))

def calculate_payroll(department):
    data = read_csv(department)
    total_salary = sum(
        float(employee["Base Salary"]) + float(employee["Increment"]) - float(employee["Deductions"]) + float(employee["Bonus"]) - float(employee["Pension"])
        for employee in data
    )
    total_increment = sum(float(employee["Increment"]) for employee in data)
    total_deductions = sum(float(employee["Deductions"]) for employee in data)
    total_bonus = sum(float(employee["Bonus"]) for employee in data)
    total_pension = sum(float(employee["Pension"]) for employee in data)
    
    print(f"Total Payroll for {department}: ${total_salary:.2f}")
    print(f"Total Increment: ${total_increment:.2f}")
    print(f"Total Deductions: ${total_deductions:.2f}")
    print(f"Total Bonus: ${total_bonus:.2f}")
    print(f"Total Pension: ${total_pension:.2f}")

def calculate_pension(employee):
    base_salary = float(employee["Base Salary"])
    increment = float(employee["Increment"])
    pension_percentage = 5  # Adjust the pension percentage as needed
    pension_contribution = (base_salary + increment) * pension_percentage / 100
    return pension_contribution

def remove_employee(department, employee_name):
    data = read_csv(department)
    updated_data = [employee for employee in data if employee["First Name"].lower() != employee_name.lower()]
    write_csv(department, updated_data)
    print("Employee removed successfully!")

def update_employee(department, employee_name):
    data = read_csv(department)
    for employee in data:
        if employee["First Name"].lower() == employee_name.lower():
            print(f"Updating information for {employee_name}:")
            employee["Last Name"] = input("Enter updated last name: ")
            employee["Position"] = input("Enter updated position: ")
            employee["Base Salary"] = float(input("Enter updated base salary: "))
            employee["Increment"] = (employee["Base Salary"] * float(input("Enter updated increment percentage: "))) / 100
            employee["Deductions"] = float(input("Enter updated deductions: "))
            employee["Bonus"] = float(input("Enter updated bonus: "))
            employee["Classification"] = input("Enter updated classification (e.g., Full-Time, Part-Time): ")
            write_csv(department, data)
            print("Employee information updated successfully.")
            return
    print(f"No employee found with the name {employee_name}.")

def save_payroll_report(department):
    data = read_csv(department)
    with open(f'payroll_report_{department.lower()}.txt', 'w') as report_file:
        report_file.write(f"Payroll Report for {department}\n")
        report_file.write("==================================\n")
        for employee in data:
            total_salary = float(employee["Base Salary"]) + float(employee["Increment"]) - float(employee["Deductions"]) + float(employee["Bonus"])
            report_file.write("First Name: {}, Last Name: {}, Position: {}, Base Salary: ${:.2f}, Increment: ${:.2f}, Deductions: ${:.2f}, Bonus: ${:.2f}, Total Salary: ${:.2f}\n".format(
                employee["First Name"], employee["Last Name"], employee["Position"],
                float(employee["Base Salary"]), float(employee["Increment"]), float(employee["Deductions"]),
                float(employee["Bonus"]), total_salary
            ))
    print("Payroll report saved successfully!")

def sort_employees(department, key):
    data = read_csv(department)
    sorted_data = sorted(data, key=lambda x: x[key])
    print(f"Employees in {department} sorted by {key}:")
    for employee in sorted_data:
        total_salary = float(employee["Base Salary"]) + float(employee["Increment"]) - float(employee["Deductions"]) + float(employee["Bonus"])
        print("First Name: {}, Last Name: {}, Position: {}, Base Salary: ${:.2f}, Increment: ${:.2f}, Deductions: ${:.2f}, Bonus: ${:.2f}, Total Salary: ${:.2f}".format(
            employee["First Name"], employee["Last Name"], employee["Position"],
            float(employee["Base Salary"]), float(employee["Increment"]), float(employee["Deductions"]),
            float(employee["Bonus"]), total_salary
        ))

def search_employee(department, search_term):
    data = read_csv(department)
    search_results = [employee for employee in data if search_term.lower() in employee["First Name"].lower() or search_term.lower() in employee["Last Name"].lower()]
    
    if search_results:
        print(f"Search results for '{search_term}':")
        for employee in search_results:
            total_salary = float(employee["Base Salary"]) + float(employee["Increment"]) - float(employee["Deductions"]) + float(employee["Bonus"])
            print("First Name: {}, Last Name: {}, Position: {}, Base Salary: ${:.2f}, Increment: ${:.2f}, Deductions: ${:.2f}, Bonus: ${:.2f}, Total Salary: ${:.2f}".format(
                employee["First Name"], employee["Last Name"], employee["Position"],
                float(employee["Base Salary"]), float(employee["Increment"]), float(employee["Deductions"]),
                float(employee["Bonus"]), total_salary
            ))
    else:
        print(f"No results found for '{search_term}'.")

def visualize_payroll_distribution(department):
    data = read_csv(department)
    total_salaries = [float(employee["Base Salary"]) + float(employee["Increment"]) - float(employee["Deductions"]) + float(employee["Bonus"]) for employee in data]
    
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(data)), total_salaries, align='center', alpha=0.7)
    plt.xlabel('Employee')
    plt.ylabel('Total Salary ($)')
    plt.title(f'Total Salary Distribution for {department}')
    plt.show()

def track_hours_worked(department, employee_name, hours_worked):
    data = read_csv(department)
    for employee in data:
        if employee["First Name"].lower() == employee_name.lower():
            employee["Hours Worked"] = str(hours_worked)
            write_csv(department, data)
            print(f"Hours worked for {employee_name} tracked successfully.")
            return
    print(f"No employee found with the name {employee_name}.")

def conduct_performance_review(department, employee_name, score, comments):
    data = read_csv(department)
    for employee in data:
        if employee["First Name"].lower() == employee_name.lower():
            if "Performance Reviews" not in employee:
                employee["Performance Reviews"] = []
            review = {"Date": datetime.now().strftime("%Y-%m-%d"), "Score": score, "Comments": comments}
            employee["Performance Reviews"].append(review)
            write_csv(department, data)
            print(f"Performance review for {employee_name} conducted successfully.")
            return
    print(f"No employee found with the name {employee_name}.")

if authenticate(): # Main program loop
    print("Welcome to the Enhanced Payroll Management System!")

    while True:
        print("\nMenu:")
        print("1. Select Department")
        print("2. Add Employee")
        print("3. View Employees")
        print("4. Calculate Payroll")
        print("5. Remove Employee")
        print("6. Update Employee Information")
        print("7. Save Payroll Report")
        print("8. Sort Employees")
        print("9. Search Employees")
        print("10. Visualize Payroll Distribution")
        print("11. Track Hours Worked")
        print("12. Conduct Performance Review")
        print("13. Exit")

        main_choice = input("Enter your choice: ")

        if main_choice == "1":
            department = select_department()
            if department not in department_files:
                initialize_csv(department)

        elif main_choice == "2":
            department = select_department()
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            position = input("Enter position: ")
            base_salary = float(input("Enter base salary: "))
            increment_percentage = float(input("Enter increment percentage: "))
            deductions = float(input("Enter deductions: "))
            bonus = float(input("Enter bonus: "))
            classification = input("Enter classification (e.g., Full-Time, Part-Time): ")
            add_employee(department, first_name, last_name, position, base_salary, increment_percentage, deductions, bonus, classification)

        elif main_choice == "3":
            department = select_department()
            view_employees(department)

        elif main_choice == "4":
            department = select_department()
            calculate_payroll(department)

        elif main_choice == "5":
            department = select_department()
            employee_name = input("Enter the first name of the employee to remove: ")
            remove_employee(department, employee_name)

        elif main_choice == "6":
            department = select_department()
            employee_name = input("Enter the first name of the employee to update: ")
            update_employee(department, employee_name)

        elif main_choice == "7":
            department = select_department()
            save_payroll_report(department)

        elif main_choice == "8":
            department = select_department()
            sort_key = input("Enter the key to sort employees (e.g., 'First Name', 'Base Salary'): ")
            sort_employees(department, sort_key)

        elif main_choice == "9":
            department = select_department()
            search_term = input("Enter the search term: ")
            search_employee(department, search_term)

        elif main_choice == "10":
            department = select_department()
            visualize_payroll_distribution(department)

        elif main_choice == "11":
            department = select_department()
            employee_name = input("Enter the first name of the employee to track hours worked: ")
            hours_worked = float(input("Enter the number of hours worked: "))
            track_hours_worked(department, employee_name, hours_worked)

        elif main_choice == "12":
            department = select_department()
            employee_name = input("Enter the first name of the employee for the performance review: ")
            score = float(input("Enter the performance score (1-10): "))
            comments = input("Enter performance review comments: ")
            conduct_performance_review(department, employee_name, score, comments)

        elif main_choice == "13":
            print("Exiting the Enhanced Payroll System.")
            break


