package { 'nginx':
  ensure => present,
  before => [File['/etc/nginx/nginx.conf'], File['/etc/default/nginx']],
}

file {'/etc/nginx/nginx.conf':
  ensure => file,
  mode => 644,
  source => '/root/puppet/nginx.conf',
}

file {'/etc/default/nginx':
  ensure => file,
  mode => 644,
  source => '/root/puppet/nginx.def',
}

service { 'nginx':
  ensure => running,
  enable => true,
  hasrestart => true,
  hasstatus => true,
  subscribe => [File['/etc/nginx/nginx.conf'], File['/etc/default/nginx']],
}
