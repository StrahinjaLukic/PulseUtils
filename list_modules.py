import commands
import subprocess


def module_list_str():
    result = subprocess.run(commands.list_modules, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print('Captured the list')
    return result.stdout.decode("utf-8")


if __name__ == "__main__":
    print(module_list_str())
