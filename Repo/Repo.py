import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import requests
import json
import os
import subprocess

# إعدادات مبدئية للتوكن واسم المستخدم
username = ""
token = ""

# إعدادات GitHub
headers = {}

# دالة لطلب التوكن واسم المستخدم
def ask_credentials():
    global username, token, headers
    username = simpledialog.askstring("اسم المستخدم", "أدخل اسم المستخدم:")
    token = simpledialog.askstring("التوكن", "أدخل التوكن الشخصي:")
    
    if username and token:
        headers = {
            'Authorization': f'token {token}',
            'Content-Type': 'application/json',
        }
        # بعد إدخال البيانات نعرض الواجهة الرئيسية
        show_main_menu()
    else:
        messagebox.showerror("خطأ", "اسم المستخدم أو التوكن غير صحيح.")
        app.quit()  # إغلاق التطبيق إذا لم يتم إدخال البيانات بشكل صحيح

# دالة لاختيار مجلد وإضافته إلى الريبو
def add_folder_to_repo():
    folder_path = filedialog.askdirectory(title="اختر المجلد لإضافته")
    
    if folder_path:
        repo_dir = simpledialog.askstring("إدخال مسار الريبو", "أدخل مسار الريبو على جهازك:")
        
        if repo_dir:
            try:
                # الانتقال إلى مجلد الريبو
                os.chdir(repo_dir)
                
                # تنفيذ أوامر Git لإضافة المجلد وcommit وpush
                subprocess.run(["git", "add", folder_path], check=True)
                commit_message = simpledialog.askstring("Commit Message", "أدخل رسالة التغيير:")
                if commit_message:
                    subprocess.run(["git", "commit", "-m", commit_message], check=True)
                    subprocess.run(["git", "push"], check=True)
                    messagebox.showinfo("نجاح", f"تم إضافة المجلد {folder_path} إلى المستودع بنجاح!")
                else:
                    messagebox.showwarning("تحذير", "لم يتم إدخال رسالة commit.")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("خطأ", f"فشل في تنفيذ الأمر: {e}")
            except Exception as e:
                messagebox.showerror("خطأ", f"حدث خطأ: {e}")
        else:
            messagebox.showwarning("تحذير", "لم يتم إدخال مسار الريبو.")
    else:
        messagebox.showwarning("تحذير", "لم يتم اختيار أي مجلد.")

# دالة إنشاء المستودع
def create_repo():
    repo_name = simpledialog.askstring("إنشاء مستودع", "أدخل اسم المستودع:")
    if not repo_name:
        return
    url = "https://api.github.com/user/repos"
    data = {"name": repo_name, "private": False}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 201:
        messagebox.showinfo("نجاح", f"تم إنشاء المستودع: {repo_name}")
    else:
        messagebox.showerror("خطأ", f"فشل في الإنشاء: {response.status_code}")

# دالة حذف المستودع
def delete_repo():
    repo_name = simpledialog.askstring("حذف مستودع", "أدخل اسم المستودع:")
    if not repo_name:
        return
    url = f"https://api.github.com/repos/{username}/{repo_name}"
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        messagebox.showinfo("نجاح", f"تم حذف المستودع: {repo_name}")
    else:
        messagebox.showerror("خطأ", f"فشل في الحذف: {response.status_code}")

# دالة استعراض المستودعات
def list_repos():
    url = f"https://api.github.com/users/{username}/repos"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            repos = response.json()
            repo_list = "\n".join([f"- {repo['name']}" for repo in repos])
            messagebox.showinfo("المستودعات", repo_list or "لا توجد مستودعات.")
        else:
            messagebox.showerror("خطأ", f"فشل في جلب المستودعات: {response.status_code}")
    except Exception as e:
        messagebox.showerror("خطأ", f"حدث خطأ أثناء استعراض المستودعات: {e}")

# دوال Git - Commit, Push, Pull
def commit_changes():
    try:
        subprocess.run(["git", "add", "."], check=True)
        commit_message = simpledialog.askstring("Commit Message", "أدخل رسالة التغيير:")
        if commit_message:
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            subprocess.run(["git", "push"], check=True)
            messagebox.showinfo("نجاح", "تم تنفيذ commit و push بنجاح!")
        else:
            messagebox.showwarning("تحذير", "لم يتم إدخال رسالة commit.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("خطأ", f"فشل في تنفيذ الأمر: {e}")
    except Exception as e:
        messagebox.showerror("خطأ", f"حدث خطأ: {e}")

def push_changes():
    try:
        subprocess.run(["git", "push"], check=True)
        messagebox.showinfo("نجاح", "تم إرسال التغييرات إلى GitHub!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("خطأ", f"فشل في تنفيذ الأمر: {e}")

def pull_changes():
    try:
        subprocess.run(["git", "pull"], check=True)
        messagebox.showinfo("نجاح", "تم سحب التغييرات من GitHub!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("خطأ", f"فشل في تنفيذ الأمر: {e}")

# دالة استنساخ مستودع من GitHub
def clone_repo():
    repo_url = simpledialog.askstring("استنساخ مستودع", "أدخل رابط المستودع من GitHub:")
    if not repo_url:
        return
    directory = filedialog.askdirectory(title="اختر المجلد لحفظ المستودع")
    if directory:
        try:
            subprocess.run(["git", "clone", repo_url, directory], check=True)
            messagebox.showinfo("نجاح", f"تم استنساخ المستودع إلى {directory}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("خطأ", f"فشل في استنساخ المستودع: {e}")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ: {e}")

# إعداد واجهة المستخدم الرئيسية
def show_main_menu():
    app.title("RepoGPT")
    app.configure(bg="#1e1e1e")
    app.geometry("1200x600")  # نافذة أكبر
    app.resizable(True, True)

    button_frame = tk.Frame(app, bg="#1e1e1e")
    button_frame.pack(pady=30)

    def custom_button(text, command):
        return tk.Button(button_frame, text=text, command=command,
                         bg="#333", fg="white", font=("Arial", 12), padx=10, pady=5)

    buttons = [
        ("📥 Pull", pull_changes),
        ("📤 Push", push_changes),
        ("📝 Commit", commit_changes),
        ("📦 Create Repo", create_repo),
        ("🗑️ Delete Repo", delete_repo),
        ("📄 List Repos", list_repos),
        ("📂 Add Folder", add_folder_to_repo),
        ("🖥️ Clone Repo", clone_repo),
    ]

    for i, (text, command) in enumerate(buttons):
        btn = custom_button(text, command)
        btn.grid(row=0, column=i, padx=5)

# إعداد التطبيق
app = tk.Tk()
ask_credentials()  # طلب البيانات عند البداية

# بدء التطبيق
app.mainloop()
