pipeline {
    agent any
   environment{
        aws_access_key_id = credentials('aws_access_key_id')
        aws_secret_key = credentials('aws_secret_access_key')
    }

    stages {
        stage('Hello') {
            steps {
                sh '''
                export AWS_REGION=us-east-1
                export AWS_ACCESS_KEY_ID=${aws_access_key_id}
                export AWS_SECRET_ACCESS_KEY=${aws_secret_key}
                echo AWS_ACCESS_KEY_ID
                echo AWS_SECRET_ACCESS_KEY
                '''
                }
            }
        }
    }