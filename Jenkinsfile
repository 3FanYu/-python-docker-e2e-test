pipeline {
    agent {
        dockerfile true
    }
    stages {
        stage('stepOne') {
            steps {
                sh 'python --version'
                sh 'python test.py'
            }
        }
    }
}
