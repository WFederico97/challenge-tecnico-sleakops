# Challenge SleakOps

por Federico Wuthrich

## BACKEND

Se solicita elaborar un crud consumiendo a un JSON con informacion de facturacion de servicios de base de datos de AWS.
Algunos conceptos tecnicos fueron aplicados, como los siguientes:

- **Modelo**: Representado por los archivos `.py` en la carpeta `Models` y `Schemas`.
- **Controlador**: Representado por aquellos archivos que se encuentran en la carpeta `Routes`.
- **Vista**: Representada por los JSON que son devueltos en las respuestas del SWAGGER de FastAPI.
- **Arquitectura Modular**: Todos los módulos fueron separados en capas, permitiendo una facilidad de aislamiento de responsabilidades y haciendo que el código sea escalable.
- **Patrón Repository**: Se aplicó el patrón de desarrollo repository para abstraer la lógica de acceso a los datos del resto de la aplicación.

## CONTENEDORIZACIÓN

Realizada con Docker y compuesta con Docker-Compose.

## BASE DE DATOS

Se utilizó el motor de PostgreSQL. A su vez, en el archivo `database.py` se ejecuta un script con la creación de la base de datos para que se realice antes de inicializar la app. El script puede encontrarse en la carpeta `Scripts/init.sql`.

### PASO A PASO

1. Una vez inicializada la app, el proceso de DDL ya se encuentran realizado y por ende , la base de datos ya se encuentra lista para operar.
2. Para poder poblar la base de datos , es necesario hacer la llamada al endpoint `loadData/load-aws-data`.
3. Una vez tengamos nuestra base de datos con registros , vamos a poder consultar, crear , modificar y eliminar registros a traves de sus respectivos endpoints

## Configuración del Proyecto

### Requerimientos

- Python 3.13 o superior
- PostgreSQL
- Docker y Docker Compose (opcional, para levantar el proyecto en contenedores)

### Configuración Local (Windows y Mac)

1. **Clonar el repositorio:**

    ```bash
    git clone https://github.com/WFederico97/ED-MACHINA.git
    cd challenge-tecnico-sleakops
    ```

2. **Crear un entorno virtual e instalar dependencias:**

    ```bash
    python -m venv .env
    source .env/bin/activate  # Para Mac y Linux
    .env\Scripts\activate     # Para Windows
    source .env/Scripts/Activate #GIT Bash console
    pip install -r requirements.txt
    ```

3. **Levantar la base de datos y la API:**

    Asegúrate de tener PostgreSQL corriendo, el entorno activado y ejecuta:

    ```bash
    uvicorn main:app --reload --port 8000
    ```

### Configuración con Docker

1. **Clonar el repositorio:**

    ```bash
    git clone https://github.com/WFederico97/ED-MACHINA.git
    cd challenge-tecnico-sleakops
    ```

2. **Levantar los contenedores:**

    ```bash
    docker-compose up --build
    ```

    La API estará disponible en [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Estructura del Proyecto

```text
challenge-tecnico-sleakops/
├── .gitignore
├── awsPrices.json
├── Db/
│   ├── db.py
├── main.py
├── Models/
│   ├── CoreModels/
│   │   ├── PriceDimensionsModel.py
│   │   ├── ProductsModel.py
│   │   ├── TermsModel.py
│   ├── SupportModels/
│   │   ├── DatabaseEnginesModel.py
│   │   ├── InstanceTypesModel.py
│   │   ├── LicenseModels.py
│   │   ├── LocationsModel.py
│   │   ├── OfferingClasses.py
│   │   ├── PurchaseOptionsModel.py
│   │   ├── ServicesModel.py
│   │   ├── TermTypesModel.py
├── README.md
├── Repositories/
│   ├── ProductRepository.py
├── requirements.txt
├── Routes/
│   ├── LoadAwsDataRoute.py
│   ├── ProductRoutes.py
├── Schemas/
│   ├── Product.py
├── Services/
│   ├── DataLoaderService.py
│   ├── ProductService.py
├── tests/

```

---

## English

### BACKEND

The challenge was make a crud api that consumes data from a JSON with AWS DB Pricing service.
A few technical concepts were applied like :

- **Model**: Represented by the `.py` files in the `Models` and `Schemas` folders.
- **Controller**: Represented by the files located in the `Routes` folder.
- **View**: Represented by the JSONs returned in the responses from FastAPI's SWAGGER.
- **Modular Architecture**: All modules were separated into layers to facilitate the isolation of responsibilities and make the code scalable.
- **Repository Pattern**: The repository development pattern was applied to abstract data access logic from the rest of the app.
- **Single Responsibility Principle**: Where each class has its single purpose such as Routes, Services, and Repositories.

### CONTAINERIZATION

Performed with Docker and composed using Docker-Compose.

### DATABASE

PostgreSQL was used as the engine, and a script with the database creation runs in the `database.py` file before initializing the app. The script can be found in the `Scripts/init.sql` folder.

### WALKTHROUGH

1. Once the app is initialized, the DDL process is already made thus the db is ready to interact with.
2. Para poder poblar la base de datos , es necesario hacer la llamada al endpoint `loadData/load-aws-data`. To populate the db with data , it is necessary call the  `loadData/load-aws-data` endpoint.
3. Once the db is already populated with registers, you can interact with the CRUDs api endpoints.

## Project Setup

### Requirements

- Python 3.13 or higher
- PostgreSQL
- Docker and Docker Compose (optional, for running the project in containers)

### Local Setup (Windows and Mac)

1. **Clone the repository:**

    ```bash
    git clone https://github.com/WFederico97/ED-MACHINA.git
    cd challenge-tecnico-sleakops
    ```

2. **Create a virtual environment and install dependencies:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # For Mac and Linux
    venv\Scripts\activate     # For Windows
    source .env/Scripts/Activate #GIT Bash console
    pip install -r requirements.txt
    ```

3. **Start the database and the API:**

    Make sure PostgreSQL is running, your environment is active and execute:

    ```bash
    uvicorn main:app --reload --port 8000
    ```

### Docker Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/WFederico97/ED-MACHINA.git
    cd challenge-tecnico-sleakops
    ```

2. **Start the containers:**

    ```bash
    docker-compose up --build
    ```

    The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Project Structure

```text
challenge-tecnico-sleakops/
├── .gitignore
├── awsPrices.json
├── Db/
│   ├── db.py
├── main.py
├── Models/
│   ├── CoreModels/
│   │   ├── PriceDimensionsModel.py
│   │   ├── ProductsModel.py
│   │   ├── TermsModel.py
│   ├── SupportModels/
│   │   ├── DatabaseEnginesModel.py
│   │   ├── InstanceTypesModel.py
│   │   ├── LicenseModels.py
│   │   ├── LocationsModel.py
│   │   ├── OfferingClasses.py
│   │   ├── PurchaseOptionsModel.py
│   │   ├── ServicesModel.py
│   │   ├── TermTypesModel.py
├── README.md
├── Repositories/
│   ├── ProductRepository.py
├── requirements.txt
├── Routes/
│   ├── LoadAwsDataRoute.py
│   ├── ProductRoutes.py
├── Schemas/
│   ├── Product.py
├── Services/
│   ├── DataLoaderService.py
│   ├── ProductService.py
├── tests/

```
