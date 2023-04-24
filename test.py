#!/usr/bin/python
# -*- coding: UTF-8 -*-

import telnetlib
import getpass
import sys
import time
import os
import subprocess
import paramiko 

TotalRetryTimes = 2



host = sys.argv[1]
url = sys.argv[2]
execute_times = sys.argv[3]
gateway = sys.argv[4];
user = sys.argv[5] 
pwd = sys.argv[6]
NICName = sys.argv[7]
TestResult = 0
PingResult = 0



#TxTTestResult = TestResultFile
#TxTTestResult = TxTTestResult.replace('.tst','')

def ping(address, retry, success):
	i = 0
	ok = 0
	cmd = 'ping -n 1 '+address
	print cmd
	while( i < retry):
		try:
			output = subprocess.check_output(cmd)
			if 'TTL=' in output:
				ok += 1
			if ok == success:
				print "Ping Success"
				return True
		except subprocess.CalledProcessError as e:
			code      = e.returncode
			print "Ping Error! Re-send again. [ERROR NO]: %d"%(code)
		i += 1
		time.sleep(1)

		
	print "Ping Failed !"
	#rootlogger.debug("Ping Failed !")   	
	
	return False



def send_curl_command(cmd):
	#print "SEND: "
	#print cmd

	retry = 0
	print "*** Send Command : " + cmd + "\n"
	#rootlogger.debug("*** Send Command : " + cmd + "\n")   
	
	while(retry < 2):
		try:
			output = subprocess.check_output(cmd)
			#print output
			#print '\n'
			return output
		except subprocess.CalledProcessError as e:
			code      = e.returncode
			print "Send CMD Error! Re-send again. [ERROR NO]: %d"%(code)
			#rootlogger.debug("Send CMD Error! Re-send again. [ERROR NO]: %d"%(code))  
			retry += 1
			

			
			time.sleep(5)
	return 0

	
def DoPingTest():


	# Write Test Report File
	try:
		#open(my $WF, '>>','./reports/Wan_State_Test/Wan_Ping_Report.txt') or die $!;
		f = open('./reports/IPSecVPNServer_IKEv2_WithoutDPI/Wan_Ping_Report.txt',"a+")
	except:
		print "Open File Failed"		
	#finally:
	#	if f:
	#		f.close()
	

	countOfSuccess=0
	
	# Give DUT Few Time To Connect To Server
	print "      Python Response: Sleep For Waiting Connection...\n";
	time.sleep(10);
	print "      Python Response: Wake Up ...\n";

	#ping(host, 60, 5)
	#result = send_curl_command(command)
	#print result

	print "      ----Do Ping Test----\n";
	print "      host=" + host
	print "      user=" + user
	print "      password=" + pwd



	
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		ssh.connect(host, username=user, password=pwd)
	except paramiko.SSHException:
		print "Connection Failed"
		return PingResult
		quit()


	time.sleep(10)
    
 	command = "cd C:\Users\Asus_user\Downloads\iperf-3.1.3-win64"
	print "      Python Response: " + command;	
	stdin,stdout,stderr= ssh.exec_command(command)      
    

	command = "start /min iperf3.exe -c " + url + " -i 1 -t 4800 -b 100m -p 5225 -P 10 &"
	print "      Python Response: " + command;	
	stdin,stdout,stderr= ssh.exec_command(command)   

	time.sleep(5)    
    
	command = "start /min iperf3.exe -c " + url + " -i 1 -t 4800 -b 100m -p 5226 -P 10 -R &"
	print "      Python Response: " + command;	
	stdin,stdout,stderr= ssh.exec_command(command)  

	ssh.close()
    
	from telnetlib import Telnet
	tn=Telnet(host,23,60)
	tn.read_until(b"Username:")
	tn.write(user.encode('ascii') + b"\r\n")
	tn.read_until(b"Password:")
	tn.write(pwd.encode('ascii') + b"\r\n")
	command = "start /min iperf3.exe -c " + url + " -i 1 -t 4800 -b 8m -p 5225 -P 20"
	tn.write(command.encode('ascii') + b"\r\n")
	tn.read_until("TELNET")
	tn.close()
    
	from telnetlib import Telnet
	tn=Telnet(host,23,60)
	tn.read_until(b"Username:")
	tn.write(user.encode('ascii') + b"\r\n")
	tn.read_until(b"Password:")
	tn.write(pwd.encode('ascii') + b"\r\n")
	command = "start /min iperf3.exe -c " + url + " -i 1 -t 4800 -b 8m -p 5226 -P 20 -R"
	tn.write(command.encode('ascii') + b"\r\n")
	tn.read_until("TELNET")
	tn.close()
		
def main():
	
	time.sleep(30)
	
	print ""
	print "===SSH To PC And Do PingCheck==="
	
	DoPingTest()
		

	
	
	print "      Python Response : Test Finished\n"

	#try:
	#	#open(my $WF, '>>','./reports/Wan_State_Test/Wan_Ping_Report.txt') or die $!;
	#	f = open('./reports/IPSecVPNServer_IKEv2_WithoutDPI/Wan_Ping_Report.txt',"a+")
	#except:
	#	print "Open File Failed"		
	
	#if TestResult == 1:
	#	f.write(url + "_" + wtype + "------Pass\n")	
	#elif TestResult == 0:
	#	f.write(url + "_" + wtype + "------Failed\n")

	#f.close()
	
	#time.sleep(10)
	
	#print ""
	#print "===Retry Test==="
	#Retry()

		
if __name__=='__main__':  
	main()
		
	

