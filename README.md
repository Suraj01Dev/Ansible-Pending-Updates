# Ansible Pending Updates 
_Devops Portfolio Project 3_

![image](https://github.com/Suraj01Dev/Ansible-Pending-Updates/assets/120789150/366d3aac-4468-4fbc-99e0-8568424a2f32)

## Introduction
This project revolves around getting the list of all pending updates from multiple remote Linux servers and displaying all of them in a single dashboard. The tools used in this project are as follows,
- Ansible
- Jenkins
- Python
- Flask
- Streamlit
- Bash

## Steps involved in building the project 
- Planning the architecture and setup
- Creating the Python Flask Server
- Creating the Python Client 
- Creating a Python Streamlit Dashboard
- Building an Ansible Playbook
- Automating using Jenkins


## Planning the architecture and setup

This project involves three servers one for running the ansible playbook (`Ansible Master Server`) the other is the target server where the updates need to be checked (`Target Server`) and the final server is for running the
**Python Flask Server** and **Python Streamlit Dashboard** (`Output Server`). 

![image](https://github.com/Suraj01Dev/Ansible-Pending-Updates/assets/120789150/ed30af23-6626-4fe6-b992-0b0ba42bff5f)

Although the project can have multiple target servers, for simplicity we will be using only one **Target Server**. Also, again for simplicity we will be using one server for both `Ansible Master Server` and `Output Server`.

![image](https://github.com/Suraj01Dev/Ansible-Pending-Updates/assets/120789150/0a0438d8-125e-40e5-a29c-a8f8bb90cb57)

## Creating a Python Flask Server

### Prerequisites :
_To be satisfied in the Output Server_
- Python3 should be installed
- Flask Python module should be installed
  ```
  pip3 install flask
  ```
- Streamlit Python module should be installed
  ```
  pip3 install streamlit
  ```
- Pandas Python module should be installed
  ```
  pip3 install pandas
  ```
  

### Working of Python Flask Server

Let's first create the [flask_server.py](https://raw.githubusercontent.com/Suraj01Dev/Ansible-Pending-Updates/main/flask_server.py) file which runs in the **Output Server**. It listens for PUT requests from the `Python Client` in the target servers. The Flask server runs in the Output Server at port 5000. The Python client sends the pending updates from the target server as a string separated by **\n**. This data after reaching the Flask server is processed and stored in a JSON file with the following naming convention `Pending_Updates (Server: \<target server ip\>).json`


**Pending_Updates (Server: 192.168.122.125).json**
```json
{"Pending_Updates (Server: 192.168.122.125)": ["bash", "cloud-init", "dpkg", "libldap-2.5-0", "libldap-common", "linux-generic", "linux-headers-generic", "linux-image-generic", "linux-libc-dev", "python3-update-manager", "vim-common", "vim-runtime", "vim", "xxd"]}
```
The above JSON is a example output from the target server **192.168.122.125** to the output server.

`Note`: The reason for this particular naming convention is because there can be multiple target servers sending in requests, thus to differentiate between them the naming convention was developed.

To run the Flask Server execute the below command.
```bash
python3 flask_server.py
```

## Creating the Python Client 

Now let's create the Python Client [send_pending_updates.py](https://raw.githubusercontent.com/Suraj01Dev/Ansible-Pending-Updates/main/send_pending_updates.py) which will be present in the target server. The Python client will be executed periodically to send the PUT request to the Flask Server in the Output Server.

### Working of Python Client

The working of the Python Client is very simple, it executes the below bash command using python and sends the payload as a string to the Output Server as a PUT request.
```bash
apt list --upgradable 2> /dev/null| awk -F'/' '{print $1}' | tail -n +2
```

To run the python client execute the below command.
```bash
python3 send_pending_updates.py --host <ip of the output server>
```

## Creating a Python Streamlit Dashboard

The Python Streamlit Dashboard server also goes in the Output Server. And both the `flask_server.py` and [pending_updates_dashboard.py](https://raw.githubusercontent.com/Suraj01Dev/Ansible-Pending-Updates/main/pending_updates_dashboard.py) should be present in the same directory. This is because 
the **Pending_Updates (Server: \<target server ip\>).json** file created by the Flask Server will be used by the **Python Streamlit Dashboard Server** to display the data in the UI. 

In order to run the Python Streamlit Dashboard Server the below command should be executed.
```bash
streamlit run pending_updates_dashboard.py
```

![image](https://github.com/Suraj01Dev/Ansible-Pending-Updates/assets/120789150/cddfdd82-e43d-41ee-9005-a0e1dbc320a5)

The UI will look similar to this.


### Working of the Python Streamlit Dashboard

The Pending_Updates (Server: \<target server ip\>).json file created by the Flask Server will be read by the Python Streamlit Dashboard server using pandas as a DataFrame and this DataFrame is displayed in the Streamlit UI. The Python Streamlit Dashboard server makes sure it reads all the JSON files with this `Pending_Updates (Server: \<target server ip\>).json` naming convention and displays the data in the UI. The UI run on the default port **8501**.



## Building an Ansible Playbook

Now comes the interesting part which is the ansible playbook. The role of  [ansible_pending_updates.yaml](https://raw.githubusercontent.com/Suraj01Dev/Ansible-Pending-Updates/main/ansible_pending_updates.yaml) ansible-playbook is to remotely execute the Python Client in the various remote target servers.

The ansible is built on the following steps:
- Check for Python3 installation
- Installs Python3 if not found
- Checks for a directory "/opt/scripts/ansible_updates"
- If not found creates the directory "/opt/scripts/ansible_updates"
- Check for the file send_pending_updates.py under the directory "/opt/scripts/ansible_updates"
- If not found downloads the file [send_pending_updates.py](https://raw.githubusercontent.com/Suraj01Dev/Ansible-Pending-Updates/main/send_pending_updates.py) from the GitHub
- Finally executes the Python Client **send_pending_updates.py**

 Note: Before executing the ansible playbook make sure to enter the ip of the Dashboard server in the vars section of the yaml file.
```yaml
   vars:
    server_ip: "192.168.122.221" 
```

To run the ansible playbook, use the below command
```
ansible-playbook ansible_pending_updates.yaml 
```

#### Note:
To avoid passwordless authentication in ansible follow the below 2 steps:
- Passwordless SSH Login
- Passwordless sudo access for ansible user

#### Passwordless SSH Login
To enable password-less login we have to create a public and private key in the ansible node and copy the public key to all the managed nodes.
```
ssh-keygen
```
The above command will create a public and private key under the `~/.ssh`  directory.
To copy this public key to all the target nodes `ssh-copy-id` command has to be used.

```
ssh-copy-id -i ~/.ssh/id_rsa.pub ansible@target_server
```


#### Passwordless sudo access for ansible user

To enable password less sudo access follow the below steps in the target node.
1. Execute `visudo`
2. Paste the below command at the end of the file.
```
ansible         ALL = (ALL) NOPASSWD: ALL
```

## Automating using Jenkins

Now let's create a [Jenkinsfile](https://raw.githubusercontent.com/Suraj01Dev/Ansible-Pending-Updates/main/Jenkinsfile) to automate the ansible-playbook.

### Prerequisites:
- Setting up Jenkins on a ubuntu sever ([link](https://phoenixnap.com/kb/install-jenkins-ubuntu))
- Setting Ansible Master Server as a Jenkins Node ([link](https://devopscube.com/setup-slaves-on-jenkins-2/))

### Working of the Jenkinsfile

```
pipeline {
    agent {
        label "AnsibleNode"
    }

    stages {
        stage('Clean Workspace') {
            steps {
            cleanWs()
            }
        }
        stage('Ansible Playbook Download') {
            steps {
                sh 'wget https://raw.githubusercontent.com/Suraj01Dev/Ansible-Pending-Updates-Jenkins/main/ansible_pending_updates.yaml'
            }
        }
        stage('Execute Ansible Playbook') {
            steps {
                sh "ansible-playbook ansible_pending_updates.yaml"
            }
    }
}
}
```
The Jenkinsfile file logic follows the following steps:
1. Cleans the workspace
2. Downloads the `ansible_pending_updates.yaml` file from the repo
3. Finally it executes the ansible playbook using the command ```ansible-playbook ansible_pending_updates.yaml```



## Summary
1. The project contains 3 servers
   - Target server
   - Ansible Master Server
   - Output Server
2. Download the below files into the Output Server.
    ```bash
    
    wget https://raw.githubusercontent.com/Suraj01Dev/Ansible-Pending-Updates/main/flask_server.py
    wget https://raw.githubusercontent.com/Suraj01Dev/Ansible-Pending-Updates/main/pending_updates_dashboard.py
    ```
3. Open two terminal sessions and execute the below command to run the Flask Server and the Dashboard Server.
    ```bash
    python3 flask_server.py
    ```

    ```bash
    streamlit run pending_updates_dashboard.py
    ```
4. Connect the Ansible Master Server with your Jenkins setup as a SSH agent.
5. Run a Jenkins pipeline using this [repo](https://github.com/Suraj01Dev/Ansible-Pending-Updates) as a git SCM.

