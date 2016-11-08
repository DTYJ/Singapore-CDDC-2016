# Singapore-CDDC-2016
Crappy code that ~~actually~~ perhap works.

copynpaste.py is a simple and ugly script that was hack together quickly to take in a list of ip addresses (serveripaddr.txt) and hits the SSH which are enabled on that list using a set of predefined default username and password. Attempts which are successful will result in a few simple foothold establishment measures.

 * Adding SSH public key to compromised server
 * Setting of 'i' attribute to the public key file
 * Adds an unsuspecting user

> who doesn't like to auto pwn users who do not change their password?
