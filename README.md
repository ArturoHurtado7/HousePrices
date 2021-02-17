# HousePrices
## Installation

Initialize the virtual Environment, and activate it:

```bash
py -m venv venv
venv\scripts\activate
```

at the end we have to deactivate the virtual environment with the command:

```bash
deactivate
```

We need to install the following python libraries into the virtual environment:

* Twisted
* Scrapy
* Autopep8
* selenium
* requests
* BeautifulSoup4

```bash
pip install twisted scrapy autopep8 requests BeautifulSoup4
pip install -U selenium
```

if this doesn't work we have to download the library from [Twisted](https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted) repository depending on the OS and python installated, in my case i have win10 and python 3.9 therefore the wheel is Twisted-20.3.0-cp39-cp39-win_amd64.whl and run the following command:

```bash
pip install Twisted-20.3.0-cp39-cp39-win_amd64.whl
```

You need to download Chrome driver from [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) depending on your version of Chrome

and let the driver in the driver folder

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
