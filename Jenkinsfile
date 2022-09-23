pipeline {
    agent any
    stages{
     stage('build docker image'){
         steps{
           sh '''
                export AWS_REGION=${aws_region}
                export AWS_ACCESS_KEY_ID=${aws_access_key_id}
                export AWS_SECRET_ACCESS_KEY=${aws_secret_key}
                aws configure set aws_access_key_id "${AWS_ACCESS_KEY_ID}" && aws configure set aws_secret_access_key "${AWS_SECRET_ACCESS_KEY}" && aws configure set region "${AWS_REGION}"
                echo AWS_ACCESS_KEY_ID
                '''
           }
    }
    }
}