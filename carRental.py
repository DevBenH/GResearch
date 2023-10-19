from datetime import datetime
import json 
from collections import defaultdict
import argparse



def record_process(input_file):
    #dict is for single session
    sessions = defaultdict(dict)
    all_sessions = []

    with open(input_file, 'r') as file:
        session_records = json.load(file)

    #loops through each individual session in the file 
    for event in session_records:

        #add the session attributes to a dict with the key being the session id 
        if event['type'] == 'START':
            sessions[event['id']]['start_time'] = datetime.utcfromtimestamp(int(event['timestamp']))
            sessions[event['id']]['comments'] = event['comments']
        elif event['type'] == 'END':
            sessions[event['id']]['end_time'] = datetime.utcfromtimestamp(int(event['timestamp']))

    for session_id, session_data in sessions.items():
        start_time = session_data.get('start_time')
        end_time = session_data.get('end_time')

        #check if the session was complete
        if start_time and end_time:
            time_total = (end_time - start_time).total_seconds()
            #if the session was longer than 24 hours mark as being late
            if time_total > 86400:
                late = True
            else:
                late = False

            #if there were comments left mark the session as being damaged 
            if session_data.get('comments'):
                damaged = True
            else:
                damaged = False
            
            #add all info to dict
            summary = {
                'session_id': session_id,
                'start_time': start_time.strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': end_time.strftime('%Y-%m-%d %H:%M:%S'),
                'duration': time_total,
                'late': late,
                'damaged': damaged
            }

        #add individual session to global session list
        all_sessions.append(summary) 

    #write data into json file
    with open(args.output_file, 'w') as file:
        json.dump(all_sessions, file, indent=4)

#allow user to input files 
parser = argparse.ArgumentParser(description="Car Rental Application")
parser.add_argument('input_file', help='Input JSON file')
parser.add_argument('output_file', help='Output JSON file')

args = parser.parse_args()


record_process(args.input_file)

