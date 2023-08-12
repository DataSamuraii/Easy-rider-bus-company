import json
import re
from datetime import datetime
from collections import defaultdict

json_input = json.loads(input())


#  Stage 1 function
def check_data_type(input_json):
    """
    Checks the data type complies with the documentation.

    :param input_json: json string.
    :return: total errors and dict {field: value}.
    """
    error_counts = {
        "bus_id": 0,
        "stop_id": 0,
        "stop_name": 0,
        "next_stop": 0,
        "stop_type": 0,
        "a_time": 0
    }

    for el in input_json:
        if not isinstance(el['bus_id'], int):
            error_counts['bus_id'] += 1
        if not isinstance(el['stop_id'], int):
            error_counts['stop_id'] += 1
        if not isinstance(el['stop_name'], str) or not el['stop_name'].strip():
            error_counts['stop_name'] += 1
        if not isinstance(el['next_stop'], int):
            error_counts['next_stop'] += 1
        if not isinstance(el['stop_type'], str) or len(el['stop_type']) > 1:
            error_counts['stop_type'] += 1
        if not isinstance(el['a_time'], str) or not el['a_time'].strip():
            error_counts['a_time'] += 1

    return f'Type and required field validation: {sum(error_counts.values())} errors.'\
        + '\n'.join([f"{key}: {value}" for key, value in error_counts.items()])


#  Stage 2 function
def check_data_format(input_json):
    """
    Checks that the data format complies with the documentation.

    :param input_json: json string.
    :return: total errors and dict {field: value}.
    """
    error_counts = {
        "stop_name": 0,
        "stop_type": 0,
        "a_time": 0
    }

    stop_name_pattern = re.compile(r'^([A-Z][a-z]+ )+(Road|Avenue|Boulevard|Street)$')
    stop_type_pattern = re.compile(r'^[SOF]$')
    a_time_pattern = re.compile(r'^([01][0-9]|2[0-3]):[0-5][0-9]$')

    for el in input_json:
        if not stop_name_pattern.match(el['stop_name']):
            error_counts['stop_name'] += 1
        if el['stop_type'] and (not stop_type_pattern.match(el['stop_type'])):
            error_counts['stop_type'] += 1
        if not a_time_pattern.match(el['a_time']):
            error_counts['a_time'] += 1

    return f'Format validation: {sum(error_counts.values())} errors'\
        + '\n'.join([f"{key}: {value}" for key, value in error_counts.items()])


#  Stage 3 function
def get_buses(input_json):
    """
    Checks how many bus lines we have and how many stops there are on each line.

    :param input_json: json string.
    :return: list with bus num and stops associated with the line.
    """
    bus_stops = defaultdict(int)

    for el in input_json:
        bus_stops[el['bus_id']] += 1

    return '\n'.join([f"bus_id: {key}, stops: {value}" for key, value in bus_stops.items()])


#  Stage 4 function
def check_stops(input_json):
    """
    Checks each bus line has exactly one starting point (S) and one final stop (F).

    :param input_json: json string.
    :return:
    """
    s_stops, f_stops = set(), set()
    start_end_counts = defaultdict(lambda: {'S': 0, 'F': 0})

    for el in input_json:
        bus_id, stop_type, stop_name = el['bus_id'], el['stop_type'], el['stop_name']

        if stop_type == 'S':
            s_stops.add(stop_name)
            start_end_counts[bus_id]['S'] += 1
        elif stop_type == 'F':
            f_stops.add(stop_name)
            start_end_counts[bus_id]['F'] += 1

    for bus, counts in start_end_counts.items():
        if counts['S'] != 1 or counts['F'] != 1:
            return f'There is no start or end stop for the line: {bus}.'

    print(f'Start stops: {len(s_stops)} {sorted(s_stops)}.\nFinish stops: {len(f_stops)} {sorted(f_stops)}.')


#  Stage 5 function
def str_to_time(time_str):
    return datetime.strptime(time_str, "%H:%M").time()


def check_time(input_json):
    """
    Checks that the arrival time for the upcoming stops for a given bus line is increasing.

    :param input_json: json string.
    :return: OK if no errors else bus_id : station name with wrong time
    """

    bus_stops = defaultdict(list)

    bus_to_skip = {}
    previous_time = None
    last_bus_id = None

    for el in json_input:
        current_time = str_to_time(el['a_time'])

        if el['bus_id'] != last_bus_id:
            previous_time = None
            last_bus_id = el['bus_id']

        if previous_time and current_time <= previous_time:
            if el['bus_id'] in bus_to_skip:
                continue
            bus_to_skip[el['bus_id']] = el['stop_name']

        previous_time = current_time
        bus_stops[el['bus_id']].append((el['stop_type'], el['stop_name'], el['a_time']))

    if not bus_to_skip:
        print('Arrival time test:\nOK')
    else:
        return '\n'.join([f'Arrival time test:\nbus_id line {bus}: wrong time on station {bus_to_skip[bus]}' for bus, stops in bus_stops.items() if bus in bus_to_skip])


#  Stage 6 function
def check_on_demands(input_json):
    """
    Checks that all the starting (S) points, final (F) stops, and transfer (T) stations are not "On-demand" (O).

    :param input_json: json string.
    :return: OK if no intersections else sorted set of intersecting O-stops
    """

    all_stops = defaultdict(int)
    s_stops, o_stops, f_stops = set(), set(), set()

    for el in input_json:
        stop_type, stop_name = el['stop_type'], el['stop_name']

        if stop_type == 'S':
            s_stops.add(stop_name)
        elif stop_type == 'O':
            o_stops.add(stop_name)
        elif stop_type == 'F':
            f_stops.add(stop_name)

        # Count all stops for later identifying transfer stops
        all_stops[stop_name] += 1

    t_stops = {stop for stop, count in all_stops.items() if count > 1}

    incorrect_o_stops = o_stops & (s_stops | f_stops | t_stops)

    if incorrect_o_stops:
        return 'On demand stops test:\nWrong stop type: ', sorted(incorrect_o_stops)
    else:
        return 'On demand stops test:\nOK'
