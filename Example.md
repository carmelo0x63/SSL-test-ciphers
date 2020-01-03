A security scan turned up two SSH vulnerabilities:
```
SSH Server CBC Mode Ciphers Enabled
SSH Weak MAC Algorithms Enabled
```

To correct this problem I changed the /etc/sshd_config file to:
```
# default is aes128-ctr,aes192-ctr,aes256-ctr,arcfour256,arcfour128,
# aes128-cbc,3des-cbc,blowfish-cbc,cast128-cbc,aes192-cbc,
# aes256-cbc,arcfour
# you can removed the cbc ciphers by adding the line

Ciphers aes128-ctr,aes192-ctr,aes256-ctr,arcfour256,arcfour128,arcfour

# default is hmac-md5,hmac-sha1,hmac-ripemd160,hmac-sha1-96,hmac-md5-96
# you can remove the hmac-md5 MACs with

MACs hmac-sha1,hmac-ripemd160
```

Once that was done and sshd was restart, you can test for the issue like this:
```
#ssh -vv -oCiphers=aes128-cbc,3des-cbc,blowfish-cbc <server>
#ssh -vv -oMACs=hmac-md5 <server>
```

Best to test before and after so you are familiar with the output.
