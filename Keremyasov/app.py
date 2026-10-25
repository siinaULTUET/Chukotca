import tkinter as tk
from tkinter import messagebox
import json
import os

FILE_NAME = "tasks.json"

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Менеджер задач")
        self.tasks = []
        self.load_tasks()

        self.entry = tk.Entry(root, width=40)
        self.entry.pack(pady=10)

        tk.Button(root, text="Добавить", command=self.add_task).pack(pady=5)
        
        self.listbox = tk.Listbox(root, width=50, height=10)
        self.listbox.pack(pady=10)

        tk.Button(root, text="Удалить", command=self.delete_task).pack(pady=5)
        tk.Button(root, text="Отметить выполненной", command=self.toggle_task).pack(pady=5)

    def load_tasks(self):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                self.tasks = json.load(f)
                for task in self.tasks:
                    self.listbox.insert(tk.END, task["text"] + (" [Выполнено]" if task["done"] else ""))

    def save_tasks(self):
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False)

    def add_task(self):
        text = self.entry.get().strip()
        if not text:
            messagebox.showwarning("Ошибка", "Введите текст задачи")
            return
        task = {"text": text, "done": False}
        self.tasks.append(task)
        self.listbox.insert(tk.END, text)
        self.entry.delete(0, tk.END)
        self.save_tasks()

    def delete_task(self):
        try:
            index = self.listbox.curselection()[0]
            self.listbox.delete(index)
            del self.tasks[index]
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Ошибка", "Выберите задачу для удаления")

    def toggle_task(self):
        try:
            index = self.listbox.curselection()[0]
            task = self.tasks[index]
            task["done"] = not task["done"]
            self.listbox.delete(index)
            self.listbox.insert(index, task["text"] + (" [Выполнено]" if task["done"] else ""))
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Ошибка", "Выберите задачу")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()
