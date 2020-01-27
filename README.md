# Intro
sony-disconnect it is an app to disconnect your Sony WH-1000XM3 when it is inactive.

It is based on pulseaudio events.

When inactive timeout occurs it disconnects your headphones using bluetooth.


# How to run
```console
$ git clone https://github.com/w1r0x/sony-disconnect.git
$ cd sony-disconnect
$ pip install -r Requirements
$ python app.py
```

Should run with user priveleges to access pulseaudio server

# bt-device

Need to have `bt-device` app for bluetooth disconnect event

## Ubuntu
```console
$ apt-get update && apt-get install bluez-tools
```
