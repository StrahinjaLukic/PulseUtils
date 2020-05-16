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
    re_attr = re.compile(r'^\s+(.+):\s*(.*)')
    re_prop = re.compile(r'^\s+(.+)\s+=\s+"(.*)"')

    def __init__(self):
        self.attributes = {}
        self.properties = {}
        self.lines = []

    @staticmethod
    def parse_value(value_str):
        return True if value_str.lower() == 'yes' else False if value_str.lower() == 'no' else value_str

    @classmethod
    def add_item(cls, arg_match, dictionary):
        attr_key = arg_match.group(1)
        attr_value = cls.parse_value(arg_match.group(2))
        dictionary[attr_key] = attr_value

    @classmethod
    def parse_module_string(cls, module_string):
        pa_module = cls()
        pa_module.lines = module_string.splitlines()

        active = {'regex': cls.re_attr, 'dict': pa_module.attributes}

        for line in pa_module.lines:
            arg_match = active['regex'].search(line)
            if arg_match:
                assert(len(arg_match.groups()) == 2)
                attr_key = arg_match.group(1)
                if attr_key == 'properties':
                    active['regex'] = cls.re_prop
                    active['dict'] = pa_module.properties
                    continue
                cls.add_item(arg_match, active['dict'])
            else:
                active['regex'] = cls.re_attr
                active['dict'] = pa_module.attributes
                arg_match = active['regex'].search(line)
                if arg_match:
                    cls.add_item(arg_match, active['dict'])
        return pa_module


if __name__ == "__main__":
    n_mods, mods = split_module_strings(get_module_list())
    print('Found %d modules.' % n_mods)

    modules = [PAModule.parse_module_string(modstr) for modstr in mods]
    for module in modules:
        print(module.attributes)
        print(module.properties)
