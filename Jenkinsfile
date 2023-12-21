/* 
    This should only act on master and tags
    Build :nightly from the latest commit of master
    Build the last two tags that are created
    Mark the newest tag :latest
*/

pipeline {
    triggers {
        cron('@midnight')
    }
    agent {
        label 'linux && podman && x64'
    }
    environment {
        TAG = "${env.BRANCH_NAME == "jenkins" ? "latest" : "${BRANCH_NAME}"}"
    }
    stages {
        stage('Cloning repo') {
            steps {
                checkout scm
            }
        }
        stage('Building image') {
            steps {
                sh '''
                    podman build -t nginx:${TAG} .
                    podman images
                '''
            }
        }
    }
}
