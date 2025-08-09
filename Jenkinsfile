pipeline {
    agent any
    stages {
        stage('Hello') {
            steps {
                echo 'Hello Jenkins!'
            }
        }
        stage('Check Files') {
            steps {
                sh 'ls -la /workspace'
            }
        }
        stage('Restart App') {
            steps {
                sh '''
                    cd /workspace
                    docker-compose restart fastapi-app
                    echo "App restarted!"
                '''
            }
        }
    }
}