# DJANGO REST FRAMEWORK TEST PROJECT
It's a test project for:
https://github.com/cloudblue/connect-intern-program-python-task/blob/master/001_order_flow.md

Web Application that allows operating with orders by making http calls to the application's API.

###  HOW TO BUILD
Tests:
```
sudo docker build  -f ./orderFlow/mainapp/tests/Dockerfile .
```
Run local dev stand:
```
sudo docker-compose build app
sudo docker-compose up app
```