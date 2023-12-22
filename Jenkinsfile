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
            steps {
                sh'''
                    podman run --rm anchore/syft -o spdx-json ${IMAGE}:${TAG} > ${IMAGE}_${TAG}.spdx.json
                    ls
                '''
            }
        }
        stage('Testing') {
            steps {
                sh'''
                    podman run --rm -v ./:/path ghcr.io/gitleaks/gitleaks:latest detect --redact --report-path gitleaks.json --source="/path"                 
                '''
            }
        }
    }
}
