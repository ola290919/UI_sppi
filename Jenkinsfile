pipeline {
    agent any
    parameters {
        string(name: 'BROWSER', defaultValue: 'chrome', description: 'Browser name')
        string(name: 'NUMPROCESS', defaultValue: '1', description: 'Number of processes')
    }
    environment {
        GIT_REPO = 'https://github.com/ola290919/UI_sppi.git'
        ALLURE_RESULTS = 'allure-results'
//         EXECUTOR_URL = "${params.EXECUTOR_URL}"
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
              catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --no-cache-dir virtualenv
                pip3 install -r requirements.txt
                pip install playwright
                playwright install
                pytest --browser ${BROWSER}  --numprocesses ${NUMPROCESS} --alluredir ${ALLURE_RESULTS}
                '''
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