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
    re_arg = re.compile(r'([^=^\s]+)=([^=^\s]+)')

    def __init__(self):
        self.attributes = {}
        self.properties = {}
        self.arguments = {}
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
            attr_match = active['regex'].search(line)
            if attr_match:
                assert(len(attr_match.groups()) == 2)
                attr_key = attr_match.group(1)
                if attr_key == 'properties':
                    active['regex'] = cls.re_prop
                    active['dict'] = pa_module.properties
                    continue
                if attr_key == 'argument':
                    arguments = attr_match.group(2)[1:-1]
                    arg_match = re.search(cls.re_arg, arguments)
                    there_are_arguments = (arg_match is not None)
                    while arg_match is not None:
                        cls.add_item(arg_match, pa_module.arguments)
                        cls.add_item(arg_match, pa_module.arguments)
                        arguments = arguments[len(arg_match.group()) + 1:]
                        arg_match = re.search(cls.re_arg, arguments)
                    if there_are_arguments:
                        continue
                cls.add_item(attr_match, active['dict'])
            else:
                active['regex'] = cls.re_attr
                active['dict'] = pa_module.attributes
                attr_match = active['regex'].search(line)
                if attr_match:
                    cls.add_item(attr_match, active['dict'])
        return pa_module


if __name__ == "__main__":
    n_mods, mods = split_module_strings(get_module_list())
    print('Found %d modules.' % n_mods)

    modules = [PAModule.parse_module_string(modstr) for modstr in mods]
    nmod = 1
    for module in modules:
        print('Module #%d:' % nmod)
        print('  Attributes: %s' % str(module.attributes))
        print('  Properties: %s' % str(module.properties))
        print('  Arguments: %s' % str(module.arguments))
        nmod += 1
