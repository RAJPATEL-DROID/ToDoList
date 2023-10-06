# ToDo-List


class TaskListMemento:
    def __init__(self, tasks):
        self.tasks = tasks.copy()


class TaskBuilder:
    def __init__(self, description):
        self.description = description
        self.due_date = None
        self.tags = []

    def set_due_date(self, due_date):
        self.due_date = due_date
        return self

    def add_tags(self, tags):
        self.tags.extend(tags)
        return self

    def build(self):
        return Task(self.description, self.due_date, self.tags)

# Task Class
class Task:
    def __init__(self, description, due_date=None, tags=None):
        self.description = description
        self.completed = False
        self.due_date = due_date
        self.tags = tags or []

    def mark_completed(self):
        self.completed = True

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        due_date_str = f", Due: {self.due_date}" if self.due_date else ""
        return f"{self.description} - {status}{due_date_str}"


class TaskList:
    def __init__(self):
        self.tasks = []
        self.history = []

    def add_task(self, task):
        self.tasks.append(task)
        self.save_state()

    def mark_completed(self, description):
        for task in self.tasks:
            if task.description == description:
                task.mark_completed()
                self.save_state()
                return True
        return False

    def delete_task(self, description):
        self.tasks = [task for task in self.tasks if task.description != description]
        self.save_state()

    def view_tasks(self, filter_type="all"):
        if filter_type == "completed":
            return [task for task in self.tasks if task.completed]
        elif filter_type == "pending":
            return [task for task in self.tasks if not task.completed]
        else:
            return self.tasks

    def undo(self):
        if len(self.history) > 1:
            self.history.pop()
            self.tasks = self.history[-1].tasks.copy()

    def redo(self):
        if len(self.history) < len(self.tasks):
            self.tasks = self.history[len(self.history)].tasks.copy()
            self.history.append(TaskListMemento(self.tasks.copy()))

    def save_state(self):
        self.history.append(TaskListMemento(self.tasks.copy()))


if __name__ == "__main__":
    todo_list = TaskList()

    while True:
        print("\nOptions:")
        print("1. Add Task")
        print("2. Mark Completed")
        print("3. Delete Task")
        print("4. View Tasks")
        print("5. Undo")
        print("6. Redo")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            description = input("Enter task description: ")
            due_date = input("Enter due date (optional): ")
            tags = input("Enter tags (optional, comma-separated): ").split(",")
            task = TaskBuilder(description).set_due_date(due_date.strip()).add_tags(tags).build()
            todo_list.add_task(task)
            print(f"Task '{description}' added.")

        elif choice == "2":
            description = input("Enter task description to mark as completed: ")
            if todo_list.mark_completed(description):
                print(f"Task '{description}' marked as completed.")
            else:
                print(f"Task '{description}' not found.")

        elif choice == "3":
            description = input("Enter task details to delete: ")
            todo_list.delete_task(description)
            print(f"Task '{description}' deleted.")

        elif choice == "4":
            filter_type = input("Enter filter type ('all', 'completed', 'pending'): ")
            tasks = todo_list.view_tasks(filter_type)
            if tasks:
                print("\nTask List:")
                for i, task in enumerate(tasks, 1):
                    print(f"{i}. {task}")
            else:
                print("No tasks found.")

        elif choice == "5":
            todo_list.undo()
            print("Undo Finished.")

        elif choice == "6":
            todo_list.redo()
            print("Redo Finished.")

        elif choice == "7":
            break

        else:
            print("Invalid choice.Kindly try again.")
