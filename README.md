# nginx-hls-viewers

A python script for monitoring live viewer count from an nginx HLS stream with the nginx-rtmp-module enabled.

Other solutions for this exist but rely on too many dependencies, or require piping the stream through some means other 
than nginx itself. Which makes setup cumbersome and time-consuming.

This is a single python script with **no** dependencies. Simply download and run with python interpreter.

It works by monitoring the nginx access log and using the IP address of the client and the time at which they were last 
seen to tell if they are still watching.

The script then writes to a file for you to do what you wish with, for example, to configure nginx to serve the file 
over HTTP.

## Setup

Download with curl and run as a normal python script.

```shell script
curl https://raw.githubusercontent.com/ketnipz/nginx-hls-viewers/main/main.py
sudo python3 main.py -I /var/log/nginx/hls_access.log
```

By default, the output file is located at `/tmp/hls.count`. This file contains nothing but the current view count.

```shell script
cat /tmp/hls.count
0
```

You may also configure a systemd service to keep this python script running, 
[click here for an example .service file](https://raw.githubusercontent.com/ketnipz/nginx-hls-viewers/main/nginx-hls-viewers.service).

To see an example nginx configuration file, 
[click here](https://raw.githubusercontent.com/ketnipz/nginx-hls-viewers/main/nginx-hls-viewers.conf).

## Usage

```
usage: main.py [-h] [-I IN_FILE_NAME] [-O OUT_FILE_NAME] [-w WAIT]

optional arguments:
  -h, --help            show this help message and exit
  -I IN_FILE_NAME, --in IN_FILE_NAME
                        Path to the nginx logging file
  -O OUT_FILE_NAME, --out OUT_FILE_NAME
                        Path to live viewer count file
  -w WAIT, --wait WAIT  Time in minutes to wait before assuming a client
                        is not longer watching
```