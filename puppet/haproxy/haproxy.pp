package { 'haproxy':
  ensure => present,
  before => [File['/etc/haproxy/haproxy.cfg'],File['/etc/default/haproxy']],
}

file {'/etc/haproxy/haproxy.cfg':
  ensure => file,
  mode => 644,
  source => '/root/puppet/haproxy.cfg',
}

file {'/etc/default/haproxy':
  ensure => file,
  mode => 644,
  source => '/root/puppet/haproxy.def',
}

service { 'haproxy':
  ensure => running,
  enable => true,
  hasrestart => true,
  hasstatus => true,
  subscribe => [File['/etc/haproxy/haproxy.cfg'],File['/etc/default/haproxy']],
}

file {'/etc/sysctl.conf':
  ensure => file,
  mode => 644,
  source => '/root/puppet/sysctl.conf',
}

exec {'/sbin/sysctl -p':
  before => Service['haproxy'],
  subscribe => File['/etc/sysctl.conf'],
}