class redis {

  include redis::apt

  package {'redis-server':
    ensure => latest,
    require => Apt::Repo['redis'],
  }

  service { 'redis-server':
    ensure => running,
    enable => true,
    hasrestart => true,
    require => Package['redis-server'],
  }
}

class redis::apt {
  apt::repo {'redis':
    source => '/vagrant/puppet/files/redis/redis.list',
    key => '5862E31D',
  }
}

class {'redis::apt': stage => 'repo' }