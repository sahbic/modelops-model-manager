# create image
docker build --no-cache --progress=plain -f .\tests\3_integration_test\model_container\Dockerfile .\tests\3_integration_test\model_container -t modelops_model_container

# test
docker run --rm -it modelops_model_container /bin/bash

# push to registry
docker tag modelops_model_container docker-registry-frascb.unx.sas.com/modelops_model_container
docker push docker-registry-frascb.unx.sas.com/modelops_model_container