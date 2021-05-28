# Virtual Assistant

Virtual Assistant is a Python library that takes voice commands to perform a list of actions:
1. Open **windows application**
2. Get **weather reports**
3. Get the latest **covid statistics**
4. Search and play video on **Youtube**
5. Perform **web search**
6. Get **Date** and **time**

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following:-

1. Install requirements.txt
```bash
pip install -r requirements.txt
```
2. Install **pyaudio**
```bash
pip install pipwin
pipwin install pyaudio
```
If the above mentioned method doesn't work try install **.whl** file according to the python version from this [link](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
```bash
pip install -path_to_whl_file-
```
3. Update **config.json** to include application paths

4. Add/update **.env** to include following parameters (pyowm key can be generated [here](https://openweathermap.org/)):
```bash
config_json_path = --path to config json here--
pyowm_key= --pyowm generated key--
```

## Usage

The utility can be imported and started as shown below:

```python
from src.utils.virtual_assistant import VirtualAssistant
VirtualAssistant().start_assistant()
```
Few sample commands to try once the utility is running :
1. alexa what time it is?
2. alexa what date is it?
3. alexa what does **"say an object or concept name"** means?
4. alexa give latest covid reports.
5. alexa tell me a joke
6. alexa who is **"say a persons name"**?
7. alexa play **"say a song name"**
8. alexa open **"say a configured application name"**

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.