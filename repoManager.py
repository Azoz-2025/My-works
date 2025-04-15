import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import requests
import json
import os
import subprocess

# ألوان داكنة
BG_COLOR = "#1e1e1e"
FG_COLOR = "#ffffff"
BTN_COLOR = "#3a3a3a"

class GitHubRepoManager:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub Repo Manager")
        self.root.geometry("800x500")  # حجم متوسط للنافذة
        self.root.configure(bg=BG_COLOR)

        self.token = ""
        self.username = ""

        self.create_widgets()

    def create_widgets(self):
        self.token_label = tk.Label(self.root, text="GitHub Token:", bg=BG_COLOR, fg=FG_COLOR)
        self.token_label.pack()
        self.token_entry = tk.Entry(self.root, show="*", width=50)
        self.token_entry.pack(pady=5)

        self.username_label = tk.Label(self.root, text="GitHub Username:", bg=BG_COLOR, fg=FG_COLOR)
        self.username_label.pack()
        self.username_entry = tk.Entry(self.root, width=50)
        self.username_entry.pack(pady=5)

        self.button_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.button_frame.pack(pady=10)

        buttons = [
            ("Create Repo", self.create_repo),
            ("List Repos", self.list_repos),
            ("Delete Repo", self.delete_repo),
            ("Git Commit", self.git_commit),
            ("Git Push", self.git_push),
            ("Git Pull", self.git_pull),
            ("Help", self.show_help)
        ]

        for text, command in buttons:
            btn = tk.Button(self.button_frame, text=text, command=command, bg=BTN_COLOR, fg=FG_COLOR, width=12)
            btn.pack(side=tk.LEFT, padx=5)

        self.output = scrolledtext.ScrolledText(self.root, height=15, width=90, bg=BTN_COLOR, fg=FG_COLOR)
        self.output.pack(pady=10)

    def get_headers(self):
        self.token = self.token_entry.get()
        self.username = self.username_entry.get()
        return {
            'Authorization': f'token {self.token}',
            'Content-Type': 'application/json',
        }

    def create_repo(self):
        repo_name = simpledialog.askstring("Create Repo", "Enter repo name:")
        if not repo_name:
            return
        url = "https://api.github.com/user/repos"
        data = json.dumps({"name": repo_name, "private": False})
        response = requests.post(url, headers=self.get_headers(), data=data)
        if response.status_code == 201:
            self.output.insert(tk.END, f"Repo '{repo_name}' created successfully.\n")
        else:
            self.output.insert(tk.END, f"Failed to create repo: {response.status_code}\n{response.text}\n")

    def list_repos(self):
        url = f"https://api.github.com/users/{self.username_entry.get()}/repos"
        response = requests.get(url, headers=self.get_headers())
        if response.status_code == 200:
            self.output.insert(tk.END, "Repositories:\n")
            for repo in response.json():
                self.output.insert(tk.END, f"- {repo['name']}\n")
        else:
            self.output.insert(tk.END, f"Failed to list repos: {response.status_code}\n{response.text}\n")

    def delete_repo(self):
        repo_name = simpledialog.askstring("Delete Repo", "Enter repo name to delete:")
        if not repo_name:
            return
        url = f"https://api.github.com/repos/{self.username_entry.get()}/{repo_name}"
        response = requests.delete(url, headers=self.get_headers())
        if response.status_code == 204:
            self.output.insert(tk.END, f"Repo '{repo_name}' deleted successfully.\n")
        else:
            self.output.insert(tk.END, f"Failed to delete repo: {response.status_code}\n{response.text}\n")

    def git_commit(self):
        msg = simpledialog.askstring("Git Commit", "Enter commit message:")
        if msg:
            self.run_git_command(["git", "add", "."])
            self.run_git_command(["git", "commit", "-m", msg])

    def git_push(self):
        self.run_git_command(["git", "push"])

    def git_pull(self):
        self.run_git_command(["git", "pull"])

    def run_git_command(self, command):
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            self.output.insert(tk.END, result.stdout + "\n")
        except subprocess.CalledProcessError as e:
            self.output.insert(tk.END, e.stderr + "\n")

    def show_help(self):
        help_text = (
            "Create Repo: ينشئ مستودع جديد في حسابك على GitHub.\n"
            "List Repos: يعرض جميع المستودعات الخاصة بك.\n"
            "Delete Repo: يحذف مستودع موجود.\n"
            "Git Commit: يضيف التعديلات ويحفظها محليًا برسالة.\n"
            "Git Push: يرفع التعديلات إلى GitHub.\n"
            "Git Pull: يسحب آخر التعديلات من GitHub.\n"
        )
        messagebox.showinfo("Help", help_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubRepoManager(root)
    root.mainloop()
