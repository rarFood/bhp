import subprocess
import platform

a = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
a = [i.split(":")[1][1:-1] for i in a if "All User Profile" in i]
infile = open('wifi.txt','a')
infile.write('\n\n<<<<<<<<<<<' + platform.node() + '>>>>>>>>>>>\n\n')
# infile.write('\n\n<<<<<<<<<<<' + '>>>>>>>>>>>\n\n')
for i in a:
    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split('\n')
    results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
    print ("Fetching...")
    try:
        infile.write("{:<30}|  {:<}".format(i, results[0]) + '\n')
    except IndexError:
        infile.write("{:<30}|  {:<}".format(i, "") + '\n')
infile.close()
# a = input("Done.")
