#!/usr/bin/python2.7

import os
import sys
import re
from datetime import datetime, timedelta
import errno
from collections import Counter
import hashlib


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'



def read_file(filename, date):

    with open(filename) as f:
        content = f.readlines()

    output = []

    regex_date = re.compile(date, flags=0)

    for line in content:
            matches_date = re.search(regex_date, line)
            output.append(matches_date)

    return output


def main():

    filename = '/data/log/syslogng_ems_event.log'
#    filename = '/tmp/test'
#    d = datetime.today() - timedelta(1)
    date = datetime.today().strftime("%b %d")
#    date = d.strftime("%b %d")
    regex_date = "<[1-9]+>" + date + " (.)*"
    new_regex_date = regex_date.replace('0',' ')

    log_lines = []

    for line in read_file(filename, new_regex_date):
        if line:
            log_lines.append(line.group())

    hosts = []
    alerts = []
    dict_alerts = []

    for line in log_lines:
        host = line.split()[3]
        hosts.append(host)
        raw_alert = line.split(']:')[1]
        alert = re.search(' (.)*;', raw_alert).group(0).lstrip()
        alerts.append(alert)
        dict_alerts.append([host, alert])

    msgs_per_host = Counter(hosts).most_common()
    total_msgs = sum(Counter(hosts).values())

    lista = []


    for j in set(hosts):

        report = []
        alerts_per_host = []

        for i in dict_alerts:
            if i[0] == j:
                alerts_per_host.append(i[1])
                alertas = Counter(alerts_per_host).most_common()
                report.append([i[0],alertas])

        lista.append(report.pop())

#    print color.BOLD + "\nReport date: " + date.strftime("%Y/%b/%d") + color.END
    print color.BOLD + "\nReport date: " + datetime.today().strftime("%b-%d-%Y") + color.END
    print color.BOLD + "\nSummary:" + color.END
    print color.BOLD + "Host\t\tMessages" + color.END
    for i in msgs_per_host:
        print i[0] + "\t(" + str(i[1]) + ")"

    print color.BOLD + "Total messages\t" + color.END + str(total_msgs)
    print color.BOLD + "Total hosts\t" + color.END + str(len(set(hosts)))
    print "\n"

    for i in lista:
        print color.BOLD + "* " + color.UNDERLINE + i[0] + ":" + color.END + color.END
        for j in i[1]:
            print "- (" + str(j[1]) + ")" + j[0]

    print "\n"

if __name__ == '__main__':
        main()
