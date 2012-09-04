#!/usr/bin/python

import sys
import paramiko
from datetime import date
from optparse import OptionParser

MONTHLY_CAP = float(250000)
DAILY_CAP = MONTHLY_CAP/30

def get_ssh_conn():
    key = paramiko.RSAKey.from_private_key_file('/var/lib/nagios/.ssh/id_rsa')
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('10.10.10.1', username='root', pkey=key)
    return ssh

def main():
    usage = get_month_usage()
    print monthly_status(usage)
                 
    
def get_month_usage(critical=0.95, warning=0.90):
    month = '%02d' % date.today().month
    year = date.today().year
   
    ssh = get_ssh_conn()
    stdin, stdout, stderr = ssh.exec_command('nvram show | grep traff-' + str(month) + '-' + str(year) + '=')
    
    output = stdout.readlines()
    
    #parse the output
    data = output[0][14:]
    days = data.split(' ')
    
    #get just the totals info in the formate (UL:DL)
    total = days[-1].replace('[','').replace(']','').replace('\n','')
    ul, dl = total.split(':')

    ssh.close()
    return monthly_status(int(ul) + int(dl), critical, warning)

def get_today_usage(critical=0.95, warning=0.90):
    month = '%02d' % date.today().month
    year = date.today().year

    ssh = get_ssh_conn()
    stdin, stdout, stderr = ssh.exec_command('nvram show | grep traff-' + str(month) + '-' + str(year) + '=')
    
    output = stdout.readlines()
    
    #parse the output
    data = output[0][14:]
    days = data.split(' ')
    
    #get just the totals info in the formate (UL:DL)
    day_of_month = date.today().day
    total = days[day_of_month - 1].replace('[','').replace(']','').replace('\n','')
    ul, dl = total.split(':')

    ssh.close()
    return daily_status(int(ul) + int(dl), critical, warning)
    
    
def monthly_status(usage, critical, warning):
    if usage > (MONTHLY_CAP * critical):
        return 'CRITICAL - Monthly Cap:%0.2fGB  Usage:%0.2fGB' % ((MONTHLY_CAP/1000.00), (usage/1000.00))
    elif usage > (MONTHLY_CAP * warning):
        return 'WARNING - Monthly Cap:%0.2fGB  Usage:%0.2fGB' % ((MONTHLY_CAP/1000.00), (usage/1000.00))
    else:
        return 'OK - Monthly Cap:%0.2fGB  Usage:%0.2fGB' % ((MONTHLY_CAP/1000.00), (usage/1000.00))

def daily_status(usage, critical, warning):
    if usage > (DAILY_CAP * critical):
        return 'CRITICAL - Daily Cap:%0.2fGB  Usage:%0.2fGB' % ((DAILY_CAP/1000.00), (usage/1000.00))
    elif usage > (DAILY_CAP * warning):
        return 'WARNING - Daily Cap:%0.2fGB  Usage:%0.2fGB' % ((DAILY_CAP/1000.00), (usage/1000.00))
    else:
        return 'OK - Daily Cap:%0.2fGB  Usage:%0.2fGB' % ((DAILY_CAP/1000.00), (usage/1000.00))

if __name__ == '__main__':
    parser = OptionParser(usage="Usage: %prog [options]",  version="%prog 1.0")
    parser.add_option('-m', '--monthly', action="store_true", dest="month", default=False,
                      help='Do Monthly Usage Check')
    parser.add_option('-d', '--daily', action="store_true", dest="day", default=False,
                      help='Do Daily Usage Check')
    parser.add_option('-c', '--critical', action='store', type='float', dest='critical', default='0.95',
                      help='Set CRITICAL level (as percent eg. 0.95)')
    parser.add_option('-w', '--WARNING', action='store', type='float', dest='warning', default='0.90',
                      help='Set WARNING level (as percent eg. 0.90)')
    (options, args) = parser.parse_args()

    output = ""
    if options.day:
        output = get_today_usage(options.critical, options.warning)
    elif options.month:
        output = get_month_usage(options.critical, options.warning)

    if len(output) < 2:
        print 'Please use -h for options'
        print options("-h")
    if output[:2] == 'OK':
        print output
        sys.exit(0)
    elif output[:2] == 'WA':
        print output
        sys.exit(1)
    elif output[:2] == 'CR':
        print output
        sys.exit(2)
        


