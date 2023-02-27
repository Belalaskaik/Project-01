from datetime import datetime, timedelta

def merge_time_slots(person1_schedule, person2_schedule):
    # Combine both schedules into one available_slots
    combined_schedule = person1_schedule + person2_schedule

    # Convert the start and end times to integers (minutes since midnight)
    for slot in combined_schedule:
        slot[0] = int(slot[0].replace(':', ''))  # e.g. '7:00' -> 700
        slot[1] = int(slot[1].replace(':', ''))

    # Sort the slots by start time
    combined_schedule.sort(key=lambda slot: slot[0])

    # Merge overlapping slots
    merged_schedule = []
    current_start_time = None
    current_end_time = None
    for slot in combined_schedule:
        if current_start_time is None:
            current_start_time, current_end_time = slot
        elif slot[0] <= current_end_time:
            current_end_time = max(current_end_time, slot[1])
        else:
            merged_schedule.append([current_start_time, current_end_time])
            current_start_time, current_end_time = slot
    merged_schedule.append([current_start_time, current_end_time])

    # Convert the start and end times back to strings (hh:mm format)
    for slot in merged_schedule:
        slot[0] = f'{slot[0] // 100:02}:{slot[0] % 100:02}'  # e.g. 700 -> '07:00'
        slot[1] = f'{slot[1] // 100:02}:{slot[1] % 100:02}'

    return merged_schedule


def max_time(time1, time2):
    t1_hours, t1_minutes = map(int, time1.split(':'))
    t2_hours, t2_minutes = map(int, time2.split(':'))

    if t1_hours > t2_hours:
        return time1
    elif t2_hours > t1_hours:
        return time2
    else:  # t1_hours == t2_hours
        if t1_minutes > t2_minutes:
            return time1
        else:
            return time2


def min_time(time1, time2):
    t1_hours, t1_minutes = map(int, time1.split(':'))
    t2_hours, t2_minutes = map(int, time2.split(':'))

    if t1_hours < t2_hours:
        return time1
    elif t2_hours < t1_hours:
        return time2
    else:  # t1_hours == t2_hours
        if t1_minutes < t2_minutes:
            return time1
        else:
            return time2


          


def get_common_daily_range(person1_DailyAct, person2_DailyAct):
    start_time = max(person1_DailyAct[0], person2_DailyAct[0])
    end_time = min(person1_DailyAct[1], person2_DailyAct[1])
    return [start_time, end_time]


def get_free_slots(duration, schedule, common_range):
    start_time = datetime.strptime(common_range[0], '%H:%M')
    end_time = datetime.strptime(common_range[1], '%H:%M')
    free_slots = []
    last_end_time = start_time

    for slot in schedule:
        slot_start_time = datetime.strptime(slot[0], '%H:%M')
        slot_end_time = datetime.strptime(slot[1], '%H:%M')

        if slot_start_time > last_end_time and slot_start_time < end_time:
            free_duration = (slot_start_time - last_end_time).total_seconds() / 60
            if free_duration >= duration:
                free_slots.append([last_end_time.strftime('%H:%M'), slot_start_time.strftime('%H:%M')])
        
        last_end_time = max(last_end_time, slot_end_time)

    if end_time > last_end_time:
        free_duration = (end_time - last_end_time).total_seconds() / 60
        if free_duration >= duration:
            free_slots.append([last_end_time.strftime('%H:%M'), end_time.strftime('%H:%M')])

    return free_slots


slots = [['7:00', '8:30'], ['12:00', '13:00'], ['16:00', '18:00']]
duration = 30

person1_schedule = [['7:00', '8:30'], ['12:00', '13:00'], ['16:00', '18:00']]
person1_DailyAct = ['8:00', '19:00']

person2_schedule = [['9:00', '10:30'], ['12:20', '14:30'], ['14:00', '15:00'], ['16:00', '17:00']]
person2_DailyAct = ['9:00', '18:30']

merged_schedule = merge_time_slots(person1_schedule, person2_schedule)



common_range = get_common_daily_range(person1_DailyAct, person2_DailyAct)

available_slots=get_free_slots(duration, merged_schedule, common_range)
print(available_slots)
