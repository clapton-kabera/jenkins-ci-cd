pipeline {
  agent any
  
  options {
    skipDefaultCheckout()
    timeout(time: 15, unit: 'MINUTES')
    disableConcurrentBuilds()
  }

  environment {
    IMAGE = 'kabera/flask-app'
    EC2_HOST = '<EC2 IP Address>'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    stage('Build') {
      steps {
        sh 'python3 -m venv .venv'
        sh '.venv/bin/pip install -r requirements-dev.txt'
      }
    }
    stage('Test') {
      steps {
        sh '.venv/bin/python3 -m pytest --junitxml=reports/junit_report.xml'

      }
      post {
        always {
          junit 'reports/junit_report.xml'
        }
      }
    }
    stage('Docker Build') {
      steps {
        sh 'docker build -t $IMAGE:$BUILD_NUMBER -t $IMAGE:latest .'
      }
    }
    stage('Push Image') {
      steps {
        withCredentials([usernamePassword(
          credentialsId: 'registry_creds',
          usernameVariable: 'REG_USER',
          passwordVariable: 'REG_PASS'
        )]) {
          sh 'echo "$REG_PASS" | docker login -u "$REG_USER" --password-stdin'
          sh 'docker push $IMAGE:$BUILD_NUMBER'
          sh 'docker push $IMAGE:latest'
        }
      }
      post {
        always {
          sh 'docker logout'
        }
      }
    }
    stage('Deploy') {
      steps {
        sshagent(credentials: ['ec2_ssh']) {
          sh '''
            SSH="ssh -o StrictHostKeyChecking=accept-new ec2-user@$EC2_HOST"
            $SSH "docker pull $IMAGE:$BUILD_NUMBER"
            $SSH "docker rm -f flask-app || true"
            $SSH "docker run -e APP_VERSION=$BUILD_NUMBER -d --name flask-app --restart unless-stopped -p 80:5000 $IMAGE:$BUILD_NUMBER"
            $SSH "docker image prune -af"
          '''
        }
      }
    }
  }
  post {
    success {
      echo "Deployment #${BUILD_NUMBER} successful..."
    }
    failure {
      echo "Deployment #${BUILD_NUMBER} failed..."
    }
    cleanup {
      sh '''
        docker rmi $IMAGE:$BUILD_NUMBER $IMAGE:latest || true
        docker image prune -f
      '''
      deleteDir()
    }
  }
}
