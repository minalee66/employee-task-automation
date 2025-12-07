import csv

class Task:
    def __init__(self, title, deadline):
        self.title = title
        self.deadline = deadline
        self.completed = False

    def mark_completed(self):
        self.completed = True


class Employee:
    def __init__(self, emp_id, name):
        self.emp_id = emp_id
        self.name = name
        self.tasks = []

    def assign_task(self, task):
        self.tasks.append(task)

    def show_tasks(self):
        for i, task in enumerate(self.tasks, 1):
            status = "✅ Completed" if task.completed else "⏳ Pending"
            print(f"{i}. {task.title} (Deadline: {task.deadline}) - {status}")


class TaskManager:
    def __init__(self, filename="employees.csv"):
        self.filename = filename

    def save_tasks(self, employee):
        # Rewrite the file to avoid duplicate rows for the same employee
        employees = self.load_tasks()
        employees[employee.emp_id] = employee
        with open(self.filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            for emp in employees.values():
                for task in emp.tasks:
                    writer.writerow([emp.emp_id, emp.name, task.title, task.deadline, task.completed])

    def load_tasks(self):
        employees = {}
        try:
            with open(self.filename, mode="r") as file:
                reader = csv.reader(file)
                for row in reader:
                    emp_id, name, title, deadline, completed = row
                    if emp_id not in employees:
                        employees[emp_id] = Employee(emp_id, name)
                    task = Task(title, deadline)
                    task.completed = completed == "True"
                    employees[emp_id].assign_task(task)
        except FileNotFoundError:
            pass
        return employees


if __name__ == "__main__":
    manager = TaskManager()

    while True:
        print("\n--- Employee Task System ---")
        print("1. Add Employee and Tasks")
        print("2. View All Tasks")
        print("3. Mark Task Completed")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            employees = manager.load_tasks()
            emp_id = input("Enter Employee ID: ")

            # Prevent duplicate IDs
            if emp_id in employees:
                print(f"Error: Employee ID {emp_id} already exists for {employees[emp_id].name}.")
                print("Please use a different Employee ID.")
                continue

            name = input("Enter Employee Name: ")
            emp = Employee(emp_id, name)

            while True:
                title = input("Enter Task Title: ")
                deadline = input("Enter Task Deadline (YYYY-MM-DD): ")
                task = Task(title, deadline)
                emp.assign_task(task)

                more = input("Add another task? (y/n): ")
                if more.lower() != "y":
                    break

            manager.save_tasks(emp)

        elif choice == "2":
            employees = manager.load_tasks()
            for emp_id, emp in employees.items():
                print(f"\nTasks for {emp.name}:")
                emp.show_tasks()

        elif choice == "3":
            employees = manager.load_tasks()
            emp_id = input("Enter Employee ID: ")
            emp = employees.get(emp_id)
            if emp:
                while True:
                    emp.show_tasks()
                    task_no = int(input("Enter task number to mark completed: "))
                    emp.tasks[task_no - 1].mark_completed()
                    manager.save_tasks(emp)
                    print("Task marked as completed ✅")

                    more = input("Mark another task for this employee? (y/n): ")
                    if more.lower() != "y":
                        break
            else:
                print("Employee not found.")

        elif choice == "4":
            print("Exiting system...")
            break
