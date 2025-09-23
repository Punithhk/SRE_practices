pipeline {
  agent any
  stages {
    stage('Checkcode') {
      steps {
        git(url: 'https://github.com/Punithhk/SRE_practices', branch: 'main')
      }
    }

    stage('Checkfiles') {
      parallel {
        stage('Checkfiles') {
          steps {
            sh 'dir'
          }
        }

        stage('npm initialize') {
          steps {
            sh 'cd backend/ && npm install '
          }
        }

      }
    }

  }
}