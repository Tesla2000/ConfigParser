## Running

You can run script with docker or python

### Python
```shell
python main.py --config_file config_parser/config_sample.toml
```

### Cmd
```shell
poetry install
poetry run config_parser
```

### Docker
```shell
docker build -t ConfigParser .
docker run -it ConfigParser /bin/sh
python main.py
```
