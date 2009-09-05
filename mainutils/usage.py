from yalib.alien import argparse

# HACK: _registered_executables is global, which assumes the equivalent of
#        'if __name__ == "__main__": main(sys.argv)' is ran just once per Python interpreter invocation
_registered_executables = {}
def executable(other):
    """executable classes must know how to register with an argparse parser, validate the parsed arguments,
        be constructed by __init__(self, options) and have an invoke() function"""
    other_class_cli_name = other.CLI_NAME if hasattr(other, 'CLI_NAME') else other.__name__.lower()
    if other_class_cli_name in _registered_executables and _registered_executables[other_class_cli_name] is not other:
        raise AssertionError('double executable registration for %s' % (other_class_cli_name,))
    _registered_executables[other_class_cli_name] = other
    return other

def initialize_subparsers(parser):
    subparsers = parser.add_subparsers(help='command to invoke')
    for command_name, command_class in _registered_executables.items():
        subcommand_parser = subparsers.add_parser(command_name)
        command_class.initialize_subparser(subcommand_parser)
        subcommand_parser.set_defaults(executable=command_class)

def parse_arguments(argv, **parser_kwargs):
    parser = argparse.ArgumentParser(**parser_kwargs)
    initialize_subparsers(parser)
    options = parser.parse_args(argv[1:])
    options.executable.validate_arguments(parser, options)
    return options

class BaseExecutable(object):
    @classmethod
    def initialize_subparser(cls, subparser):
        pass
    @classmethod
    def validate_arguments(cls, parser, options):
        pass
    def __init__(self, options):
        self.options = options
    def invoke(self):
        raise NotImplementedError('you must subclass %s.invoke' % (self.__class__.__name__,))
