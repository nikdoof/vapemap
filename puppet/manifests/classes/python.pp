stage { 'pre': before => Stage['main'] }

class python {

  package {
    "build-essential": ensure => latest;
    "python": ensure => latest;
    "python-dev": ensure => latest;
    "python-setuptools": ensure => installed;
    "git-core": ensure => installed;
    "mercurial": ensure => installed;
    "libevent-dev": ensure => installed;
    "libgeos-dev": ensure => installed;
  }
  exec {'pip-package':
    command => 'easy_install pip',
    path => '/usr/local/bin:/usr/bin:/bin',
    require => Package['python-setuptools'],
    subscribe => Package['python-setuptools'],
  }
  package {['virtualenv', 'virtualenvwrapper', 'gunicorn', 'gevent']:
    ensure => latest,
    provider => pip,
    require => Exec['pip-package'],
  }
}
class { 'python': stage => 'pre' }

define python::venv($path, $requirements) {

  file {"$requirements":
    ensure => present,
  }

  exec{"${name}-venv":
    path => '/usr/local/bin:/usr/bin:/bin',
    command => "virtualenv --system-site-packages ${path}",
    creates => "${path}",
    require => Package['virtualenv'],
  }
  exec {"${name}-requirements":
    command => "/usr/bin/env bash -c 'source ${path}/bin/activate; pip install -i http://f.pypi.python.org/simple -r ${requirements}'",
    require => Exec["${name}-venv"],
    subscribe => File["$requirements"],
  }

}