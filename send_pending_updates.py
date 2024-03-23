#! /bin/python3
import subprocess
import requests


def get_command_updates_output(command):

    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (updates_output, err) = p.communicate()
    p_status = p.wait()
    return updates_output


def send(host):
    ip_address=get_command_updates_output("hostname -I").decode().split()[0]
    cmd="apt list --upgradable 2> /dev/null| awk -F'/' '{print $1}' | tail -n +2"
    output=get_command_updates_output(cmd).decode().strip()

    url = f'http://{host}:5000/put_example'  

    data = {'key': 'updates', 'value': ip_address+"\n"+output}

    response = requests.put(url, json=data)

    print(response.json())

if __name__=="__main__":
    host="192.168.122.221"
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--host',help="Host Name",nargs='?', default= host)
    args=parser.parse_args()
    send(args.host)
    
