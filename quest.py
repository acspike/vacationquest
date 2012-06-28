#!/usr/bin/env python
import sys, os, time, code

#quest config
# - using precise 64 ami id
script_path = sys.path[0]
boto_config = os.path.join(script_path, 'boto.conf')
image_id = 'ami-3c994355'
name_prefix = 'acspike_quest_'
key_name = name_prefix+'key'
key_path = os.path.join(script_path, key_name+'.pem')
sec_group_name = name_prefix+'sec_group'
tag_name = name_prefix+'tag'
tags = ['siege1','siege2','haproxy','nginx1','nginx2']
user_data='''#!/bin/bash
/usr/bin/apt-get update
/usr/bin/apt-get -y install puppet-common
touch /root/user_data_script_complete
'''

#connect
# - obtain AWS credentials from user or cache on future invocations
if os.path.exists(boto_config):
    print 'Reading cached AWS credentials from %s\n' % (boto_config,)
else:
    print 'Enter AWS Access Key ID:'
    aws_access_key_id = raw_input('> ')
    print 'Enter AWS Secret Access Key:'
    aws_secret_access_key = raw_input('> ')
    
    boto_conf_text = '''[Credentials]
aws_access_key_id = %s
aws_secret_access_key = %s''' % (aws_access_key_id, aws_secret_access_key)
    
    open(boto_config, 'w').write(boto_conf_text)
    print 'AWS credentials have been cached at %s\n' % (boto_config,)

os.environ['BOTO_CONFIG'] = boto_config
import boto

import fabric
from fabric.api import env,run,sudo,put
from fabric.contrib.files import exists
env.key_filename = key_path

conn = boto.connect_ec2()

def get_instances():
    instances = {}
    for reservation in conn.get_all_instances():
        for instance in reservation.instances:
            if tag_name in instance.tags and instance.state=='running':
                instances[instance.tags[tag_name]] = instance
    return instances

def print_instances():
    instances = get_instances()
    print
    print 'host  \tinternal ip \texternal ip'
    for instance_name in sorted(instances.keys()):
        instance = instances[instance_name]
        print '%s\t%s\t%s' % (instance_name, instance.private_ip_address, instance.ip_address)

def create_key_pair():
    if not conn.get_key_pair(key_name):
        key = conn.create_key_pair(key_name)
        key.save(script_path)
    else:
        print 'key pair "%s" already exists' % (key_name,)

def create_group():
    group_names =  [x.name for x in conn.get_all_security_groups()]
    if sec_group_name not in group_names:
        group = conn.create_security_group(sec_group_name, sec_group_name)
        #ssh(tcp:22) to all
        group.authorize(ip_protocol='tcp', from_port=22, to_port=22, cidr_ip='0.0.0.0/0')
    else:
        print 'security group "%s" already exists' % (sec_group_name,)

def create_instances():
    tagged_instances = 0
    for reservation in conn.get_all_instances():
        for instance in reservation.instances:
            if tag_name in instance.tags and instance.update() in ['pending','running']:
                tagged_instances += 1
    if tagged_instances == 0:
        desired_instances = 5
        res = conn.run_instances(image_id,desired_instances,desired_instances,key_name,['default',sec_group_name], user_data)
        print 'running instances'
        print 'waiting',
        while [x for x in [y.update() for y in res.instances] if x != 'running']:
            time.sleep(10)
            print '.',
        print
        for inst, tag in zip(res.instances,tags):
            inst.add_tag(tag_name,tag)
    else:
        print '%s instances with "%s" tag exist ' % (tagged_instances, sec_group_name)

def provision(filter=None):
    instances = get_instances()
    
    #generate haproxy configuration with nginx host ips
    proxied_ips = {'nginx1': instances['nginx1'].private_ip_address, 'nginx2': instances['nginx2'].private_ip_address}
    haproxy_conf_template = open('puppet/haproxy.cfg.template','r').read()
    haproxy_conf = open('puppet/haproxy.cfg','w')
    haproxy_conf.write(haproxy_conf_template % proxied_ips)
    haproxy_conf.close()
    
    try:
        for instance in instances.values():
            tag = instance.tags[tag_name].encode('ascii','ignore')
            if filter and not tag.startswith(filter):
                continue
            env.host_string = "ubuntu@"+instance.ip_address.encode('ascii','ignore')
            
            print 'waiting for user_data script to complete',
            while not exists('/root/user_data_script_complete',True):
                time.sleep(10)
                print '.',
            print
            sudo('rm -rf /root/puppet')
            put('puppet','/root/',True)
        
            if tag.startswith('nginx'):
                sudo('puppet apply /root/puppet/nginx.pp')
            
            if tag.startswith('haproxy'):
                sudo('puppet apply /root/puppet/haproxy.pp')
                
            if tag.startswith('siege'):
                sudo('puppet apply /root/puppet/siege.pp')
    finally:
        fabric.network.disconnect_all()

def terminate_instances():
    terminal_instances = []
    for reservation in conn.get_all_instances():
        for instance in reservation.instances:
            if tag_name in instance.tags:
                terminal_instances.append(instance)
                instance.terminate()
    print 'terminating instances'
    print 'waiting',
    while [x for x in [y.update() for y in terminal_instances] if x != 'terminated']:
        time.sleep(10)
        print '.',
    print

def delete_key_pair():
    conn.delete_key_pair(key_name)
    os.remove(key_path)

def delete_group():
    conn.delete_security_group(sec_group_name)   
    
if 'init' in sys.argv:
    create_key_pair()
    create_group()
    create_instances()
    
if 'provision' in sys.argv:
    provision()
    print_instances()
    
if 'teardown' in sys.argv:
    terminate_instances()
    
if 'clean' in sys.argv:
    delete_key_pair()
    delete_group()
    
if 'interact' in sys.argv or len(sys.argv) == 1:
    code.interact(local=locals())
