class supervisor {
  package{'supervisor':
    ensure => latest,
  }

  service{'supervisor':
    ensure => running,
    hasrestart => false,
    require => Package['supervisor'],
  }
}

define supervisor::program(
  $command         = $title,
  $directory       = "/tmp/",
  $user            = "nobody",
  $autostart       = true,
  $autorestart     = true,
  $redirect_stderr = true)
  {

  file {"/etc/supervisor/conf.d/$title.conf":
    ensure => present,
    owner => "root",
    group => "root",
    content => template('supervisor/program.erb'),
    notify => Service['supervisor'],
    require => Package['supervisor'],
  }
}