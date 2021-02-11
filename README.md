# HousePrices
## Instalation

Initialice the virtual Enviroment, and activate:

```bash
py -m venv venv
venv\scripts\activate
```

at the end we have to deactivate the virtual enviroment with the command:

```bash
deactivate
```

We need to install the following python libraries into the virtual enviroment: 

* Twisted
* Scrapy
* Autopep8

```bash
pip install Twisted Scrapy Autopep8
```

if this doesn't work we have to download the library from [Twisted](https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted) repository depending on the OS and python installated, in my case i have win10 and python 3.9 therefore the wheel is Twisted-20.3.0-cp39-cp39-win_amd64.whl and run:

```bash
pip install Twisted-20.3.0-cp39-cp39-win_amd64.whl
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
