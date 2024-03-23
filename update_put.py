#!/usr/bin/python3
import subprocess


def get_command_updates_output(command):

    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (updates_output, err) = p.communicate()
    p_status = p.wait()
    return updates_output




cmd="""apt list --upgradable 2> /dev/null| awk -F'/' '{print $1}' | tail -n +2"""

output=str(get_command_updates_output(cmd))

import requests
url = 'http://192.168.122.221:5000/put_example'  # Modify this if your server is running on a different host or port

# Define the data you want to send in JSON format
data = {'key': 'updates', 'value': output}

# Send the PUT request
response = requests.put(url, json=data)

# Print the response from the server
print(response.json())
