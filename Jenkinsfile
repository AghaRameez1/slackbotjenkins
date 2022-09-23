pipeline {
    agent any
    stages{
     stage('AWS LOGIN'){
         steps{
         withAWS(credentials: 'aws creds', region: 'us-west-1') {
           sh '''
           aws config
              '''
           }
           }
    }
    }
}