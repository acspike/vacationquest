#!/usr/bin/env python
import virtualenv, textwrap

python_version='2.7'
pywin32_build = '217'

packages = '''Fabric==1.4.2
boto==2.5.2
distribute==0.6.27
pycrypto==2.6
ssh==1.7.14
virtualenv==1.7.2'''

extra_text = textwrap.dedent("""
import os, subprocess, struct, urllib

def adjust_options(options, args):
    #default to a subdirectory
    if not args:
        args.append('venv')

def after_install(options, home_dir):
    packages = '''%s'''.split()
    
    if sys.platform == 'win32':
        bin = 'Scripts'
        
        if 8 * struct.calcsize("P") == 64:
            arch = '-amd64'
        else:
            arch = '32'
        url = 'http://downloads.sourceforge.net/project/pywin32/pywin32' \
                '/Build%%%%20%s/pywin%%s-%s.win32-py%s.exe' %% (arch,)
        pywin32_installer = join(home_dir, 'pywin32.exe')
        urllib.urlretrieve(url, pywin32_installer)
        subprocess.call([join(home_dir, bin, 'easy_install'), pywin32_installer])
    else:
        bin = 'bin'
        
    for package in packages:
        subprocess.call([join(home_dir, bin, 'pip'), 'install', package])
""" % (packages, pywin32_build, pywin32_build, python_version))


output = virtualenv.create_bootstrap_script(extra_text, python_version=python_version)
f = open('bootstrap.py', 'w').write(output)