import csv
import math
import datetime

# There are probably more elegant ways to do this,
#    with less repeated code, etc. This seemed to do the job for me.
TAs = set(['arb379','aa2398','ax28','az258',
            'jl3726','cb776','cai29','dsc254',
            'dl654','dl772','drr68','eg456',
            'ebc48','el536','efg36','gd326',
            'ha366','hb388','hy539','hc667',
            'jl2964','jc3464','jk2332','jq77',
            'kpl39','lwt29','lew96','ah839',
            'lz266','ld477','lmc336','nn269',
            'ork6','rkk59','rc564','fs333',
            'rgh224','rt389','sh797','sw984',
            'tps87','tj258','bh486','wmg47',
            'wh367','xy269','yz386','yh385',
            'ys447','ys393','yx67','zg48',
            'zc422','tj36','nh386','ahf42']) # taken from contact list

# course roster, 12/09/19
# used for joining student data later
roster = {}
with open('2019FA_CS4780_001(12632)_Dec_09_2019.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        roster[row['NET ID']] = row['NAME']

# # # TASK: build up dictionaries for each net id, gathering info
# # #       from indiv .csv files

# HW tallys
total = {} # dictionary: student -> dictionary of info
hw3exceptions = set(['as2643','at677','el629','jjc387','js2595',
                    'jt658','pk574','skh83','ss2972','ss3263',
                    'sf373','wz276','asa242']) # Grace Hopper exemptions

# build up fields of the final .csv files
fieldnames = ["NET ID","NAME"]
hwgrades=[]
hwldays=[]
for i in range(1,6):
    hw_name = 'HW%d' % i
    hwgrades.append('Grade '+hw_name)
    hwldays.append('LateDays '+hw_name)
fieldnames.extend(hwgrades)
fieldnames.extend(hwldays)
# traverse Gradescope files named 'HW?.csv'. Contains lateness,grade info
# downloaded 12/17
for i in range(1,6):
    hw_name = 'HW%d' % i
    hw_lday = 'LateDays '+hw_name
    hw_grade = 'Grade '+hw_name
    with open(hw_name+'.csv',newline='\n') as hwfile:
        reader = csv.DictReader(hwfile)
        for row in reader:
            netid = row['Email'].split('@')[0] # deal with netids without @cornell.edu
            if netid not in TAs:
                if netid not in total:
                    nam = row['Name'].split(' ')
                    newnam = ','.join(nam[::-1])
                    total[netid] = {'NET ID':netid, 'NAME':newnam}
                student = total[netid]
                if row['Lateness (H:M:S)'] is not None: # if late
                    [hours,mins,secs] = map(int,row['Lateness (H:M:S)'].split(':'))
                    if hours+mins+secs==0 or (i==3 and netid in hw3exceptions):
                        student[hw_lday] = 0
                    else:
                        hourmins = hours+(mins-10)/60.0
                        student[hw_lday] = math.ceil(hourmins/24.0)
                    student[hw_grade] = row['Total Score']
# now [total] contains dictionaries of each student's records
# compare with roster and divide into two .csv files
with open('HW_info_extras.csv','w',newline='') as fhandextra:
    with open('HW_info_joinedroster.csv','w',newline='') as fhandjoin:
        writer = csv.DictWriter(fhandjoin, fieldnames=fieldnames)
        writer.writeheader()
        writerex = csv.DictWriter(fhandextra, fieldnames=fieldnames)
        writerex.writeheader()
        for netid in sorted(total.keys()):
            dic = total[netid]
            if netid in roster:
                dic['NAME'] = roster[netid]
                writer.writerow(dic)
            else:
                writerex.writerow(dic)


# # # Same process with projects.
#     The data format from Vocareum is different
#     late day calc was a bit more annoying

total = {} # dictionary: student -> dictionary of info
duedates = ['Sep-18-2019 12:00:00 am',
            'Sep-26-2019 12:00:00 pm',
            'Oct-14-2019 12:00:00 am',
            'Nov-05-2019 12:00:00 pm',
            'Nov-21-2019 12:00:00 pm',
            'Dec-10-2019 12:00:00 pm']
formatstr = '%b-%d-%Y %I:%M:%S %p'
# Weird glitch on Vocareum caused their submission to have wrong dates
p3exceptions = set(['ra534','kz265'])

# build field names for final .csv files
fieldnames = ["NET ID","NAME"]
pgrades=[]
pldays=[]
for i in range(1,7):
    p_name = 'P%d' % i
    pgrades.append('Grade '+p_name)
    pldays.append('LateDays '+p_name)
fieldnames.extend(pgrades)
fieldnames.extend(pldays)
# traverse 6 projects, save data
for i in range(1,7):
    p_name = 'P%d' % i
    p_lday = 'LateDays '+p_name
    p_grade = 'Grade '+p_name
    # Vocareum saved only submission time, instead of lateness.
    # Used datetime for time subtraction.
    duedate = datetime.datetime.strptime(duedates[i-1], formatstr)
    with open(p_name+'.csv',newline='\n') as proj:
        reader = csv.DictReader(proj)
        for row in reader:
            netid = row['email'].split('@')[0]
            if netid not in TAs:
                if netid not in total:
                    total[netid] = {'NET ID':netid, 'NAME':None}
                student = total[netid]
                subtime = datetime.datetime.strptime(row['last submission date-time'][:-4],formatstr)
                hours = (subtime-duedate).total_seconds()/3600.0
                if row['late']=='Y':
                    assert(hours>=0)
                    if (hours>168) or (i==3 and netid in p3exceptions): # various Vocareum glitches
                        hours = 0
                    if hours>36: hours -= 12 # due to late submission deadline being at midnight
                                             # even if the real deadline was at noon.
                    student[p_lday] = math.ceil(hours/24.0)
                else:
                    assert(hours<0)
                    student[p_lday] = 0
proj_names=['','Score: Project 1 - KNN','Score: Project 2: Perceptron',
            'Score: Project 3 - SVM and Kernels','Score: Project 4 - Deep Learning',
            'Score: Project 5 - Naive Bayes','Score: Project 6 - Final Competition']
# Vocareum grades downloaded in batch, in a separate file.
with open('VocareumGrades.csv') as pgradefile:
    reader = csv.DictReader(pgradefile)
    for row in reader:
        netid = row['Email'].split('@')[0]
        for i in range(1,7):
            p_name = 'P%d' % i
            p_grade = 'Grade '+p_name
            if netid not in TAs:
                if netid not in total:
                    total[netid] = {'NET ID':netid, 'NAME':None}
                student = total[netid]
                rawgrade = row[proj_names[i]]
                # the string '--------' corresponds to no submission
                if i==1 and rawgrade!='--------':
                    student[p_grade] = float(rawgrade)/13.0*100.0
                elif i!=1 and rawgrade!='--------':
                    student[p_grade] = float(rawgrade)
# now [total] contains dictionaries of each student's records
# compare with roster and divide into two .csv files
with open('Proj_info_extras.csv','w',newline='') as fhandextra:
    with open('Proj_info_joinedroster.csv','w',newline='') as fhandjoin:
        writer = csv.DictWriter(fhandjoin, fieldnames=fieldnames)
        writer.writeheader()
        writerex = csv.DictWriter(fhandextra, fieldnames=fieldnames)
        writerex.writeheader()
        for netid in sorted(total.keys()):
            dic = total[netid]
            if netid in roster:
                dic['NAME'] = roster[netid]
                writer.writerow(dic)
            else:
                writerex.writerow(dic)


