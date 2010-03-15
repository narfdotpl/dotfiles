#!/usr/bin/env python
# encoding: utf-8
"""
Store and visualize your daily RapidShare download logs.

Example usage:

    python rapidshare_logs.py get ~/logs/rs.json myusername mypassword
    python rapidshare_logs.py plot ~/logs/rs.json
    python rapidshare_logs.py plot ~/logs/rs.json 61  # last two months

Dependencies:

  - [BeautifulSoup][]
  - [gnuplot][]

I don't know the numbers of the lowest versions that do the job, I use
BeautifulSoup 3.0.8 and gnuplot 4.2.

  [BeautifulSoup]: http://www.crummy.com/software/BeautifulSoup/
  [gnuplot]: http://www.gnuplot.info/
"""

from datetime import datetime, timedelta
import json
from os.path import expanduser, realpath
from subprocess import call
from sys import argv, stderr
from tempfile import NamedTemporaryFile
from urllib import urlencode
from urllib2 import urlopen

from BeautifulSoup import BeautifulSoup

from utils import preview, which


__author__ = 'Maciej Konieczny <hello@narf.pl>'


class InvalidLoginInformation(Exception):
    pass


def _get_html(username, password):
    """
    Try to login to a premium RapidShare account and return received html.
    """

    url = 'https://ssl.rapidshare.com/cgi-bin/premiumzone.cgi'
    data = urlencode({
        'login': username,
        'password': password,
        'showlogs': 1
    })
    response = urlopen(url, data)
    return ''.join(response.readlines())


def _get_logs_from_file(path):
    try:
        with open(path) as f:
            return json.load(f)
    except IOError:  # except file does not exist
        return {}


def _get_logs_from_web(username, password):
    """
    Return {date: size} dictionary (in {'yyyy-mm-dd': int} format) of
    number of kilobytes downloaded in given day.
    """

    # get html
    html = _get_html(username, password)
    if 'Forgotten your password?' in html:
        raise InvalidLoginInformation()

    # "Gentlemen, please take your marks!"
    get_string_attr = lambda tag: getattr(tag, 'string', None)
    logs = {}

    # parse logs from html table
    soup = BeautifulSoup(html)
    for tr in soup.body.find('table', 'dtabelle')('tr'):
        try:
            date_str, dummy, size_str = map(get_string_attr, tr)
            date = datetime.strptime(date_str, '%a, %d. %b %Y') \
                   .date().isoformat()
            size = int(size_str.split()[0])
        except ValueError:  # not a three column row or not a valid date or...
            pass            # ...size string
        else:
            logs[date] = logs.get(date, 0) + size

    return logs


def _plot(logs, last_x_days=None):
    """
    Create a PNG plot showing downloads from `last_x_days` or since the
    first day in the log file.
    """

    # last_x_days can be either a positive number or None
    if last_x_days is not None:
        last_x_days = int(last_x_days)
        if last_x_days <= 0:
            raise ValueError()

    # configure gnuplot
    png = '/tmp/rapidshare.png'
    config = """
        set term png
        set output "{0}"

        set title "RapidShare downloads"
        set xlabel "days"
        set ylabel "gigabytes"

        set xdata time
        set timefmt "%Y-%m-%d"
        set format x "%m-%d"

        set grid
        set nokey
        set style data boxes
        set style fill solid 0.3
    """.format(png)

    # make tomorrow the last day in the plot (empty)
    one_day = timedelta(days=1)
    tomorrow = datetime.now().date() + one_day

    # choose the first day in the plot
    if last_x_days:
        date = tomorrow - timedelta(days=last_x_days)
    else:
        first = min(logs.iterkeys())
        date = datetime.strptime(first, '%Y-%m-%d').date()
    date -= one_day

    # save date range in config
    config += 'set xrange ["{0}":"{1}"]\n'.format(date, tomorrow)

    # save logs in a temporary file in gnuplot-compatible format
    with NamedTemporaryFile() as data:
        while date < tomorrow:
            # set size to zero for days that are not in logs
            size = logs.get(date.isoformat(), 0) / 1e6  # GB
            data.write('{0}\t{1}\n'.format(date, size))
            date += one_day
        data.flush()

        # save gnuplot config and plotting instructions in a temporary file
        with NamedTemporaryFile() as gnuplot:
            gnuplot.write(config)
            gnuplot.write('plot "{0}" using 1:2 lt 3'.format(data.name))
            gnuplot.flush()

            # run gnuplot
            call('cat "{0}" | gnuplot'.format(gnuplot.name), shell=True)

    # try to open PNG
    if which('qlmanage'):
        preview(png)
    elif which('open'):
        call('open ' + png, shell=True)
    else:
        print 'see ' + png


def update(d1, d2):
    """
    If dictionary d1 can be updated by d2, update it and return True.
    Otherwise return False.
    """

    k1 = set(d1.keys())
    k2 = set(d2.keys())

    # check for new keys
    if k2 - k1:
        d1.update(d2)
        return True

    # check for new values of old keys
    for key in k2:
        if d1[key] != d2[key]:
            d1.update(d2)
            return True

    return False


def usage():
    # strip preceding and trailing \n
    return __doc__[1:-1]


def _main():
    # parse command-line arguments
    args = argv[1:]
    try:
        action = args.pop(0)
        path = realpath(expanduser(args.pop(0)))
    except IndexError:
        print >> stderr, usage()
        exit(1)

    # act!
    if action == 'get':
        # parse username and password
        try:
            username = args.pop(0)
            password = args.pop(0)
        except IndexError:
            print >> stderr, usage()
            exit(1)

        # get logs
        filelogs = _get_logs_from_file(path)
        try:
            weblogs = _get_logs_from_web(username, password)
        except InvalidLoginInformation:
            print >> stderr, 'Invalid username or password.'
            exit(1)

        # update and save filelogs
        if update(filelogs, weblogs):
            with open(path, 'w') as f:
                json.dump(filelogs, f, sort_keys=True, indent=2)

    elif action == 'plot':
        # parse number of days
        try:
            last_x_days = args.pop(0)
        except IndexError:
            last_x_days = None

        # plot filelogs
        logs = _get_logs_from_file(path)
        try:
            _plot(logs, last_x_days)
        except ValueError:
            print >> stderr, 'Number of days has to be a number (sic!) ' \
                             'greater than zero.'
            exit(1)

    else:
        print >> stderr, "Unknown action '{0}'.".format(action)
        exit(1)

if __name__ == '__main__':
    _main()
