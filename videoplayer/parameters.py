import argparse
import os


class ArgumentParser:
    def __init__(self):
        self.argument_parser = argparse.ArgumentParser(description="Terminal Video Player",
                                                       formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        self.argument_parser.add_argument("-f", "--file", help="Video file to play")
        self.argument_parser.add_argument("-c", "--color", help="Color mode", action='store_true')
        self.argument_parser.add_argument("-p", "--pre", help="Pre-render video", action='store_true')
        self.argument_parser.add_argument("-s", "--save", help="Save pre-rendered video", action='store_true')
        self.argument_parser.add_argument("-F", "--fps",
                                          help="Framerate of the video (will use the framerate of the original video if not specified)",
                                          type=int, default=0)
        self.argument_parser.usage = "videoplayer.py [-h for help]"
        self.parameters = self.argument_parser.parse_args()
        self.ValidateArguments()

    def ValidateArguments(self):
        self.CheckFileExists()
        self.CheckHelp()
        if os.name == 'nt' and self.parameters.color:
            print("Color mode probably not supported on Windows, consider switching to better OS")
        if self.parameters.fps == 0:
            print("Using source framerate")
        elif self.parameters.fps < 0:
            print("-F [--fps] positional argument must be positive")
            exit()

    def CheckFileExists(self):
        if not os.path.isfile(self.argument_parser.parse_args().file):
            raise argparse.ArgumentTypeError("File not found")

    def CheckHelp(self):
        if 'help' in self.parameters:
            self.argument_parser.print_help()
            exit()

    def GetColor(self):
        return self.parameters.color

    def GetFile(self):
        return self.parameters.file

    def GetFPS(self):
        return self.parameters.fps

    def GetPre(self):
        return self.parameters.pre
