import commands
import subprocess
import re


def get_module_list():
    result = subprocess.run(commands.list_modules, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode('utf-8'))
    return result.stdout.decode("utf-8")


def split_module_strings(module_list_string):
    module_strings = re.split(r'index: \d+', module_list_string)
    n_mod_match = re.search(r'\d+', module_strings[0])
    if n_mod_match is None:
        raise ValueError('Number of loaded modules not present in module list string.')
    n_mods = int(n_mod_match.group())
    assert(n_mods == (len(module_strings) - 1))
    return n_mods, module_strings[1:]


if __name__ == "__main__":
    n_mods, mods = split_module_strings(get_module_list())
    print('Found %d modules.' % n_mods)
    # for modstr in
    print(mods[0])
    print(mods[1])
    print(mods[2])
