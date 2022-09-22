pipeline {
    agent any
    stages{
     stage('build docker image'){
         steps{
           sh '''
                docker build -t slack --build-arg github_token=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 --build-arg slack_token=xoxb-497707237954-4067438317570-JIFOJ0laylCxfi7esa2q92yG --build-arg signing_secret=e8ea65bd94211948939e15ab4bd94d71 .
                aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 489994096722.dkr.ecr.us-east-2.amazonaws.com/reactapp-hasnain
                docker tag slack:latest 489994096722.dkr.ecr.us-east-2.amazonaws.com/reactapp-hasnain:latest
                docker push 489994096722.dkr.ecr.us-east-2.amazonaws.com/reactapp-hasnain:latest
                '''
           }
    }
    }
}