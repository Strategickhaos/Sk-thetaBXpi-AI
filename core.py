from interface.shell_exec import run_command
def main():
    print('?? Stratigickhaos Agent Active')
    while True:
        cmd = input('> ')
        if cmd.lower() in ['exit', 'quit']: break
        print(run_command(cmd))
if __name__ == '__main__':
    main()
