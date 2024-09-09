pipeline {
    agent any
    parameters {
        string(name: 'BROWSER', defaultValue: 'chrome', description: 'Browser name')
        string(name: 'NUMPROCESS', defaultValue: '1', description: 'Number of processes')
    }
    environment {
        SHELL = '/bin/bash'
        GIT_REPO = 'https://github.com/ola290919/UI_sppi.git'
        ALLURE_RESULTS = 'allure-results'
        BROWSER = "${params.BROWSER}"
        NUMPROCESS = "${params.NUMPROCESS}"
    }
    stages {
        stage('Clone repository') {
            steps {
                git branch: 'main', url: "${env.GIT_REPO}"
            }
        }
        stage('Install dependencies for tests') {
            steps {
             withCredentials([string(credentialsId:'envtxt',variable:'ENV_MS')]){
              catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                sh '''
                ##python3 -m venv venv
                #. venv/bin/activate
                #pip3 install -r requirements.txt
                cat ${ENV_MS} > env
                source env
                #SELENIUM_REMOTE_URL="http://10.0.1.17:4444" pytest --br ${BROWSER}  --numprocesses ${NUMPROCESS} --alluredir ${ALLURE_RESULTS}
                '''
              }
             }
            }
        }
        stage('Generate Allure Report') {
            steps {
                allure includeProperties: false, jdk: '', results: [[path: "${env.ALLURE_RESULTS}"]]
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}