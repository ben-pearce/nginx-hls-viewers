import subprocess
import argparse
import re
import time
import logging

logger = logging.getLogger('nginx-hls-viewers')
logging.basicConfig(level=logging.NOTSET)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-I', '--in', dest='in_file_name', type=str,
                        default='/var/log/nginx/access.log',
                        help='Path to the nginx logging file')
    parser.add_argument('-O', '--out', dest='out_file_name', type=str,
                        default='/tmp/hls.count',
                        help='Path to live viewer count file')
    parser.add_argument('-w', '--wait', type=int, default=5,
                        help='Time in minutes to wait before assuming a client is not longer watching')
    args = parser.parse_args()

    try:
        with open(args.in_file_name, 'r') as f:
            s = f.read()
    except IOError as e:
        logging.critical(f'unable to read infile: {e}')
        exit()

    f = subprocess.Popen(['tail', '-F', args.in_file_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    clients = {}

    logger.info('listening for hls viewers')

    line = f.stdout.readline()
    p = re.compile(r'((?:\d+\.){3}\d+) - - \[.+] "GET .+\.(?:ts|m4s)')

    try:
        while line:
            line = f.stdout.readline()
            result = p.search(str(line))

            if result is not None:
                ip_addr = result.group(1)
                clients[ip_addr] = time.time()

            for ip_addr, last_seen in clients.copy().items():
                if last_seen < time.time() - args.wait * 60:
                    del clients[ip_addr]

            count = len(clients)
            out = open(args.out_file_name, 'w')
            out.write(str(count))

            logger.info(f'currently {count} viewers')
    except KeyboardInterrupt:
        logger.critical('shutting down')
