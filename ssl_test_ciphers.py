#!/usr/bin/env python
# Scans a remote host to display all available common TLS ciphers
# author: ccalifan@cisco.com
# history, date format ISO 8601:
#  2016-10-14: 1.0 initial version

# Import some modules
from __future__ import print_function	# print() as a function not as a statement
import argparse				# write user-friendly command-line interfaces
import os				# use operating system dependent functionalities
import subprocess			# spawn new processes, connect to their input/output/error pipes, and obtain their return codes
import sys				# variables used or maintained by the interpreter and functions that interact strongly with the interpreter

# Version number
__version__ = 1.0
__build__ = 161015

# https://svn.blender.org/svnroot/bf-blender/trunk/blender/build_files/scons/tools/
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def validIP(ipAddrs):
  # Split the input string into a list of octets
  octList = ipAddrs.split('.')
  # Must contain 4 octets
  if len(octList) != 4:
      return False
  # Each octet must be a digit AND between 0 and 255
  for x in octList:
      if not x.isdigit():
          return False
      i = int(x)
      if i < 0 or i > 255:
          return False
  return True

def main():
  parser = argparse.ArgumentParser(description='Scans <IP address>:<IP address> querying all the supported TLS ciphers, version {version}, build {build}.'.format(version=__version__, build=__build__))
  parser.add_argument('ipAdd', metavar='<IP address>', type=str, help='IP address of the host to scan for ciphers')
  parser.add_argument('whichPort', metavar='<Port number>', type=str, help='Port number, usually equals 443')
  parser.add_argument('-V', '--version', action='version', version='%(prog)s {version}'.format(version=__version__))

  # In case of no arguments print help message then exits
  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
  else:
    args = parser.parse_args() # else parse command line

  # Let's validate input
  if not validIP(args.ipAdd):
    print('Address is not a valid IPv4 one!')
    print('Exiting...', end='\n\n')
    sys.exit(2)

  if (int(args.whichPort) < 1) or (int(args.whichPort) > 65535):
    print('Port out of range!')
    print('Exiting...', end='\n\n')
    sys.exit(3)

  # If input is OK we can continue. First we fetch the output of openssl ciphers run on the local machine
  # this will give us a string with all the locally supported ciphers
  sslVer = subprocess.check_output(['openssl', 'version'])
  print('[+] ' + os.uname()[0] + ' version ' + os.uname()[2] + ' running on ' + os.uname()[4] + ' platform')
  print('[+] ' + sslVer.rstrip() + ', fetching the list of locally supported ciphers...')
  myCiphers = subprocess.check_output(['openssl', 'ciphers', 'ALL:eNULL'])
  # Transform string into a list
  lCiphers = myCiphers.rstrip('\n').split(':')
  for item in lCiphers:
    # Here we build the command string, stderr is redirected to stdout to keep output clean
    cmdstr = 'echo -n | openssl s_client -cipher ' + item + ' -connect ' + args.ipAdd + ':' + args.whichPort + ' 2>&1'
    # Send the command string to subprocess for execution
    sslout = subprocess.check_output(cmdstr, shell=True)
    if ":error:" in sslout:
      print(bcolors.FAIL + '[-] ' + item + ' NOT supported!' + bcolors.ENDC)
    else:
      print(bcolors.OKBLUE + '[+] ' + item + ' supported!!!' + bcolors.ENDC)
      
if __name__ == '__main__':
  main()
