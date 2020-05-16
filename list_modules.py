import commands
import subprocess
import re


def get_module_list():
    result = subprocess.run(commands.list_modules, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print('Captured the list')
    return result.stdout.decode("utf-8")


def get_module_strings(module_list_string):
    module_strings = re.split(r'index: ([\d])', module_list_string)
    return module_strings


if __name__ == "__main__":
    mods = get_module_strings(get_module_list())
    print(mods[1])
    print(mods[2])
