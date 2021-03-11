pipeline {
    agent {
        dockerfile true
    }
    stages {
        stage('prep') {
            steps {
                sh 'python --version'
            }
        }
        stage('run'){
            steps{
                sh 'python test.py 3樊 fanfanfan9453@gmail.com 0987654321'
            }
        }
        stage('done'){
            steps{
                sh 'echo All Done!'
            }
        }
    }
}
