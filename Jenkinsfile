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
        
        stage('Unit Test for Score code') {

            agent {
                    docker {
                        image 'docker-registry-frascb.unx.sas.com/modelops_pyunit'
                    }
                }

            steps {
                sh 'python tests/2_unit_test/unit_test_pipeline.py development/models/Sklearn_GBT/Sklearn_GBT.pickle data/test.csv result.csv'
            }

            post {

                success {
                        echo 'Score code file successfully passed Unit Test!'
                    }

                failure {
                        echo 'Code failed the Unit test, please see logs.'
                    }
            }

        }

        stage('Integration test for Score code') {

            agent any

            steps {

                script {

                    docker.image('docker-registry-frascb.unx.sas.com/modelops_model_container').withRun('-p 9999:9999') { test ->
                        docker.image('docker-registry-frascb.unx.sas.com/modelops_model_container').inside("-u 0 --entrypoint=/pybox/app/startServer.sh --link ${test.id}:test_score") {
                        }

                        docker.image('docker-registry-frascb.unx.sas.com/modelops_exec_container').inside("--workdir=/home/test --link ${test.id}:test_score") {
                            
                                env.TOKEN = sh(script:"curl -s test_score:9999/", returnStdout: true).trim()
                                sh(returnStdout: true, script: "if [ ${env.TOKEN} == 'pong' ]; then echo 'Instance is up...'; else echo 'Something is wrong with container instance'; exit 1; fi")
                                env.EXECUTION_ID = sh(returnStdout: true, script:"curl -s --form file=@tests/3_integration_test/exec_container/test.csv --form press=OK test_score:9999/executions | jq -r '.id'").trim()
                                sh("echo ${env.EXECUTION_ID}")
                                sh(returnStdout: true, script: "if [ ! -z ${env.EXECUTION_ID} ]; then curl -s -o tests/3_integration_test/exec_container/result.csv test_score:9999/query/${env.EXECUTION_ID}; else echo 'Something is wrong with container instance'; exit 1; fi")
                                sh(returnStdout: true, script: "curl -s -o tests/3_integration_test/exec_container/result.log test_score:9999/query/${env.EXECUTION_ID}/log")
                                sh(returnStdout: true, script: "curl -s -o tests/3_integration_test/exec_container/system.log test_score:9999/system/log")
                                sh("cat tests/3_integration_test/exec_container/result.csv")
                                sh("cat tests/3_integration_test/exec_container/result.log")
                                sh("tail -5 tests/3_integration_test/exec_container/system.log")
                            }
                    }
                }
            }

            post {

            success {
                    echo 'Score code file successfully passed Unit Test!'
                }

            failure {
                    echo 'Code failed the Unit test, please see logs.'
                }
            }

        }
  
    }
}
