package { 'siege':
  ensure => present,
  before => File['/root/.siegerc'],
}

file {'/root/.siegerc':
  ensure => file,
  mode => 644,
  source => '/root/puppet/siegerc',
}

file {'/etc/sysctl.conf':
  ensure => file,
  mode => 644,
  source => '/root/puppet/sysctl.conf',
}

exec {'/sbin/sysctl -p':
  subscribe => File['/etc/sysctl.conf'],
}