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

                    node {

                        docker.image('docker-registry-frascb.unx.sas.com/modelops_model_container').withRun('-p 9999:9999') { test ->

                            docker.image('docker-registry-frascb.unx.sas.com/modelops_model_container').inside("-u 0 --entrypoint=/pybox/app/startServer.sh --link ${test.id}:test_score") {
                            }

                            docker.image('docker-registry-frascb.unx.sas.com/modelops_exec_container').inside("--workdir=/home/test --link ${test.id}:test_score") {
                                sh("echo toto")
                            }

                        }

                    }

                }

                script {

                    node {
                        checkout scm
                        docker.image('mysql:5').withRun('-e "MYSQL_ROOT_PASSWORD=my-secret-pw"') { c ->
                            docker.image('mysql:5').inside("--link ${c.id}:db") {
                                /* Wait until mysql service is up */
                                sh 'while ! mysqladmin ping -hdb --silent; do sleep 1; done'
                            }
                            docker.image('centos:7').inside("--link ${c.id}:db") {
                                /*
                                * Run some tests which require MySQL, and assume that it is
                                * available on the host name `db`
                                */
                                sh 'make check'
                            }
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
