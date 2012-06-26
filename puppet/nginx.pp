package { 'nginx':
  ensure => present,
  before => File['/etc/nginx/nginx.conf'],
}

file {'/etc/nginx/nginx.conf':
  ensure => file,
  mode => 644,
  source => '/root/puppet/nginx.conf',
}

service { 'nginx':
  ensure => running,
  enable => true,
  hasrestart => true,
  hasstatus => true,
  subscribe => File['/etc/nginx/nginx.conf'],
}
