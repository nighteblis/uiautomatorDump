import shlex
from subprocess import Popen, PIPE
import xml.etree.ElementTree as ET
import time

def get_exitcode_stdout_stderr(cmd):
    """
    Execute the external command and get its exitcode, stdout and stderr.
    """
    args = shlex.split(cmd)

    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode
    #
    return exitcode, out, err
	
	
def capture(filename):
    get_exitcode_stdout_stderr("adb shell screencap -p /sdcard/"+filename+".png")
    exitcode,out,err = get_exitcode_stdout_stderr('adb pull /sdcard/'+filename+'.png "D:\long term\uiautomator simple_automation"')
    #print exitcode
    #print err
    get_exitcode_stdout_stderr("adb shell rm /sdcard/"+filename+".png	")
    return

def xmlParse():

    return
    
def bounds2array(boundsString):

    #print boundsString
    first=boundsString.split("][")
    
    return first[0].split("[")[1].split(",") , first[1].split("]")[0].split(",")
    
def swipeBar(a,b):
    x=a
    y=b
    x[0] = str(int(x[0]) + 50) 
    y[0] = str(int(y[0]) - 50)
    
    x[1] = str ( ( int(y[1]) + int(x[1]) ) / 2 +  ( int(y[1]) - int(x[1]) ) /4 )
    
    y[1] = x[1]
    
    cmd = "adb shell input swipe "+x[0]+" "+x[1] +" "+ y[0]+" "+y[1] + " 100 "    # arbitrary external command, e.g. "python mytest.py"
    print cmd
    exitcode, out, err = get_exitcode_stdout_stderr(cmd)
    return    
    
def horizswipe(a,b,step):

    x=a
    y=b
    temp =  int(x[0]) + int(y[0]) 
    x[0] = str( temp /2  + step/2 ) 
    y[0] = str( temp /2  - step/2) 
    
    x[1] = str ( ( int(y[1]) + int(x[1]) ) / 2 +  ( int(y[1]) - int(x[1]) ) /4 )
    
    y[1] = x[1]

    #print x[0]
    #print y[0]    
    
    #swipe <x1> <y1> <x2> <y2> [duration(ms)] 
    cmd = "adb shell input swipe "+x[0]+" "+x[1] +" "+y[0]+" "+y[1] + " 100 "    # arbitrary external command, e.g. "python mytest.py"
    print cmd
    #print "adb shell input swipe "+x[0]+" "+x[1] +" "+y[0]+" "+y[1] + " 100 " 
    exitcode, out, err = get_exitcode_stdout_stderr(cmd)
    return

    
def uiautomatordump():

    cmd = "adb shell uiautomator dump "  # arbitrary external command, e.g. "python mytest.py"
    exitcode, out, err = get_exitcode_stdout_stderr(cmd)
    # get the dump xml 
    cmd = "adb shell cat /storage/emulated/legacy/window_dump.xml" 
    exitcode, out, err = get_exitcode_stdout_stderr(cmd)
    if exitcode != 0:
        print err
    else:
        print 
        #print out	 
        
    root = ET.fromstring(out)
    #print root    

    return root


def getfee(root):    
    
    
    daily_fee_tv = root.findall(".//node[@resource-id='com.ucredit.paydayloan:id/daily_fee_tv']")[0]

    #ET.dump(daily_fee_tv[0])

    #print daily_fee_tv.attrib['text']

    collected_amount_tv = root.findall(".//node[@resource-id='com.ucredit.paydayloan:id/collected_amount_tv']")[0]

    #print collected_amount_tv.attrib['text']

    total_fee_tv = root.findall(".//node[@resource-id='com.ucredit.paydayloan:id/total_fee_tv']")[0]

    #print total_fee_tv.attrib['text']

    return daily_fee_tv.attrib['text'],collected_amount_tv.attrib['text'],total_fee_tv.attrib['text']
    


root = uiautomatordump()

loan_amount_view = root.findall(".//node[@resource-id='com.ucredit.paydayloan:id/loan_amount_view']")[0]

#print loan_amount_view.attrib['bounds']


a,b = bounds2array(loan_amount_view.attrib['bounds'])

swipeBar(a,b)


loan_days_view = root.findall(".//node[@resource-id='com.ucredit.paydayloan:id/loan_days_view']")[0]

#print loan_days_view.attrib['bounds']

#print type(loan_days_view.attrib['bounds'])

c,d = bounds2array(loan_days_view.attrib['bounds'])

swipeBar(c,d)


root = uiautomatordump()

feea,feeb,feec = getfee(root)
last = 0
    
#print "fees:"
#print (feea,feeb,feec)

#capture("test-500-7days")

y=7

for x in range(500, 1100,100):

    if x!=500:
        horizswipe(a,b, 120)
        print "amount to right"
    time.sleep(2)       
    root = uiautomatordump()
    #capture("test-"+str(x)+"-"+str(y)+"days")
    loan_amount_view = root.findall(".//node[@resource-id='com.ucredit.paydayloan:id/loan_amount_view']")[0]
    loan_days_view = root.findall(".//node[@resource-id='com.ucredit.paydayloan:id/loan_days_view']")[0]
    #print loan_amount_view.attrib['bounds']
    a,b = bounds2array(loan_amount_view.attrib['bounds'])      
    c,d = bounds2array(loan_days_view.attrib['bounds'])
    feea,feeb,feec = getfee(root)           

    for y in range(7, 31):

        print str(y)+" days"+" amount "+str(x)
        if y!=7:
            horizswipe(c,d, 40)
        time.sleep(2)       
        root = uiautomatordump()
        capture("test-"+str(x)+"-"+str(y)+"days")
        loan_amount_view = root.findall(".//node[@resource-id='com.ucredit.paydayloan:id/loan_amount_view']")[0]
        loan_days_view = root.findall(".//node[@resource-id='com.ucredit.paydayloan:id/loan_days_view']")[0]
        #print loan_amount_view.attrib['bounds']
        a,b = bounds2array(loan_amount_view.attrib['bounds'])      
        c,d = bounds2array(loan_days_view.attrib['bounds'])       
        feea,feeb,feec = getfee(root)          
    
        while feeb == last:
        
            horizswipe(c,d, 40)
            time.sleep(2)                
            root = uiautomatordump()
            capture("test-"+str(x)+"-"+str(y)+"days")
            loan_amount_view = root.findall(".//node[@resource-id='com.ucredit.paydayloan:id/loan_amount_view']")[0]
            loan_days_view = root.findall(".//node[@resource-id='com.ucredit.paydayloan:id/loan_days_view']")[0]
            #print loan_amount_view.attrib['bounds']
            a,b = bounds2array(loan_amount_view.attrib['bounds'])      
            c,d = bounds2array(loan_days_view.attrib['bounds'])           
            feea,feeb,feec = getfee(root)   
        f = open('paydayloan_test_result.csv', 'a')
        f.write(feea+','+feeb+','+feec+'\n')
        f.close()
        last = feeb
        

    swipeBar(c,d)
    print "swipe day bar to left"
    time.sleep(2)
    
    
'''
    
time.sleep(3)
horizswipe(a,b, 120)
print "1"
time.sleep(3)
horizswipe(a,b, 120)
print "2"
time.sleep(3)
horizswipe(a,b, 120)
print "3"
time.sleep(3)


time.sleep(3)
horizswipe(c,d, 80)
print "1"
time.sleep(3)
horizswipe(c,d, 80)
print "2"
time.sleep(3)
horizswipe(c,d, 80)
print "3"
time.sleep(3)


'''
