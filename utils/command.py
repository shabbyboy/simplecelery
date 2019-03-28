'''
命令行处理类，先写个简单的吧
'''

import argparse

class Command(object):
    def execcommand(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--run",'-r',required=True)
        args = parser.parse_args()
        return args
