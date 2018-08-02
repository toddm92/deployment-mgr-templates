```
  title: VM Template
  author: Todd
  description: |
    Creates and deploys one VM into each specified zone.
    Subnetwork naming convention: network + -sub1- + region
  version: 2.0
```

#### deploy..
```
gcloud deployment-manager deployments create my-deployment --config config.yaml
```

#### tear down..
```
gcloud deployment-manager deployments delete my-deployment
```
