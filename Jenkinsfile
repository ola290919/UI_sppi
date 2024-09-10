pipeline {
    agent any
    parameters {
        string(name: 'SELENIUM_REMOTE_URL', defaultValue: 'http://10.0.1.17:4444', description: 'remote url')
        string(name: 'NUMPROCESS', defaultValue: '1', description: 'Number of processes')
    }
    environment {
        GIT_REPO = 'https://github.com/ola290919/UI_sppi.git'
        ALLURE_RESULTS = 'allure-results'
        NUMPROCESS = "${params.NUMPROCESS}"
        SELENIUM_REMOTE_URL = "${params.SELENIUM_REMOTE_URL}"
    }
    stages {
        stage('Clone repository') {
            steps {
                git branch: 'main', url: "${env.GIT_REPO}"
            }
        }
        stage('Install dependencies for tests') {
            steps {
             withCredentials([file(credentialsId:'env_ms',variable:'ENV_MS')]){
              catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip3 install -r requirements.txt
                pip3 install pytest-playwright
                cp ${ENV_MS} .env
                SELENIUM_REMOTE_URL=${SELENIUM_REMOTE_URL} pytest --numprocesses ${NUMPROCESS} --alluredir ${ALLURE_RESULTS}
                rm -f .env
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