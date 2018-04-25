# Programmer: rarFood
#
# This is a simple program that takes the list output of a masscan and converts it into
# targeted nmap commands for each target in the masscan output file
#
# usage: python massParser.py <masscan output list>
import sys
import os
# import argparse # future proofing my code

def create_lists(l):
    l.sort() # sort
    l.pop(0) # remove '#end'
    l.pop(0) # remove '#masscan'

    n = [] # empty list to fill it with splited version
    tcp = [] # empty list for tcp entries
    udp = [] # empty list for udp entries

    for i in l:
        n.append(i.split())

    for i in n: # separate into tcp and udp targe lists
        if i[1] == "tcp" :
            tcp.append(i)
        else :
            udp.append(i)

    return tcp, udp

def create_dict(tcp, udp): # this function creates target dictionaries for udp and tcp targets
    targetsTcp = {} # empty dictionary
    targetsUdp = {} # empty dictionary
    if len(tcp)!=0: # check to see if there are any tcp targets
        ips = []
        for i in tcp:
            ips.append(i[3])
        ips = sorted(set(ips)) # sort and remove duplicates from targets

        targetsTcp = {}.fromkeys(ips,0) # create the dictionary

        for i in ips:
            lst = []
            for x in tcp :
                if i == x[3]: # look for every port with matching target
                    lst.append(int(x[2])) # create a list for each target
            lst.sort() # sort the ports
            for m in range(len(lst)): # convert them into strings
                lst[m] = str(lst[m])
            targetsTcp[i]=lst # port lists to dictionary for each target

    if len(udp) != 0 : # does the same as the abover but for udp
        ips = []
        for i in udp:
            ips.append(i[3])
        ips = sorted(set(ips))

        targetsUdp = {}.fromkeys(ips,0)

        for i in ips:
            lst = []
            for x in udp :
                if i == x[3]:
                    lst.append(int(x[2]))
            lst.sort()
            for m in range(len(lst)):
                lst[m] = str(lst[m])
            targetsUdp[i]=lst

    return targetsTcp, targetsUdp # return both dictionaries

def command_tcp(dict): # empty function just in case i want to separate them
    pass

def command_upd(dict): # # empty function just in case i want to separate them
    pass

def parse_masscan(file) : # function to print out the nmap commands for each target, only using open ports according to masscan
    infile = open(file,'r')
    l = []
    for line in infile :
        l.append(line)

    tcp, udp = create_lists(l) # call the create_list() function
    targetsTcp, targetsUdp = create_dict(tcp,udp) # call the create_dict(function)

    if len(targetsTcp) != 0: # check to see if there are any targets with open tcp ports
        script = []
        for i in targetsTcp.keys(): # check the ports for each target and create the ports string for the nmap command
            ports = ""
            for x in targetsTcp[i]:
                ports += str(x) + ","
            script.append("nmap -sV -sS -Pn -O -vv -oA NMAP-TCP-" + str(i) + " -p " + ports[:-1] + " " + i)
        print "#"+ "<"*10 + "--- TCP Targets ---" + ">"*10
        outFile = open('nmap-TCP-' + str(sys.argv[1])[-6][:2] +".sh", 'w' )
        for string in sorted(script, key = len): # print out the nmap commands for each target
            print string
            outFile.write(string)
        os.system('chmod +x ' + 'nmap-TCP-' + str(sys.argv[1])[-6:][:2] +".sh")
        outFile.close()
    else : # if there are no targets
        print "# No targets for TCP "

    if len(targetsUdp) != 0 : # does the exact same thing as the above block but for udp targets
        script = []
        for i in targetsUdp.keys():
            ports = ""
            for x in targetsUdp[i]:
                ports += str(x) + ","
            script.append("nmap -sV -sU -Pn -vv -oA NMAP-UDP-"+ str(i) + " -p " + ports[:-1] + " " + i)
        print "#"+ "<"*10 + "--- UDP Targets ---" + ">"*10
        outFile = open('nmap-UDP-' + str(sys.argv[1])[-6:][:2] +".sh", 'w' )
        for string in sorted(script, key= len):
            print string
            outFile.write(string)
        os.system('chmod +x ' + 'nmap-UDP-' + str(sys.argv[1])[-6:][:2] +".sh")
        outFile.close()
    else:
        print "# No targets for UDP"


parse_masscan(str(sys.argv[1])) # call the function
