stage {'repo': before => Stage['pre']}

class apt {
  exec {'apt-get-update':
    path => '/usr/local/bin:/usr/bin:/bin',
    command => 'apt-get update',
  }
}

class {'apt': stage => 'repo' }

define apt::repo ($source, $key) {

  file {"/etc/apt/sources.list.d/${name}.list":
    source => "${source}",
    owner => root,
    group => root,
    mode => 0644,
    notify => Exec['apt-get-update'],
  }

  apt::key{"${name}-key":
    key => "${key}",
  }
}

define apt::key($key) {
  exec {"${name}-exec":
    command => "/usr/bin/env bash -c 'apt-key adv --recv-key --keyserver keyserver.ubuntu.com ${key}'",
  }
}

Apt::Repo <| |> -> Exec['apt-get-update']
Apt::Key <| |> -> Exec['apt-get-update']