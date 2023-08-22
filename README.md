Easy Rider Bus Company database checker I made myself!

I've just been hired by a bus company that started actively using the Internet for business. Before I came, their database had been updated a few times by various employees with various levels of skill. My task is to find all the mistakes they made in the database. Good news: I had documentation, but bad news: it's incomplete. This promises to be quite an investigation!

---
# Bus Company Schedule Validator Documentation

## Overview

The Bus Company Schedule Validator is a Python program that validates the schedule data for a bus company. It ensures that the provided data meets certain criteria in terms of structure, format, and logical consistency. The validation process is divided into multiple stages, each focusing on different aspects of validation. This separation into stages allows for a methodical approach to validating the data, making it suitable for an educational project.

## Functions

### Stage 1: Data Type Validation

- **Function**: `check_data_type(input_json)`
- **Description**: Validates the data types of various fields in the JSON input and counts the number of errors.
- **Parameters**: The JSON object containing the bus schedule data.
- **Returns**: Error message detailing the count and nature of errors.

### Stage 2: Data Format Validation

- **Function**: `check_data_format(input_json)`
- **Description**: Validates the data format by checking it against regular expressions.
- **Parameters**: The JSON object containing the bus schedule data.
- **Returns**: Error message detailing the count and nature of errors.

### Stage 3: Bus Line and Stops Counter

- **Function**: `get_buses(input_json)`
- **Description**: Counts the number of stops for each bus line.
- **Parameters**: The JSON object containing the bus schedule data.
- **Returns**: String with the bus ID and the number of stops associated with each line.

### Stage 4: Start and Finish Stop Validation

- **Function**: `check_stops(input_json)`
- **Description**: Validates that each bus line has exactly one starting point (S) and one final stop (F).
- **Parameters**: The JSON object containing the bus schedule data.
- **Returns**: Message regarding the validation of start and end stops.

### Stage 5: Arrival Time Validation

- **Function**: `check_time(input_json)`
- **Description**: Validates that the arrival times for the upcoming stops for a given bus line are in increasing order.
- **Parameters**: The JSON object containing the bus schedule data.
- **Returns**: "OK" if no errors; else details of stations with incorrect times.

### Stage 6: On-Demand Stop Validation

- **Function**: `check_on_demands(input_json)`
- **Description**: Validates that all starting (S) points, final (F) stops, and transfer (T) stations are not "On-demand" (O).
- **Parameters**: The JSON object containing the bus schedule data.
- **Returns**: "OK" if no errors; else a sorted set of incorrect On-demand stops.

## Usage

This script expects a JSON object as input. The input should be structured according to the expected fields for the bus schedule. 

## Example

A typical JSON input might look like:

```json
[
  {
    "bus_id": 128,
    "stop_id": 1,
    "stop_name": "Prospekt Avenue",
    "next_stop": 3,
    "stop_type": "S",
    "a_time": "08:12"
  },
  {
    "bus_id": 256,
    "stop_id": 2,
    "stop_name": "Pilotow Street",
    "next_stop": 3,
    "stop_type": "S",
    "a_time": "09:20"
  },
  {
    "bus_id": 512,
    "stop_id": 6,
    "stop_name": "Sunset Boulevard",
    "next_stop": 0,
    "stop_type": "F",
    "a_time": "08:16"
  },
  ...
]
```

## Conclusion

The Bus Company Schedule Validator provides a comprehensive and staged approach to validating a bus company's schedule. By dividing the validation into clear stages, it aids in understanding different facets of validation and ensures that the data complies with all necessary standards. This educational project serves as a robust example of data validation techniques in Python.

---
Here's the link to the project: https://hyperskill.org/projects/128

Check out my profile: https://hyperskill.org/profile/103100057
