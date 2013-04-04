from .base import *

DATABASES = {
    'default': dj_database_url.config(default='sqlite:///%s' % os.path.join(os.path.dirname(__file__), '..', '..', '..', 'testing.sqlite3')),
}

INSTALLED_APPS += [
    'django_jenkins',
]

PROJECT_APPS = [
    'stores',
]

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.django_tests',
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
)