import tkinter as tk
from tkinter import messagebox

# قائمة المهام
tasks = []

# حفظ المهام في ملف نصي
def save_tasks():
    with open("tasks.txt", "w") as file:
        for task in tasks:
            file.write(task + "\n")

# تحميل المهام من الملف
def load_tasks():
    try:
        with open("tasks.txt", "r") as file:
            global tasks
            tasks = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        tasks = []

# إضافة مهمة جديدة
def add_task():
    task = entry.get()
    if task != "":
        tasks.append(task)
        entry.delete(0, tk.END)
        update_task_list()
        save_tasks()

# حذف مهمة
def delete_task():
    try:
        index = listbox.curselection()[0]
        tasks.pop(index)
        update_task_list()
        save_tasks()
    except IndexError:
        messagebox.showwarning("تحذير", "اختار مهمة لحذفها")

# تحديث القائمة المعروضة
def update_task_list():
    listbox.delete(0, tk.END)
    for task in tasks:
        listbox.insert(tk.END, task)

# إعداد واجهة المستخدم
root = tk.Tk()
root.title("قائمة المهام")
root.geometry("400x400")

entry = tk.Entry(root, font=("Arial", 14))
entry.pack(pady=10)

add_button = tk.Button(root, text="أضف مهمة", font=("Arial", 14), command=add_task)
add_button.pack(pady=5)

delete_button = tk.Button(root, text="حذف مهمة", font=("Arial", 14), command=delete_task)
delete_button.pack(pady=5)

listbox = tk.Listbox(root, font=("Arial", 14), height=10)
listbox.pack(pady=10)

# تحميل المهام عند بدء التطبيق
load_tasks()
update_task_list()

# تشغيل التطبيق
root.mainloop()
