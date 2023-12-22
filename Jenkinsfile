pipeline {
    triggers {
        cron('@midnight')
    }
    agent {
        label 'linux && podman && x64'
    }
    environment {
        TAG = "${env.BRANCH_NAME == "jenkins" ? "latest" : "${BRANCH_NAME}"}"
        IMAGE = "nginx"
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
                    podman build -t ${IMAGE}:${TAG} .
                    podman images
                '''
            }
        }
        stage('SBOM generation') {
            sh'''
                podman run --rm anchore/syft -o spdx-json ${IMAGE}:${TAG} > ${IMAGE}.${TAG}.spdx.json
                ls
            '''
        }
    }
}
