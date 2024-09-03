# Laboratoire 1

Le projet utilise python 3.10.0

## Créer un environnement virtuel sur windows

```bash
python -m venv venv
```

## Activer l'environnement virtuel

```bash
source venv/bin/activate
```

## Installer les dépendances

```bash
pip install -r requirements.txt
```

## Base de données MongoDB, version 7.0.5

https://www.mongodb.com/try/download/community

dans l'onglet MongoDB Community Server, clicker sur Select Package et choisir la version 7.0.5
installer MongoDB sur votre machine avec l'installeur

Par défault, le port utilisé par MongoDB est le 27017, si vous l'avez changé, il faut le modifier
dans le fichier __init__.py :

```python
app.config["MONGO_URI"] = "mongodb://localhost:27017/flaskr"
```

## Lancer le serveur en mode debug (pour le développement)

Il faut remplacer la fonction restart_with_reloader dans le fichier reloader.py de Flask par la suivante:
**....\Lib\site-packages\werkzeug_reloader.py** 
```bash
 def restart_with_reloader(self) -> int:
        """Spawn a new Python interpreter with the same arguments as the
        current one, but running the reloader thread.
        """
        while True:
            _log("info", f" * Restarting with {self.name}")
            args = _get_args_for_reloading()
            new_environ = os.environ.copy()
            new_environ["WERKZEUG_RUN_MAIN"] = "true"

            ## WORK-AROUND FIX ##
            args = [f'""{a}""' if ' ' in a else a for a in args]

            exit_code = subprocess.call(args, env=new_environ, close_fds=False)

            if exit_code != 3:
                return exit_code
 ```

Fichier de config:
```bash
<component name="ProjectRunConfigurationManager">
  <configuration default="false" name="flask_config" type="PythonConfigurationType" factoryName="Python">
    <module name="analyseurPisicine" />
    <option name="INTERPRETER_OPTIONS" value="" />
    <option name="PARENT_ENVS" value="true" />
    <envs>
      <env name="PYTHONUNBUFFERED" value="1" />
      <env name="FLASK_APP" value="flaskr" />
      <env name="FLASK_ENV" value="development" />
    </envs>
    <option name="SDK_HOME" value="" />
    <option name="WORKING_DIRECTORY" value="$PROJECT_DIR$" />
    <option name="IS_MODULE_SDK" value="true" />
    <option name="ADD_CONTENT_ROOTS" value="true" />
    <option name="ADD_SOURCE_ROOTS" value="true" />
    <option name="SCRIPT_NAME" value="flask" />
    <option name="PARAMETERS" value="run --debug" />
    <option name="SHOW_COMMAND_LINE" value="false" />
    <option name="EMULATE_TERMINAL" value="false" />
    <option name="MODULE_MODE" value="true" />
    <option name="REDIRECT_INPUT" value="false" />
    <option name="INPUT_FILE" value="" />
    <method v="2" />
  </configuration>
</component>
```bash

```bash
flask --app flaskr run --debug
```

## Fonctionnement:

### on accède à la page d'accueil pour s'inscrire
```bash
http://127.0.0.1:5000/auth/register
```
### on accède à la page de login pour se connecter
```bash
http://127.0.0.1:5000/auth/login
```

### lorsqu'on clique sur connexion, on est redirigé vers la page d'accueil
```bash
http://127.0.0.1:5000/accueil/
```


