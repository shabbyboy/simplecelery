'''
shell 命令进入函数
通过分析命令行去执行操作
'''
from utils.command import Command

def main():
    comm = Command()
    argv = comm.execcommand()



if __name__=='__main__':
    main()

