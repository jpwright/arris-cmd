import requests
from bs4 import BeautifulSoup
import mechanize
import sys
import json
import os

import socket
import fcntl
import struct

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

br = mechanize.Browser()
br.set_handle_equiv(True)
br.set_handle_gzip(False)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

def login():
	if (os.path.isfile('login.txt')):
		with open('login.txt') as login:
			lines = login.readlines()
		username = lines[0].strip()
		password = lines[1].strip()
		get_response = requests.get(url='http://10.0.0.1')
		post_data = {'username': username, 'password': password}
		post_response = requests.post(url='http://10.0.0.1/home_loggedout.php', data=post_data)
	else:
		print 'warning: login failed. make sure your login.txt is correct'

def connected_devices():
	br.open('http://10.0.0.1')
	data = br.response()
	soup = BeautifulSoup(data)
	internet_usage = soup.find('div', {'id': 'internet-usage'})
	internet_usage_soup = BeautifulSoup(internet_usage.encode('utf-8').strip())
	rows = internet_usage_soup.findAll('div', {'class': 'form-row'})
	for row in rows:
		print row.text
		
def port_forwarding(alter):

	try:
		local_ip = get_ip_address('eth0')
	except:
		try:
			local_ip = get_ip_address('eth1')
		except:
			try:
				local_ip = get_ip_address('eth2')
			except:
				return 'Network interfaces all broken'
				
	print 'Local ip is '+local_ip

	br.open('http://10.0.0.1/port_forwarding.php')
	data = br.response()
	soup = BeautifulSoup(data)
	rows = soup.findAll('tr')
	rows = rows[1:]
	sshOK = False
	httpOK = False
	nothttpOK = False
	for row in rows:
		row_soup = BeautifulSoup(row.encode('utf-8').strip())
		cols = row_soup.findAll('td')
		name = cols[0].text
		ip = cols[4].text
		link = BeautifulSoup(cols[5].encode('utf-8').strip()).find('a')['href']
		index = link.split('=')[1].strip()
		
		print name + ' on port ' + cols[2].text + '-' + cols[3].text + ' forwards to ' + ip
		if alter:
			if (name == 'ssh'):
				if (ip != local_ip):
					print 'ssh ip is wrong, changing it now...'
					#deletePort(index)
					#updatePort(index, 'ssh', '22')
					sshOK = True
				else:
					print 'ssh ip is correct'
					sshOK = True
			if (name == 'http'):
				if (ip != local_ip):
					print 'http ip is wrong, changing it now...'
					deletePort(index)
					updatePort('http', '80', local_ip)
					httpOK = True
				else:
					print 'http ip is correct'
					httpOK = True
			if (name == 'nothttp'):
				if (ip != local_ip):
					print 'nothttp ip is wrong, changing it now...'
					deletePort(index)
					updatePort('nothttp', '690', local_ip)
					nothttpOK = True
				else:
					print 'nothttp ip is correct'
					nothttpOK = True
				
	if alter:
		if not sshOK:
			print 'no ssh port forwarding exists, adding it now...'
			#updatePort('ssh', '22', local_ip)
			ignore = 'me'
		if not httpOK:
			print 'no http port forwarding exists, adding it now...'
			updatePort('http', '80', local_ip)
		if not nothttpOK:
			print 'no nothttp port forwarding exists, adding it now...'
			updatePort('nothttp', '690', local_ip)

			
def deletePort(index):
	get_response = requests.get(url='http://10.0.0.1/port_forwarding.php?&delete='+index)
	#print get_response

def updatePort(name, port, ip):
	ip_comps = ip.split('.')
	post_data = {'common_services': 'other', 'other_service': name, 'sevice_type': '3', 'server_ip_address_1': ip_comps[0], 'server_ip_address_2': ip_comps[1], 'server_ip_address_3': ip_comps[2], 'server_ip_address_4': ip_comps[3], 'start_port': port, 'end_port': port}
	
	#print post_data
	post_response = requests.post(url='http://10.0.0.1/port_forwarding_add.php', data=post_data)
	#print post_response.text
				
if __name__ == "__main__":

	if len(sys.argv) < 2:
		print 'usage: arris {devices|ports|ports-update}'
	else:
		login()
		
		if sys.argv[1] == 'devices':
			connected_devices()
		if sys.argv[1] == 'ports':
			port_forwarding(False)
		if sys.argv[1] == 'ports-update':
			port_forwarding(True)
