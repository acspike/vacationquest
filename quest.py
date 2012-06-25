import sys, os, time

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

conn = boto.connect_ec2()

#setup
# - create key pair
# - run instances
# - tag instances
# - create security goups
# - assign security groups
# - base configuration
if 'setup' in sys.argv:
    if not conn.get_key_pair(key_name):
        key = conn.create_key_pair(key_name)
        key.save(script_path)
    else:
        print 'key pair "%s" already exists' % (key_name,)

    group_names =  [x.name for x in conn.get_all_security_groups()]
    if sec_group_name not in group_names:
        group = conn.create_security_group(sec_group_name, sec_group_name)
        #ssh(tcp:22) to all
        group.authorize(ip_protocol='tcp', from_port=22, to_port=22, cidr_ip='0.0.0.0/0')
    else:
        print 'security group "%s" already exists' % (sec_group_name,)
        
    tagged_instances = 0
    for reservation in conn.get_all_instances():
        for instance in reservation.instances:
            if tag_name in instance.tags and instance.update() in ['pending','running']:
                tagged_instances += 1
    if tagged_instances == 0:
        res = conn.run_instances(image_id,5,5,key_name,['default',sec_group_name])
        while [x for x in [y.update() for y in res.instances] if x != 'running']:
            time.sleep(10)
            print '.',
        print
        for inst, tag in zip(res.instances,tags):
            inst.add_tag(tag_name,tag)
    else:
        print '%s instances with "%s" tag exist ' % (tagged_instances, sec_group_name)
        
#test
# - test base config
# - tune and test; repeat
if 'test' in sys.argv:
    pass

#teardown
# - terminate instances
# - delete keypair
# - delete security groups
if 'teardown' in sys.argv:
    terminal_instances = []
    for reservation in conn.get_all_instances():
        for instance in reservation.instances:
            if tag_name in instance.tags:
                terminal_instances.append(instance)
                instance.terminate()
    while [x for x in [y.update() for y in terminal_instances] if x != 'terminated']:
        time.sleep(10)
        print '.',
    print
    
    #conn.delete_key_pair(key_name)
    #conn.delete_security_group(sec_group_name)