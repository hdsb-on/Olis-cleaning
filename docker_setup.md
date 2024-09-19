1. Build the docker image

```
docker build -t olis_cleaning_env .
```

2. Run the image interactively, with bash

```
docker run -it olis_cleaning_env -c "bash"
```

3. We can now run our script from the shell in docker, with the specified environment