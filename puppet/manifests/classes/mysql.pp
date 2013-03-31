# Get mysql up and running
class mysql {
  package { "mysql-server":
    ensure => installed,
  }

  case $operatingsystem {
    ubuntu: {
      package { "libmysqld-dev":
        ensure => installed,
      }
    }
  }

  service { "mysql":
    ensure => running,
    enable => true,
    require => Package['mysql-server'],
  }
}

define mysql::database($user, $password) {
  exec { "create-${name}-db":
    unless => "/usr/bin/mysql -uroot ${name}",
    command => "/usr/bin/mysql -uroot -e \"create database ${name};\"",
    require => Service["mysql"],
  }

  exec { "grant-${name}-db":
    unless => "/usr/bin/mysql -u${user} -p${password} ${name}",
    command => "/usr/bin/mysql -uroot -e \"grant all on ${name}.* to ${user}@localhost identified by '$password';\"",
    require => [Service["mysql"], Exec["create-${name}-db"]]
  }
}
