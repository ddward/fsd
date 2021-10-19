## Hello Analytiks! :octocat:

This is the code repo for my financial data API. The API is live at [financialstatementdata.com](https://www.financialstatementdata.com), feel free to play around there and try out the code examples.

The API is split out into four microservices, each in it's own Docker container:
1. API
2. Database
3. Server
4. Tests

The value of splitting the app like this is that it leans into a continuous integration project flow. The same API, Database data, and Server containers are used in deployment and testing, and it's easy to spin up the test container on every deployment.

### 1. API
The API is built in the [Django](https://www.djangoproject.com/) and [Django REST framework](https://www.django-rest-framework.org/). Django is a great out of the box ready web framework with it's own ORM and database version control. The Django REST framework is a plugin that streamlines API development.

Take a look at the files in the fsd/api/api sub-folder for API backend logic. Currently the API serves one endpoint based on a company's stock ticker. Future releases will have more endpoints.

fsd/api/gui handles front-end logic, fsd/api/templates has html, and fsd/api/static houses css and javascript files.

fsd/api/common and fsd/api/config tie the app together and cover several security features.

Django, like all python backend web frameworks, requires a Web Server Gateway Interface (WSGI) to handle http requests. This app uses Uwsgi for that middleware which is configured in fsd/api/api/api_uwsgi.ini.

### 2. Database
This is a pretty straight forward postgres instance. It houses both auth data and the data that the API serves.

### 3. Server
Nginx is a popular web and reverse proxy server. nginx.conf within the nginx-proxy folder is configured to communicate with Uwsgi in the API container to serve the API to the world.

### 4. Tests
This container is used for black-box testing, a testing script lives at fsd/tests/tests.py. Starting this container automatically runs these tests.

## Thanks
Let me know if you have any questions about the code either via email or by phone.  -David
