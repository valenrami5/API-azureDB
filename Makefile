IMAGE_NAME := hr-management-api
ACR_NAME := hrmanagementapiregistry

build:
	docker build --platform linux/amd64 -t $(IMAGE_NAME):latest .

login:
	az login
	az acr login --name $(ACR_NAME)
push:
	make build
	docker tag $(IMAGE_NAME):latest $(ACR_NAME).azurecr.io/$(IMAGE_NAME):latest
	docker push $(ACR_NAME).azurecr.io/$(IMAGE_NAME):latest