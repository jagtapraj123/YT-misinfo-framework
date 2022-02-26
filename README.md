# YouTube Misinformation Framework

## Objective

Software for deploying YouTube video classification models and collecting crowdsourcing dataset.

## Installation

1. Create virtual environment.
   - **Using Conda**

        ```sh
        conda create --name yt_misinfo python=3.9
        conda activate yt_misinfo
        ```

        Anything above python=3.7+ would be ok.
   - **Using virtualenv**

        ```sh
        virtualenv venv_yt_misinfo
        source venv_yt_misinfo/bin/activate
        ```

2. Install Python Requirements.

    ```sh
    pip install -r requirements.txt
    ```

3. Install NPM Requirements.

    ```sh
    cd frontend
    npm i
    ```

## Database Setup

The database is provided as a json file in `initial_dataset` directory. Run `setup.py` file to configure the database to latest data.

```sh
python initial_dataset/setup.py
```

## Run Website and Server

The framework consists of two different apps that need to be run as separate programs.

- ### Run Backend (Flask App)

    ```sh
    python app.py
    ```

- ### Run Frontend (React App)

    ```sh
    cd frontend
    npm start
    ```
