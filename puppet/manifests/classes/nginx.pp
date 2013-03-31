class nginx {

  include nginx::apt

  package {'nginx':
    ensure => latest,
    require => Apt::Repo['nginx'],
  }
  service {'nginx':
    ensure => running,
    enable => true,
    require => Package['nginx'],
  }

  file{['/etc/nginx/sites-available', '/etc/nginx/sites-enabled']:
    ensure => directory,
  }

  # Remove the default config
  file {['/etc/nginx/sites-enabled/default', '/etc/nginx/conf.d/default.conf']:
    ensure => absent,
    require => Package['nginx'],
    notify => Service['nginx'],
  }

  file {'/etc/nginx/nginx.conf':
    owner => root,
    group => root,
    mode => 0644,
    ensure => present,
    source => '/vagrant/puppet/files/nginx/nginx.conf',
    require => Package['nginx'],
    notify => Service['nginx'],
  }
}

class nginx::apt {
  apt::repo {'nginx':
    source => '/vagrant/puppet/files/nginx/nginx.list',
    key => 'ABF5BD827BD9BF62',
  }
}

class {'nginx::apt': stage => 'repo' }


# Setup a gunicorn instance in nginx
define nginx::gunicorn($ensure, $host, $port, $root, $static='') {
  case $ensure {
    enabled: {
      file{"/etc/nginx/sites-available/${name}.conf":
        content => template('nginx/gunicorn.erb'),
        ensure => present,
        notify => Service['nginx'],
        require => [Package['nginx'], File['/etc/nginx/sites-available']],
      }
      file{"/etc/nginx/sites-enabled/${name}.conf":
        ensure => link,
        target => "/etc/nginx/sites-available/${name}.conf",
        notify => Service['nginx'],
        require => [File["/etc/nginx/sites-available/${name}.conf"], File['/etc/nginx/sites-enabled']],
      }
    }
    absent: {
      file{"/etc/nginx/sites-available/${name}.conf":
        ensure => absent,
        notify => Service['nginx'],
      }
      file{"/etc/nginx/sites-enabled/${name}.conf":
        ensure => absent,
        notify => Service['nginx'],
      }
    }
  }
}