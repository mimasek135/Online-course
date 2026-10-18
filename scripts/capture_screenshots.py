"""Capture the real local Django admin and a real successful exam submission."""
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
from django.test import Client
from onlinecourse.models import Course
from playwright.sync_api import sync_playwright

base_url = os.environ.get('SCREENSHOT_BASE_URL', 'http://127.0.0.1:8000').rstrip('/')
user = get_user_model().objects.get(username=os.environ.get('SCREENSHOT_USERNAME', 'demo_admin'))
if not user.is_staff or not user.is_superuser:
    raise SystemExit('Screenshot account must be a local superuser.')
client = Client()
client.force_login(user)
session_key = client.cookies['sessionid'].value
course = Course.objects.get(name='Django Web Development')
correct_ids = list(course.question_set.values_list('choice__id', flat=True).filter(choice__is_correct=True))
out = Path(__file__).resolve().parents[1] / 'screenshots'
out.mkdir(exist_ok=True)
with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    context = browser.new_context(viewport={'width': 1440, 'height': 1080}, device_scale_factor=1)
    context.add_cookies([{'name': 'sessionid', 'value': session_key, 'url': base_url}])
    page = context.new_page()
    page.goto(base_url + '/admin/', wait_until='networkidle')
    page.get_by_role('heading', name='Site administration').wait_for()
    assert page.get_by_text('Authentication and Authorization', exact=True).count()
    assert page.get_by_role('link', name='OnlineCourse', exact=True).count()
    page.screenshot(path=str(out / '03-admin-site.png'), full_page=True)
    page.goto(f'{base_url}/course/{course.pk}/', wait_until='networkidle')
    for pk in correct_ids:
        page.locator(f'#choice-{pk}').check()
    page.get_by_role('button', name='Submit exam', exact=True).click()
    page.get_by_role('heading', name='Congratulations!', exact=True).wait_for()
    assert '100%' in page.locator('.score').inner_text()
    assert page.get_by_role('heading', name='Exam results', exact=True).count()
    page.screenshot(path=str(out / '07-final.png'), full_page=True)
    print('Saved actual screenshots:', out)
    print('Successful exam result:', page.url)
    browser.close()
