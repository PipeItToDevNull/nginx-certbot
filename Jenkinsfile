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
        TAG = getEnvName(env.BRANCH_NAME)
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
                    podman build -t nginx:${TAG} .
                    podman images
                '''
            }
        }
    }
}
