"Utilities that relate to Operating-System like actions: processes, files, signals, etc"

import tempfile
import os

class TemporaryDirectoryContext(object):
    def __enter__(self):
        self.temporary_directory = tempfile.mkdtemp()
        return self.temporary_directory
    def __exit__(self, error_type, error, traceback):
        for directory, subdirectories, filenames in os.walk(self.temporary_directory):
            for filename in filenames:
                os.remove(os.path.join(directory, filename))
        os.removedirs(self.temporary_directory)
