# Test Fullstack Tech-K

## Instrucciones de uso
---
Basta con ejecutar el siguiente comando en el directorio principal:

```bash
docker-compose up --detach
```

Para correr los tests del backend hay que ir al directorio `./techk/` y ejecutar el siguiente comando:
> Se toma como supuesto que se sabe instalar pyenv y pipenv

```bash
pipenv install --python $(pyenv root)/versions/3.7.4/bin/python -r requirements.txt
pipenv run tox
```

## Consideraciones

- Se considero que era mejor dejar separados los ambientes de frontend y backend, ya que en producción recomendaría dejarlo de esta manera si se quiere sacar el mayor provecho a cada una de estas partes cuando ya se tenga un flujo grande de usuarios y así tambien evitar lidiar con un monolito que luego habría que separar.
