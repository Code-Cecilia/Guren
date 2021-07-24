import datetime


def pretty_time(time, time_offset):
    if time.hour > 12:
        am_pm = 'PM'
        time -= datetime.timedelta(hours=12)
    else:
        am_pm = 'AM'
    return f'The time is: {str(time)[11:-7]} {am_pm}, GMT {time_offset}'


def time_bm(timezone):
    now = datetime.datetime.utcnow()

    if timezone is None:
        return pretty_time(now, '+0')
    else:
        time_offsets = [int(value) for value in timezone.split(':')]
        if len(time_offsets) == 2:
            now += datetime.timedelta(hours=time_offsets[0],
                                      minutes=time_offsets[1] * (-1 if (time_offsets[0] < 0) else 1))
        else:
            now += datetime.timedelta(hours=time_offsets[0])

        return pretty_time(now, timezone)
