package { 'siege':
  ensure => present,
  before => File['/root/.siegerc'],
}

file {'/root/.siegerc':
  ensure => file,
  mode => 644,
  source => '/root/puppet/siegerc',
}