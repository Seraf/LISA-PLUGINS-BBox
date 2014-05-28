from setuptools import setup
import json

metadata = json.loads(open('lisa/plugins/BBox/bbox.json').read())

def listify(filename):
    return filter(None, open(filename, 'r').read().strip('\n').split('\n'))

if __name__ == '__main__':
    setup(
        version=metadata['version'],
        name='lisa-plugin-BBox',
        packages=["lisa.plugins"],
        url='http://www.lisa-project.net',
        license='MIT',
        author='Julien Syx',
        author_email='julien.syx@gmail.com',
        description='LISA home automation system - Server',
        include_package_data=True,
        namespace_packages=['lisa.plugins'],
        install_requires=listify('requirements.txt'),
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'License :: OSI Approved :: MIT License',
            'Operating System :: POSIX',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Topic :: Internet :: WWW/HTTP',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )
