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


class PAModule:
    def __init__(self):
        self.attributes = {}
        self.properties = {}
        self.lines = []

    @staticmethod
    def parse_value(value_str):
        return True if value_str.lower() == 'yes' else False if value_str.lower() == 'no' else value_str

    @classmethod
    def parse_module_string(cls, module_string):
        pa_module = cls()
        pa_module.lines = module_string.splitlines()
        for line in pa_module.lines:
            arg_match = re.search(r'^\s+(.+):\s+(.*)', line)
            if arg_match:
                assert(len(arg_match.groups()) == 2)
                attr_key = arg_match.group(1)
                attr_valstr = arg_match.group(2)
                attr_value = cls.parse_value(attr_valstr)
                pa_module.attributes[attr_key] = attr_value
        return pa_module


if __name__ == "__main__":
    n_mods, mods = split_module_strings(get_module_list())
    print('Found %d modules.' % n_mods)

    modules = [PAModule.parse_module_string(modstr) for modstr in mods]
    for module in modules:
        print(module.attributes)
