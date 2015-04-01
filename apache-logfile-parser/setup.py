from distutils.core import setup

setup(
    name="aparse",
    version="1.0",
    description = 'Parses Apache Log File',
    author = 'T. Vonnegut',
    author_email = 'freembr@users.noreply.github.com',
    license = 'GNU Public License',
    url = 'github.com/freembr',
    py_modules = ['aparse'],
    package_dir = {'aparse': 'lib'},
    packages = ['aparse']
)
