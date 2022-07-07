#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Copyright (C) 2019-2022 成都曲速时代科技有限公司

from datetime import datetime
import utmp


class MyUptime:
    """
    Uptime数据
    """
    current_systime = ''
    sys_uptime = ''
    user_amount = 0
    avgload_1_min = ''
    avgload_5_min = ''
    avgload_15_min = ''

    def get_currentsystime(self):
        """
        获取当前时间
        """
        self.current_systime = datetime.now().strftime('%H:%M:%S')

    def get_sysuptime(self):
        """
        获取系统启动时间
        """
        with open('/proc/uptime', 'r') as f:
            uptime_secs = int(float(f.read().split(' ')[0]))
            up_days = uptime_secs // (60 * 60 * 24)
            up_hours = str((uptime_secs // (60 * 60)) % 24)
            up_minutes = str((uptime_secs // 60) % 60)
            if up_days:
                self.sys_uptime += str(up_days) + (' days, ' if up_days > 1 else ' day, ')
            if up_hours:
                self.sys_uptime += up_hours + ':' + up_minutes
            else:
                self.sys_uptime += up_minutes

    def get_useramount(self):
        """
        获取当前连接用户数
        """
        with open('/var/run/utmp', 'rb') as f:
            buf = f.read()
            for entry in utmp.read(buf):
                if entry.type.value == 7 and entry.user != '':
                    self.user_amount += 1

    def get_avgloadtime(self):
        """
        获取平均负载时间
        """
        with open('/proc/loadavg', 'r') as f:
            self.avgload_1_min, self.avgload_5_min, self.avgload_15_min = f.readline().split(' ')[:3]

    def my_print(self):
        """
        打印Uptime内容
        """
        print(
            f'{self.current_systime} up  {self.sys_uptime}, '
            f'{self.user_amount} {"users" if self.user_amount > 1 else "user"},'
            f'load average: {self.avgload_1_min}  {self.avgload_5_min}  {self.avgload_15_min}')

    def __init__(self):
        self.get_currentsystime()
        self.get_sysuptime()
        self.get_useramount()
        self.get_avgloadtime()


def main():
    MyUptime().my_print()


if __name__ == '__main__':
    main()
