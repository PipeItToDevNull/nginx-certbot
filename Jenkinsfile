/* 
    This should only act on master and tags
    Build :nightly from the latest commit of master
    Build the last two tags that are created
    Mark the newest tag :latest
*/

pipeline {
    agent {
        label 'linux && podman && x64'
    }
    environment {
        TAG = 'nightly'
    }
    stages {
        stage('Cloning repo...') {
            steps {
                checkout scm
            }
        }
        stage('Stage 1') {
            steps {
                echo 'Building...'
                sh '''
                    podman system prune -a -f
                    podman build -t nginx:${TAG} .
                '''
            }
        }
    }
}
