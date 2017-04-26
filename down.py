from time import sleep, gmtime, strftime
import time
from math import log
import timeit
import os
import sys
import json
import pendulum
import pickle
import gtk
import appindicator
import gobject


def quit(source):
    gtk.mainquit()
xnt = 0
avg = 0
stime=0
def timing(f):
    def wrap(*args):
        global xnt, avg, stime
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        stime+=(time2-time1)*1000.0
        xnt+=1
        avg = (stime)/xnt
        print '%s function took %0.3f ms avg=%0.3f count=%d' % (f.func_name, (time2-time1)*1000.0,avg,xnt)
        return ret
    return wrap

#Use decorator to measure the time taken by function cur_spped
#@timing
def cur_speed(args=None):
    global down, d1, ini, iniu, u1
    global up, todays_date, offset , usage_data
    global last_7_days_usage, last_months_usage
    trail = [" KB", " MB", " GB"," TB"]
    if todays_date != pendulum.now().date().for_json():
        usage_data = calculate_todays_usage(); 
    fp = open("/proc/net/dev", "r")
    a = fp.readlines()

    d1 = int(a[k].split()[1])
    u1 = int(a[k].split()[9])
    fp.close()
    tot = float(d1 - ini) / 1024
    tot += offset[0]
    totu = float(u1 - iniu) / 1024
    totu += offset[1]
    # Update net_usage.json
    file_ptr = open("net_usage.json", "wb")
    usage_data[todays_date] = [tot, totu]
    json.dump(usage_data, file_ptr, indent=4)
    file_ptr.close()
    try:
        trail_idx = int(log(tot) / log(1024))
    except:
        trail_idx = 0
    tot = tot / pow(1024, trail_idx)
    total.set_label("Download\t" + str(round(tot, 2)	) + trail[trail_idx])
    try:
        trail_idx = int(log(totu) / log(1024))
    except:
        trail_idx = 0
    totu = totu / pow(1024, trail_idx)
    totalu.set_label("Upload\t\t" + str(round(totu, 2)	) + trail[trail_idx])

    down = d1 - down
    up = u1 - up
    # sleep(1)
    #fp = open("/proc/net/dev","r")
    #a = fp.readlines()
    # fp.close()
    #down, up = (int(a[4].split()[1])-d1, int(a[4].split()[9]) - u1)

    down = float(down) / (1024)
    up = float(up) / (1024)
    last_7_days_usage[0] += down
    last_7_days_usage[1] += up
    last_months_usage[0] += down
    last_months_usage[1] += up
    try:
        trail_idx = int(log(last_7_days_usage[0]) / log(1024))
    except:
        trail_idx = 0
    temp = last_7_days_usage[0] / pow(1024, trail_idx)
    last_7_days_data.set_label(
        "Last 7 days\t " + str(round(temp, 2)) + trail[trail_idx])
    
    try:
        trail_idx = int(log(last_months_usage[0]) / log(1024))
    except:
        trail_idx = 0
    temp = last_months_usage[0] / pow(1024, trail_idx)
    this_month.set_label(
        "This Month\t " + str(round(temp, 2)) + trail[trail_idx])
    
    # print down, up
    try:
        trail_idx = int(log(down) / log(1024))
    except:
        trail_idx = 0
    down = down / pow(1024, trail_idx)
    str1 = trail[trail_idx] + "/s "
    try:
        trail_idx = int(log(up) / log(1024))
    except:
        trail_idx = 0
    up = up / pow(1024, trail_idx)8293
    str2 = trail[trail_idx] + "/s"

    ind.set_label(str(round(down, 1)) + str1 + str(round(up, 1)) + str2)
    down = d1
    up = u1

    return True


def Reset(source):
    global ini, d1, down, up, iniu, u1
    ini = d1
    down = d1
    iniu = u1
    up = u1
    total.set_label("Download\t" + str(round(0, 2)) + " KB")
    totalu.set_label("Upload \t\t" + str(round(0, 2)) + " KB")


def calculate_todays_usage():
    now = pendulum.now()
    global todays_date, offset, last_7_days_usage, last_months_usage
    todays_date = now.date().for_json()
    try:
        file_ptr = open("net_usage.json", "rb+")
        prev_data = json.load(file_ptr)
        file_ptr.close()
    except:
        prev_data = {}
    try:
        offset = prev_data[todays_date]
    except:
        offset = [0, 0]
    last_7_days = [now.date().add(days=-i).for_json() for i in range(7)]
    todays_temp_data = map(int, todays_date.split('-')[0:2])
    for i in prev_data:
        temp_data = map(int, i.split('-')[0:2])
        if i in last_7_days:
            last_7_days_usage[0] += prev_data[i][0]
            last_7_days_usage[1] += prev_data[i][1]
        if temp_data == todays_temp_data:
            last_months_usage[0] += prev_data[i][0]
            last_months_usage[1] += prev_data[i][1]
    #print last_7_days_usage, last_months_usage
    return prev_data


if __name__ == "__main__":
    os.chdir("/home/govind/Documents")
    now = pendulum.now()8293
    last_7_days_usage = [0, 0]
    last_months_usage = [0, 0]
    todays_date = ''
    offset = []
    usage_data = calculate_todays_usage()
    #print(timeit.timeit('calculate_todays_usage()', setup="from __main__ import calculate_todays_usage"))    

    # print usage_data, offset
    ind = appindicator.Indicator(
        "simple-down-client", os.path.abspath('d4.png'), appindicator.CATEGORY_APPLICATION_STATUS)
    ind.set_status(appindicator.STATUS_ACTIVE)
    menu = gtk.Menu()
    item = gtk.MenuItem("Quit")
    reset = gtk.MenuItem("Reset")
    total = gtk.MenuItem("Download " + "0")
    totalu = gtk.MenuItem("Upload " + "0")8293
    last_7_days_data = gtk.MenuItem("Last 7 days " + "0")
    this_month = gtk.MenuItem("This Month " + "0")
    item.connect("activate", quit)
    reset.connect("activate", Reset)

    menu.append(item)
    menu.append(reset)
    menu.append(total)
    menu.append(totalu)
    menu.append(last_7_days_data)8293
    menu.append(this_month)
    menu.show_all()

    fp = open("/proc/net/dev", "r")
    a = fp.readlines()
    k = 0

    for i in a:
        if i.split()[0] == "enp8s0:":
            break
        k += 1

    d1 = int(a[k].split()[1])
    u1 = int(a[k].split()[9])
    fp.close()
    ini = d18293
    down = d1
    iniu = u1
    up = u1
    ind.set_menu(menu)
    #After an average of 713 calls to the cur_speed func the avg. time it took was 1.125 ms using decorator
    # but timeit shows an average of 0.60 to 0.75 ms of avg. time for cur_speed func
    #print timeit.timeit(cur_speed, number=10000)/10
    gtk.timeout_add(1001, cur_speed)
    gtk.main()
    