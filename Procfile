web: cd app; python manage.py collectstatic --noinput; python manage.py run_gunicorn
debug: cd app; python manage.py collectstatic --noinput; DJANGO_DEBUG=1 python manage.py run_gunicorn
update_haystack: cd app; python manage.py update_index
reindex_haystack: cd app; python manage.py rebuild_index --noinput
syncdb: cd app; python manage.py syncdb --migrate --noinput