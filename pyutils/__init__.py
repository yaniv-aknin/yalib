"Utilities that are useful within the context of Python itself. cross-version implementations, inspect-like functionality, etc"

import code

def interact(locals=None):
    try:
        from IPython.Shell import IPShellEmbed
        interact_func = lambda locals: IPShellEmbed(argv=())(local_ns=locals)
    except ImportError:
        interact_func = lambda locals: code.interact(local=locals)
    interact_func(locals)
