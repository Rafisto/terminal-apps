import argparse
import os

argument_parser = argparse.ArgumentParser(description="Terminal Video Player",
                                          formatter_class=argparse.ArgumentDefaultsHelpFormatter)
argument_parser.add_argument("file", help="Video file to play")
argument_parser.usage = "videoplayer.py [-h for help]"


def CheckFileExists(file):
    if not os.path.isfile(file):
        raise argparse.ArgumentTypeError("File not found")
    return file


def CheckHelp(parameters):
    if parameters.help:
        argument_parser.print_help()
        exit()


class VideoPlayer:
    parameters = argument_parser.parse_args()
    CheckHelp(parameters)

    file = CheckFileExists(parameters.file)


VideoPlayer()
