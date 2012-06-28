Learning some new technologies on vacation

**quest.sh**

a single command to bootstrap a virtualenv and execute quest.py 
inside of that environment to create and provision servers

You will be prompted for your AWS credentials on the first 
invocation. Afterward they will be cached in boto.conf.

Assumes the availability of python, its associated development 
libraries and a functional c compiler


**bootstrap.py**

manually bootstrap an appropriate virtualenv inside of the repo


**make-bootstrap.py**

regenerate bootstrap.py script


**quest.py**

execute quest.py from the containing directory

quest.py should be followed by a list of tasks to perform.
The order of the task names on the command line is
insignificant. The tasks are always performed in the 
following order:

init
	generates a key pair
	configures a security group to allow external ssh access
	runs ec2 instances
provision
	uploads configuration data and provisions servers with puppet
teardown
	terminates ec2 instances
clean
	deletes key pair and security group

optionally you can specify 'interact' to drop into an interactive 
python shell. If no tasks are specified 'interact' is the default.

Requirements:
	python
	boto
	fabric (paramiko, pycrypto)