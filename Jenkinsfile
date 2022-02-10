pipeline {
    agent none
    stages {

        stage('Code Quality Test') {

            parallel{

                stage('Score Code Quality Test') {

                    agent {
                        dockerfile {
                            filename 'Dockerfile'
                            dir 'tests/1_code_quality_test'
                        }
                    }

                    steps{
                        sh 'pylint --disable=C,R,W development/models/Sklearn_GBT/Sklearn_GBTScore.py'
                    }

                    post {
                        success {
                            echo "Score code file successfully passed the Code Quality Test!"
                        }
                        failure {
                            echo "Code failed the quality test, please see logs."
                        }
                    }
                }
            }
        }
        stage('Code Validation Test') {

            parallel {

                stage('Validate Score Code') {

                    agent {
                        docker {
                            image 'python:3-alpine' 
                        }
                    }

                    steps {
                        sh 'python -m py_compile development/models/Sklearn_GBT/Sklearn_GBTScore.py'
                    }

                    post {

                    success {
                            echo 'Score code file successfully validated!'
                        }

                    failure {
                            echo 'Code failed the Validation test, please see logs.'
                        }
                    }
                }
            }
        }  
    }
}