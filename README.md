https://the-tech.mit.edu/mediawiki/index.php/Publication_Schedule

=How to Update the Publication Schedule=

1. Check out the git repository adscal:

<code>$ git clone [username]@the-tech.mit.edu:/srv/git/adscal.git</code>
or, from your account on tt:

<code>
$ git clone /srv/git/adscal.git
$ cd adscal
</code>
or clone from this repo...

2. Modify pubdates.txt to add the new dates. The format should be pretty clear from the file:
<code>
$ tail pubdates.txt

2015-4-14/issue

2015-4-17/special

2015-4-24/issue

2015-4-28/issue

2015-5-1/issue

2015-5-5/issue

2015-5-8/issue

2015-5-12/issue

2015-6-5/special

2015-6-12/issue

</code>
Note that you can make your job somewhat easier with adscal.py. If you give it a date range in the following way, it'll spit out all the Tuesdays and Fridays in that range:

<code>
$ python adscal.py -h
usage: adscal.py [-h] -s startmonth -e endmonth -S startyear [-E endyear] [-d]
</code>

Ads Calendar Tool
<code>
optional arguments:
  -h, --help            show this help message and exit
  -s startmonth, --start-month startmonth
                        Starting month
  -e endmonth, --end-month endmonth
                        Ending month
  -S startyear, --start-year startyear
                        Starting year
  -E endyear, --end-year endyear
                        Ending year (if not included, assumed same as
                        starting)
  -d, --print-dates     Print list of dates in date range rather than calendar
                        HTML
</code>
<code>
$ python adscal.py -s 1 -e 2 -S 2015 -d

2015-1-2/issue

2015-1-6/issue

2015-1-9/issue

2015-1-13/issue

2015-1-16/issue

2015-1-20/issue

2015-1-23/issue

2015-1-27/issue

2015-1-30/issue

2015-2-3/issue

2015-2-6/issue

2015-2-10/issue

2015-2-13/issue

2015-2-17/issue

2015-2-20/issue

2015-2-24/issue

2015-2-27/issue

</code>

<code>
$ python adscal.py -s 1 -e 2 -S 2015 -d --no-tuesdays

2015-1-2/issue

2015-1-9/issue

2015-1-16/issue

2015-1-23/issue

2015-1-30/issue

2015-2-6/issue

2015-2-13/issue

2015-2-20/issue

2015-2-27/issue

</code>

It prints this output to the terminal, so you'll want to pipe it to the end of the current pubdates file: (''Note the use of two > symbols; using only one will overwrite the file!'')
<code>
$  python adscal.py -s 1 -e 2 -S 2015 -d >> pubdates.txt
</code>
At this point, you'll need to edit the file, removing dates we don't publish on (holidays etc. -- check the academic calendar!) and changing the appropriate '/issue' designations to '/special'

3. Generate the new HTML file. Super easy; uses the same python script as before; this time just don't include the '-d' flag. You can tune the date range as before, but you can't control Tuesday/Friday inclusion; it'll put in whatever's in pubdates.txt

Pipe it to adscal.html, overwriting this time:

<code>
$ python adscal.py -s 1 -e 2 -S 2015 > adscal.html
</code>
**perhaps outdated
4. Replace the file /srv/www/tech/ads/adscal.html with the one you've generated

4new. Copy-paste the generated html into the ruby site's static page for ads calendar.

5. Finally, commit the changed versions. You'll need to commit adscal.html and pubdates.txt to the git repo and push the changes, ''and'' commit the changed version of adscal.html in /srv/www/tech/ads.

That's it! Long writeup, but shouldn't take very long to do.
