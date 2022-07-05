from datetime import datetime
import utmp

# 系统文件路径
UPTIME_FILE = "/proc/uptime"
UTMP_FILE = "/var/run/utmp"
LOADAVG_FILE = "/proc/loadavg"


# 获取当前时间
def getCurrentSysTime():
    return datetime.now().strftime("%H:%M:%S")


# 获取系统启动时间
def getSysUptime():
    uptime = ""
    with open(UPTIME_FILE, "r") as f:
        up_time = f.read()
        time_list = up_time.split(" ")
        # 获取启动时间
        uptime_secs = float(time_list[0])
        # 获取具体启动时间
        up_days = int((uptime_secs / (60 * 60 * 24)))
        up_hours = str(int((uptime_secs / (60 * 60)) % 24))
        up_minutes = str(int((uptime_secs / 60) % 60))
        # 判断当前时间显示格式
        if up_days > 1:
            uptime += str(up_days) + (" days, " if up_days > 1 else " day, ")
        if up_hours:
            uptime += (up_hours + ":" + up_minutes)
        else:
            uptime += up_minutes
    return uptime


# 获取当前计算机用户数
def getCountUsers():
    user_count = 0
    with open(UTMP_FILE, 'rb') as f:
        buf = f.read()
        for entry in utmp.read(buf):
            # user_process = 7
            if entry.type.value == 7 and entry.user != "":
                user_count += 1
    return user_count


# 获取平均负载时间
def getAvgLoadTime():
    with open(LOADAVG_FILE, "r") as f:
        load_avg = f.read()
        load_avg_list = load_avg.split(" ")
    return load_avg_list


# 输出
def UptimePrint(
        current_systime, sys_uptime, sys_user_count,
        sys_avg_load_1, sys_avg_load_5, sys_avg_load_15):
    print("%s up  %s, %s %s, load average: %s  %s  %s" % (
        current_systime, sys_uptime,
        sys_user_count, "users" if sys_user_count > 1 else "user",
        sys_avg_load_1, sys_avg_load_5, sys_avg_load_15))


def main():
    current_sys_time = getCurrentSysTime()
    sys_uptime = getSysUptime()
    sys_user_count = getCountUsers()
    sys_avg_load_1 = getAvgLoadTime()[0]
    sys_avg_load_5 = getAvgLoadTime()[1]
    sys_avg_load_15 = getAvgLoadTime()[2]
    UptimePrint(current_sys_time, sys_uptime, sys_user_count, sys_avg_load_1, sys_avg_load_5, sys_avg_load_15)


if __name__ == '__main__':
    main()
