import secrets
from datetime import date
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from onlinecourse.models import Course, Lesson, Question, Choice

class Command(BaseCommand):
    help = 'Create an example course and a local administrator. Existing passwords are never reset.'
    def add_arguments(self, parser):
        parser.add_argument('--username', default='demo_admin')
    def handle(self, *args, **options):
        user, created = get_user_model().objects.get_or_create(username=options['username'])
        if created:
            password = secrets.token_urlsafe(16)
            user.is_staff = user.is_superuser = True
            user.set_password(password)
            user.save()
            self.stdout.write(f'Local admin username: {user.username}\nLocal admin password: {password}')
        else:
            self.stdout.write('User already exists; password and permissions unchanged.')
        course, created = Course.objects.get_or_create(name='Django Web Development', defaults={
            'description': 'Build your understanding of Django models, URL routing, and web forms.', 'pub_date': date(2026, 1, 1)})
        if created:
            for order, title, content in [(1, 'Models and the database', 'Django models describe stored data. A ForeignKey creates a many-to-one relationship.'),
                (2, 'URLs and views', 'URL patterns connect incoming requests to views. A view returns an HTTP response.'),
                (3, 'Forms and security', 'Use POST for submissions and include the CSRF token in internal POST forms.')]:
                Lesson.objects.create(course=course, order=order, title=title, content=content)
            data = [
                ('Which Django field creates a many-to-one relationship?', [('ForeignKey', True), ('CharField', False), ('BooleanField', False)]),
                ('Which file maps URL paths to views?', [('models.py', False), ('urls.py', True), ('admin.py', False)]),
                ('Which practices protect an exam submission? Select all correct answers.', [('Use POST', True), ('Include a CSRF token', True), ('Trust any submitted choice ID', False)]),
            ]
            for content, choices in data:
                q = Question.objects.create(course=course, content=content, grade=10)
                for text, correct in choices:
                    Choice.objects.create(question=q, content=text, is_correct=correct)
        self.stdout.write(self.style.SUCCESS(f'Course ready: /course/{course.pk}/'))
