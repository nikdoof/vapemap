
import "classes/*.pp"

include apt
include python
include nginx
include mysql
include supervisor

$database = "mysql://vapemap:randompassword1234@localhost/vapemap"

mysql::database{'vapemap':
  user => 'vapemap',
  password => 'randompassword1234'
}

python::venv {'vapemap':
  path => "/usr/local/${name}-venv",
  requirements => '/vagrant/requirements.txt',
}

file{'/usr/local/bin/vapemap-init.sh':
  content => "#!/bin/bash\n. /usr/local/main-venv/bin/activate\nDATABASE_URL=$database /usr/bin/env python manage.py run_gunicorn -c gunicorn_config --preload",
  ensure => present,
  mode => 755,
}

supervisor::program {'vapemap':
  command => '/usr/local/bin/vapemap-init.sh',
  directory => '/vagrant/app/',
  user => 'vagrant',
  require => [File['/usr/local/bin/vapemap-init.sh'], Python::Venv['vapemap'], Mysql::Database['vapemap']],
}

nginx::gunicorn { 'vapemap':
  ensure => enabled,
  host => '_',
  port => 3322,
  root => '/vagrant/root/',
  static => '/vagrant/static/',
}

exec{'vapemap-collectstatic':
  command => "/usr/bin/env bash -c 'source /usr/local/main-venv/bin/activate; cd /vagrant/app;DATABASE_URL=$database /usr/bin/env python ./manage.py collectstatic --noinput'",
  path => '/usr/local/bin:/usr/bin:/bin',
  require => Python::Venv['vapemap'],
}

exec{'vapemap-syncdb':
  command => "/usr/bin/env bash -c 'source /usr/local/main-venv/bin/activate; cd /vagrant/app;DATABASE_URL=$database /usr/bin/env python ./manage.py syncdb --all --noinput'",
  path => '/usr/local/bin:/usr/bin:/bin',
  require => [Python::Venv['vapemap'], Mysql::Database['vapemap']],
}

exec{'vapemap-migrationfake':
  command => "/usr/bin/env bash -c 'source /usr/local/main-venv/bin/activate; cd /vagrant/app;DATABASE_URL=$database /usr/bin/env python ./manage.py migrate --fake --noinput'",
  path => '/usr/local/bin:/usr/bin:/bin',
  require => Exec['vapemap-syncdb'],
}