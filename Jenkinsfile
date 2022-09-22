pipeline {
    agent any
    stages{
     stage('Initialize'){
     steps {
     script{
        def dockerHome = tool 'myDocker'
        echo "${readProp['dockerHome']}"
        env.PATH = "${dockerHome}/bin:${env.PATH}"
        }}
    }
     stage('build docker image'){
         steps{
           sh '''
                docker build -t slack --build-arg github_token=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 --build-arg slack_token=xoxb-497707237954-4067438317570-JIFOJ0laylCxfi7esa2q92yG --build-arg signing_secret=e8ea65bd94211948939e15ab4bd94d71 .
                '''
           }
    }
    }
}