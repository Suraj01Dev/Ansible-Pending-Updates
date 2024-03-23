# Ansible Pending Updates 
_Devops Portfolio Project 3_


## Introduction
This project revolves around getting the list of all pending updates from multiple remote Linux servers and displaying all of them in a single dashboard. The tools used in this project are as follows ,
- Ansible
- Jenkins
- Python
- Flask
- Streamlit
- Bash

## Steps involved in building the project 
- Planning the architecture and setup
- Creating a Python Flask Server
- Creating a Python Client 
- Creating a Python Streamlit Dashboard
- Building an Ansible Playbook
- Automating using Jenkins


### Planning the architecture and setup

This project involves three servers one for running the ansible playbook (`Ansible Master Server`) the other is the target server where the updates need to be checked (`Target Server`) and the final server is for running the
**Python Flask Server** and **Python Streamlit Dashboard** (`Output Server`). 

![image](https://github.com/Suraj01Dev/Ansible-Pending-Updates/assets/120789150/ed30af23-6626-4fe6-b992-0b0ba42bff5f)

Although the project can have multiple target servers, for simplicity we will be using only one **Target Server**. Also, again for simplicity we will be using one server for both `Ansible Master Server` and `Output Server`.

![image](https://github.com/Suraj01Dev/Ansible-Pending-Updates/assets/120789150/0a0438d8-125e-40e5-a29c-a8f8bb90cb57)
