###############################################################################
#
# File Name: adscal.py
#
# Current owner: Greg Steinbrecher (steinbrecher@alum.mit.edu)
# Last Modified Time-stamp: <2015-02-03 20:15:09 gstein>
#
# Created by: Greg Steinbrecher (steinbrecher@alum.mit.edu)
# Created on: 2012-06-24 (Sunday, June 24th, 2012)
#
# Modified by: Karleigh Moore (kjmoore@mit.edu, kjmoore@alum.mit.edu eventually)
# Modified on: 2017-11-08 (Wednesday, November 8, 2017)
# Modification comments: We no longer publish Tues/Fri ==> we do Thurs only + special issues.
#
###############################################################################
"""Module to output advertising calendar for The Tech in HTML format.

Defines the class AdsHTMLCalendar as a subclass of calendar.HTMLCalendar and
provides modified methods to associate publication dates with an appropriate
CSS class.
"""

import calendar
import datetime as dt
import argparse

class AdsHTMLCalendar(calendar.HTMLCalendar):
    def __init__(self, firstweekday, pub_dates={}):

        super(AdsHTMLCalendar, self).__init__(firstweekday)

        self.pub_dates = pub_dates

        self.year_table_header = '<table class="year">'
        self.month_table_header = '<table class="month">'

        self.day_abbr = ['M', 'T', 'W', 'T', 'F', 'S', 'S']

    def read_date_file(self, date_file):
        """Read file with list of dates and generate dictionary
        """
        for line in open(date_file, 'r-'):
            s = line.strip().split('/')
            date_str = s[0]

            if len(s) == 2:
                kind = s[1]
            else:
                kind = 'issue'

            (year, month, day) = [int(x) for x in date_str.split('-')]
            date = dt.date(year, month, day)
            if not self.pub_dates.has_key(date):
                self.pub_dates[date] = kind

    def date_list(self):
        """Prints the current date list in the format it likes to read it.

        In conjunction with the add_thurs method, makes it easy to generate
        a text file with too many days, remove the days we aren't
        publishimg and reload the modified text file. Way faster than typing
        them all in by hand.
        """
        out = []
        for key in sorted(self.pub_dates.iterkeys()):
            (year, month, day) = (key.year, key.month, key.day)
            out.append('%s-%s-%s/%s' % (year, month, day, self.pub_dates[key]))
            out.append('\n')
        return ''.join(out)

    def add_thurs(self, year, month):
        """ Add all Thursdays in a given month to the calendar"""
        weeks = self.monthdays2calendar(year, month)
        for week in weeks:
            for (month_day, week_day) in week:
                if month_day > 0:
                    if (week_day == 3):
                        self.pub_dates[dt.date(year, month, month_day)] = 'issue'


    def make_key_cell(self):
        """Makes the "Issue/Special Issue" key to be put in the upper left cell.
        """
        out = []
        app = out.append

        app('<td id="keycell">\n')
        app('<table id="key">')
        app('<tr><td>')
        app('<span id="issuekey">&#9632;</span>')
        app('&nbsp;issue dates</td></tr>')
        app('<tr><td>')
        app('<span id="specialkey">&#9632;</span>')
        app('&nbsp;special issues</td></tr>')

        app('</table>\n</td>')
        return ''.join(out)

    def formatarb(self, start_year, start_month, stop_year, stop_month, width=2):
        """Returns a multiline string containing the full HTML table of this
        publication schedule.
        """
        out = []
        app = out.append
        width = int(max(width,1))

        app(self.year_table_header)
        app('\n<tr>\n')

        for year in xrange(start_year, stop_year+1):
            app('<tr class="year"><th colspan="%d" class="year">%s</th></tr>' % (width, year))
            app('\n')
            if year == start_year:
                app(self.make_key_cell())
                col = 2 # Column state tracker
                first_month = start_month
            else:
                first_month = 1
                col = 1

            if year == stop_year:
                final_month = stop_month
            else:
                final_month = 12

            for month in xrange(first_month, final_month+1):
                if col == 2:
                    app('\n<td class="year">')
                    app(self.formatmonth(year, month, withyear=False))
                    app('</td>\n</tr>')
                    col = 1
                else:
                    app('<tr>\n<td class="year">')
                    app(self.formatmonth(year,month, withyear=False))
                    app('</td>')
                    col = 2

            if col == 2:
                app('<td></td>\n</tr>')
        app('</table>')
        return ''.join(out)

    def formatyear(self, year, start_month=1, end_month=12, width=2):
        """Returns a multiline string containing an HTML table of tables
        """
        out = []
        width = int(max(width, 1))
        app = out.append

        app(self.year_table_header)
        app('\n')
        app('<tr><th colspan="%d" class="year">%s</th></tr>' % (width, year))
        app('\n')
        for i in range(start_month-1, end_month+1, width):
            months = range(i, min(i+width, 13))
            app('<tr class="year">')
            for m in months:
                if m == (start_month - 1):
                    app(self.key_cell)
                else:
                    app('<td class="year">')
                    app(self.formatmonth(year, m, withyear=False))
                    app('</td>')
            if (((end_month - start_month) % 2) == 1) and (i == end_month):
                app('<td></td>')
            app('</tr>')


        app('</table>')
        return ''.join(out)


    def formatmonth(self, year, month, withyear=True):
        """Returns a multiline string contianing an HTML-formatted month.
        """

        html_list = []
        app = html_list.append

        app(self.month_table_header)
        app('\n')
        app(self.formatmonthname(year, month, withyear=withyear))
        app('\n')
        app(self.formatweekheader())
        app('\n')

        # monthdays2calendar returns list of weeks where each week is a list of
        # (month_day, week_day) pairs with month_day=0 for any day of a given
        # week that isn't a member of the month.
        for week in self.monthdays2calendar(year, month):
            app(self.formatweek(year, month, week))
            app('\n')

        app('</table>')
        app('\n')
        return ''.join(html_list)

    def formatweek(self, year, month, week):
        """Returns a string containing a week formatted as a HTML table row
        """
        out_list = []
        out_list.append('<tr class="month">')
        for (month_day, week_day) in week:
            if month_day > 0:
                day = dt.date(year, month, month_day)
                if day in self.pub_dates.keys():
                    out_list.append(self.formatday(month_day, week_day,
                                                    css_class=self.pub_dates[day]))
                else:
                    out_list.append(self.formatday(month_day, week_day))
            else:
                out_list.append(self.formatday(month_day, week_day))
        return ''.join(out_list)

    def formatweekday(self, day):
        """Returns a string containing a table header with day abbreviation
        """
        return '<td class="%s%s">%s</th>' % ('month dayname ', self.cssclasses[day],
                                             self.day_abbr[day])

    def formatday(self, day, week_day, css_class=''):
        """Slight modification of built in method to handle adding CSS to a day
        """
        if css_class != '':
            if css_class[0] != ' ': css_class = ' %s' % css_class

        if day == 0:
            return '<td class="month noday%s">&nbsp;</td>' % css_class
        else:
            css_class = '%s%s%s' % ('month ', self.cssclasses[week_day], css_class)
            return '<td class="%s">%d</td>' % (css_class, day)


def print_dates(startMonth, startYear, endMonth, endYear, tues=True, fri=True):
    adsCal = AdsHTMLCalendar(6)
    for year in xrange(startYear, endYear+1):
        if year != endYear:
            lastMonth = 12
        else:
            lastMonth = endMonth
        for month in xrange(startMonth, lastMonth+1):
            adsCal.add_thurs(year,month)
    print adsCal.date_list()

def print_html(startMonth, startYear, endMonth, endYear):
    adsCal = AdsHTMLCalendar(6)
    adsCal.read_date_file('pubdates.txt')

    print '<link rel="stylesheet" type="text/css" href="/css/adscalstyle.css">'
    print adsCal.formatarb(start_year=startYear, start_month=startMonth,
                            stop_year=endYear, stop_month=endMonth, width=2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ads Calendar Tool')
    parser.add_argument('-s', '--start-month', metavar='startmonth',
                        help="Starting month", type=int, required=True)
    parser.add_argument('-e', '--end-month', metavar='endmonth',
                        help="Ending month", type=int, required=True)
    parser.add_argument('-S', '--start-year', metavar='startyear',
                        help="Starting year", type=int, required=True)
    parser.add_argument('-E', '--end-year', metavar='endyear',
                        help="Ending year (if not included, assumed same as starting)", type=int)
    parser.add_argument('-d', '--print-dates', action='store_true',
                        help="Print list of dates in date range rather than calendar HTML")

    args = parser.parse_args()
    endYear = args.end_year
    if endYear is None:
        endYear = args.start_year
    if args.print_dates:
        print_dates(args.start_month, args.start_year, args.end_month, endYear)
    else:
        print_html(args.start_month, args.start_year, args.end_month, endYear)


