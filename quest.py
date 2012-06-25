import sys, os

# Obtain AWS credentials from user or cache on future invocations
boto_config = os.path.join(sys.path[0], 'boto.conf')
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
print conn