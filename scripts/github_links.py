"""Print submission links after the project has been uploaded to GitHub."""
import argparse
import re
parser = argparse.ArgumentParser()
parser.add_argument('username', help='Your GitHub username')
parser.add_argument('--repo', default='onlinecourse-project')
parser.add_argument('--branch', default='main')
a = parser.parse_args()
if not re.fullmatch(r'[A-Za-z0-9-]+', a.username):
    parser.error('Use a GitHub username, not an email or full URL.')
from urllib.parse import quote
base = f'https://github.com/{a.username}/{quote(a.repo, safe="")}/blob/{quote(a.branch, safe="")}'
for number, file in [(1, 'onlinecourse/models.py'), (2, 'onlinecourse/admin.py'),
                     (4, 'onlinecourse/templates/onlinecourse/course_details_bootstrap.html'),
                     (5, 'onlinecourse/views.py'), (6, 'onlinecourse/urls.py')]:
    print(f'Task {number}: {base}/{file}')
print('Task 3: upload screenshots/03-admin-site.png')
print('Task 7: upload screenshots/07-final.png')
