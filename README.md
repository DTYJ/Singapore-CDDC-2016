# Singapore-CDDC-2016
Crappy code that actually works.

automate.py is a simple and ugly script that takes in a list of ip addresses (serveripaddr.txt) and hits the SSH which are enabled on that list using a set of predefined default username and password. Attempts which are successful will result in a few simple foothold establishment measures.

 * Adding SSH public key to compromised server
 * Setting of 'i' attribute to the public key file
 * Adds an unsuspecting user

