To Run Test Env:

```
# rebuild containers
docker-compose -f docker-compose.test.yml -p ci down --rmi all
docker-compose -f docker-compose.test.yml -p ci build
docker-compose -f docker-compose.test.yml -p ci up -d

# attach output to terminal and run tests:
docker start ci_test_1 -a
```

To Run Prod Env:

```
# rebuild containers
docker-compose -f docker-compose.yml -p ci down --rmi all
docker-compose -f docker-compose.yml -p ci build
docker-compose -f docker-compose.yml -p ci up -d
```