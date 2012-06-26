Learning some new technologies on vacation

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