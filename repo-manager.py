import requests
import json

# إعداد التوكن (token) الخاص بك من GitHub
# قم بإنشاء personal access token من إعدادات GitHub API
TOKEN = "your_personal_access_token_here"
USERNAME = "your_github_username_here"

# رأس التوثيق
headers = {
    'Authorization': f'token {TOKEN}',
    'Content-Type': 'application/json',
}

# إنشاء مستودع جديد على GitHub
def create_repo(repo_name):
    url = f"https://api.github.com/user/repos"
    data = {
        "name": repo_name,
        "private": False  # يمكنك تعديلها إلى True للمستودعات الخاصة
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 201:
        print(f"تم إنشاء مستودع جديد: {repo_name}")
    else:
        print(f"فشل في إنشاء المستودع: {response.status_code}")

# عرض مستودعاتك
def list_repos():
    url = f"https://api.github.com/users/{USERNAME}/repos"
    response = requests.get(url, headers=headers)
    repos = response.json()
    print("المستودعات الموجودة:")
    for repo in repos:
        print(f"- {repo['name']}")

# حذف مستودع
def delete_repo(repo_name):
    url = f"https://api.github.com/repos/{USERNAME}/{repo_name}"
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print(f"تم حذف المستودع: {repo_name}")
    else:
        print(f"فشل في حذف المستودع: {response.status_code}")

# مثال للاستخدام
if __name__ == "__main__":
    create_repo("test-repo-using-python")  # هنا يمكنك تجربة إنشاء مستودع
    list_repos()
    delete_repo("test-repo-using-python")  # حذف المستودع الذي أنشأته
