pipeline {
    agent any
   environment{
        aws_access_key_id = credentials('aws_access_key_id')
        aws_secret_key = credentials('aws_secret_access_key')
    }

    stages {
        stage('making docker image'){
            steps{
            sh '''
                docker build -t slack --build-arg github_token=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 --build-arg slack_token=xoxb-497707237954-4067438317570-JIFOJ0laylCxfi7esa2q92yG --build-arg signing_secret=e8ea65bd94211948939e15ab4bd94d71 .

            '''
            }
        }

        stage('aws_login') {
            steps {
                sh '''
                export AWS_REGION=us-east-2
                export AWS_ACCESS_KEY_ID=${aws_access_key_id}
                export AWS_SECRET_ACCESS_KEY=${aws_secret_key}
                aws configure set aws_access_key_id "${AWS_ACCESS_KEY_ID}" && aws configure set aws_secret_access_key "${AWS_SECRET_ACCESS_KEY}" && aws configure set region "${AWS_REGION}"

                '''
                }
            }
        stage ('pushing to ecr'){
        steps{
        sh '''
         aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 489994096722.dkr.ecr.us-east-2.amazonaws.com/reactapp-hasnain
                docker tag slack:latest 489994096722.dkr.ecr.us-east-2.amazonaws.com/reactapp-hasnain:latest
                docker push 489994096722.dkr.ecr.us-east-2.amazonaws.com/reactapp-hasnain:latest
        '''
        }
        }
        stage ('accessing cluster'){
        steps{
        sh '''
        aws eks update-kubeconfig --region us-east-2 --name Hasnain-Jenkins
        kubectl apply -f manifest.yml
        echo kubectl get pods

        '''
        }
        }
    }
}