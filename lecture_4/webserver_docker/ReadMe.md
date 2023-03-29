# Run

# 1. Build the image

```bash
    docker build -t webserver_python .
```

# 2. Run the container
```bash
docker run -p 8080:7777 webserver_python
```