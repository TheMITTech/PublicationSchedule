###############################################################################
# 
# File Name: adscal.py
# 
# Current owner: Greg Steinbrecher (steinbrecher@alum.mit.edu)
# Last Modified Time-stamp: <2012-06-24 18:12:39 gstein>
# 
# Created by: Greg Steinbrecher (steinbrecher@alum.mit.edu)
# Created on: 2012-06-24 (Sunday, June 24th, 2012)
# 
###############################################################################
"""Module to output advertising calendar for The Tech in HTML format.

Defines the class AdsHTMLCalendar as a subclass of calendar.HTMLCalendar and
provides modified methods to associate publication dates with an appropriate
CSS class. 
"""

import calendar
import datetime as dt

class AdsHTMLCalendar(calendar.HTMLCalendar):
    def __init__(self, firstweekday, pub_dates):

        super(AdsHTMLCalendar, self).__init__(firstweekday)

        self.pub_dates = pub_dates

        self.year_table_header = '<table class="year">'
        self.month_table_header = '<table class="month">'

        self.day_name = calendar._localized_day('%A')
        self.day_abbr = ['M', 'T', 'W', 'T', 'F', 'S', 'S']

    def make_key_cell(self):
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
        # Pad with space if neccesary
        if css_class != '':
            if css_class[0] != ' ': css_class = ' %s' % css_class
            
        if day == 0:
            return '<td class="month noday%s">&nbsp;</td>' % css_class
        else:
            css_class = '%s%s%s' % ('month ', self.cssclasses[week_day], css_class)
            return '<td class="%s">%d</td>' % (css_class, day)
    
    def read_date_file(self, date_file):
        for line in open(date_file, 'r-'):
            (year, month, day) = [int(x) for x in line.strip().split('-')]
            date = dt.date(year, month, day)
            if not self.pub_dates.has_key(date):
                self.pub_dates[date] = 'issue'
        
        
            


if __name__ == '__main__':
    special_issues = {dt.date(2012, 6, 8): 'special',
                      dt.date(2012, 8, 24): 'special',
                      dt.date(2012, 8, 28): 'special',
                      dt.date(2012, 8, 31): 'special',
                      }
    ads_cal = AdsHTMLCalendar(6, special_issues)
    ads_cal.read_date_file('pubdates.txt')
    print '<html>\n<head>'
    print '<link rel="stylesheet" type="text/css" href="adscalstyle.css"'
    print '</head>'
    print '<title>Test Ads Calendar</title>'
    print '<body>'
    #print ads_cal.formatmonth(2012, 6, False)
    print ads_cal.formatarb(start_year=2012, start_month=2,
                            stop_year=2013, stop_month=4, width=2)
    print '</body>\n</html>'

