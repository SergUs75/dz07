from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='1',
    description='',
    url='',
    author='SU',
    author_email='',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={
        'console_scripts': [
            'clean-folder = clean_folder.clean:clean_folder'
        ]
    }
)