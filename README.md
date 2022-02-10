# Modelops Project

This project aims to showcase a CI/CD approach for a Data Scientist developing models in a Python environment on SAS Viya (3.5). It is inspired from this project https://gitlab.sas.com/ivnard/modelops-with-sas-model-manager-and-sas-workflow-manager

## Troubleshooting

- Github push/pull blocked in internal network: https://stackoverflow.com/questions/7953806/github-ssh-via-public-wifi-port-22-blocked
- Github webhook with a local deployment of Jenkins: https://medium.com/@joydeep56053/continuous-integration-using-jenkins-blueocean-github-ubuntu-robotframework-5b800ae1df8c

## Set up Private Docker Publishing Destinations in SAS Model Manager

[Tutorial Video](https://www.youtube.com/watch?v=tc6E90A5kyM)

### Configure Docker Host

- Enable remote connections to Docker Host: https://dockerlabs.collabnix.com/beginners/components/daemon/access-daemon-externally.html

### Set Up Private Docker Registry

- Set up Docker Registry host: https://www.digitalocean.com/community/tutorials/how-to-set-up-a-private-docker-registry-on-ubuntu-20-04
- Enable user/password security activation or not ?
- Secure Nginx with Let's Encrypt: https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-20-04
- Use a static Public IP
- Assign a Hostname http://names.na.sas.com/
- Enable HTTP/HTTPS access on Azure: https://docs.microsoft.com/en-us/answers/questions/11173/unable-to-access-my-public-ip-using-port-80.html

### Run scripts for creating the Docker destination and base images

- Scripts: https://github.com/sassoftware/model-management-resources/tree/main/addons

## Model Inference for models in Docker Container

- sample of score code files: https://github.com/sassoftware/model-container-recipes/blob/master/model-image-cli/ScoreFileTutorial.md
- test script: https://github.com/sassoftware/model-container-recipes/blob/master/model-image-cli/test/test_model_image.sh