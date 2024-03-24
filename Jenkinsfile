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
