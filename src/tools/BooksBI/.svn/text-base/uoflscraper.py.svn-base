import re
import urllib2
from BeautifulSoup import BeautifulSoup

page = urllib2.urlopen('http://www.uleth.ca/ross/timetable/timetable_201102_2.htm')
soup = BeautifulSoup(page)

for i, row in enumerate(soup.html.body.table.findAll('tr')):
    if i == 0:
        print "Semester: %s" % row.th.contents[1]
        continue
    
    # Is it a discipline?
    if row.findAll('th'):
        print "Faculty: %s" % row.th.a.string
        continue

    # is it a course?    
    if hasattr(row, 'td'):
        try:
            crn = row.td.font.b.string
            # is it a number?
            if not re.search(r'\d+', crn):
                continue
        except:
            continue
        
        try:
            course = ""
            course = row.contents[3].contents[0].contents[0]
        except:
            pass
            
        try:
            section = ""
            section = row.contents[5].contents[0].contents[0]
        except:
            pass
            
        try:
            title = ""
            title = row.contents[7].contents[0].contents[0]
        except:
            pass
            
        try:
            days = ""
            days = row.contents[13].contents[0].contents[0].strip()
        except:
            pass
            
        try:
            time = ""
            time = row.contents[15].contents[0].contents[0]
        except:
            pass
            
        try:
            professor = ""
            professor = row.contents[19].contents[0].contents[0]
        except:
            pass
            
        print "%s %s %s %s %s %s\n\n\n\n" % (course, section, title, days, time, professor)