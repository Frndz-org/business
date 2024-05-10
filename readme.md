# Frndz Business Microservice

Business microservice for Frndz.org Ecosystem

# Environment Variables

The variables can be provided via `.env` file or added to docker environments
### **`SECRET_KEY`**

Default: ''  
A secret key for a particular Django installation. This is used to provide cryptographic signing, and should be set to a
unique, unpredictable value.

### **`DEBUG`**

Default: False  
A boolean that turns on/off debug mode.

### **`DEFAULT_CACHE_TIMEOUT`**

Default: 800  
Cache TTL on this microservice

### **`SUPERUSER_PASSWORD`**

Default: ''  
Set superuser password

### **`SUPERUSER_EMAIL`**

Default: ''  
Set superuser email address

### **`SUPERUSER_USERNAME`**

Default: ''  
Set superuser username

### **`ALLOWED_HOSTS`**

Default: []  
A list of strings representing the host/domain names that this service app can serve

### **`DATABASE_NAME`**

Default: ''  
Database this service app can connect to

### **`DATABASE_USERNAME`**

Default: ''  
Database Username this service app can connect to a database

### **`DATABASE_PASSWORD`**

Default: ''  
Database Password this service app can connect to a database

### **`DATABASE_HOST`**

Default: 'localhost'  
Database Server this django app can connect to

### **`DATABASE_PORT`**

Default: '5432'  
Database Server Port this service app can connect to

### **`REDIS_HOST`**

Default: ''  
Redis Server this service app can connect to

### **`REDIS_PORT`**

Default: ''  
Redis Server Port this service app can connect to

### **`REDIS_PASSWORD`**

Default: ''  
Redis Server Password this service app can use to connect to the redis server

### **`CORS_ALLOW_ALL_ORIGINS`**

Default: False  
Set `True` if this service app should allow connection all `http origins`

### **`CORS_ALLOWED_ORIGINS`**

Default: []  
A list of origins that are authorized to make cross-site HTTP requests.

### **`RABBITMQ_HOST`**

Default: ''  
Rabbitmq Server this django app can connect to

### **`RABBITMQ_PORT`**

Default: ''  
Rabbitmq Server Port this service app can connect to

### **`RABBITMQ_USERNAME`**

Default: ''  
Rabbitmq Server Username this service app can connect to

### **`RABBITMQ_PASSWORD`**

Default: ''  
Rabbitmq Server Password this service app can connect to

### **`RABBITMQ_VIRTUAL_HOST`**

Default: ''  
Rabbitmq Server Virtual Host this service app can connect to

### **`SENTRY_DSN`**

Default: ''  
Tells a Sentry SDK where to send events so the events are associated with the correct project.

### **`KAFKA_SERVER`**

Default: **'localhost:9092'**  
Kafka Server Address to publish and subscribe event data