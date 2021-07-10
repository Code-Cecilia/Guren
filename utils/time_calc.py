  
def get_time(time):
    if time is not None:
        if time[-1] == 'h':
            time_final = int(time[:-1]) * 3600
        elif time[-1] == 'm':
            time_final = int(time[:-1]) * 60
        elif time[-1] == 's':
            time_final = int(time[:-1])
        else:
            time_final = int(time)
        return time_final


def parse_utc(utc_str):
    date = utc_str[:10]
    time = utc_str[11:19]
    return date, time


def time_suffix(time):
    if time is not None:
        if time[-1] == 'd':
            final_thing = str(time)[:-1] + ' days'
        elif time[-1] == 'h':
            final_thing = str(time)[:-1] + ' hours'
        elif time[-1] == 'm':
            final_thing = str(time)[:-1] + ' minutes'
        elif time[-1] == 's':
            if time[:-1] == '1':
                final_thing = str(time)[:-1] + ' second'
            else:
                final_thing = str(time)[:-1] + ' seconds'
        else:
            if time == '1':
                final_thing = str(time) + ' seconds'
            else:
                final_thing = str(time) + ' seconds'
        return final_thing