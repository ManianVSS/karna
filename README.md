# karna

A resource inventory, allocation and management system.

### **Development Setup**

##### **Installing python dependencies on Ubuntu**<br>

##### **Pre-Requisites**</br>
Python 3, pip and libpq-dev </br>
> sudo apt install libpq-dev</br>
> cd backend</br>
> pip install -r requirements.txt</br>

##### **Creating and Migrating DB Schema**</br>

> cd backend</br>
> ./migrate.sh</br>

##### **Running server**

> cd backend</br>
> ./runserver.sh</br>

Admin console should be up on http://localhost:8000/admin

### **Production Setup**

##### **Installing python dependencies and postgres on Ubuntu**<br>
Note: Create files referring to the .example files in root directory</br>
##### **Pre-Requisites**</br>
Python 3, pip , postgres database and libpq-dev </br>
> sudo apt install libpq-dev</br>
> cd backend</br>
> pip install -r requirements.txt</br>

##### **Creating Postgres production DB and schema one time**</br>

> ./createdb.sh

##### **Migrating DB Schema for changes**</br>

> ./migrate.sh

##### **Running server**</br>

> ./runserver.sh

Admin console should be up on http://localhost:8000/admin

### **Building Dashboard**

##### **Pre-Requisites**</br>

Install latest nodejs using official documentation</br>
Note: Ubuntu package manager has older version of Node.. Please use latest from official website.</br>
Installing yarn</br>
> npm install yarn</br>

##### **Build**</br>

> cd webui</br>
> yarn install</br>
> yarn build </br>
> cd ../backend/</br>
> ln -sf ../webui/build .</br>
> cd ..</br>
