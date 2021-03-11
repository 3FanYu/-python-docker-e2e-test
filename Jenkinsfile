pipeline{
    agent{
        dockerfile true
    }
    stages{
        stage('set up'){
            steps{
                sh 'docker build -t my-python-app .'
                sh 'docker run -it --rm -v tempdata:/data --name my-running-app my-python-app'
            }
        }
    }
}