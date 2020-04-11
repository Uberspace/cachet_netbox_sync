from setuptools import setup

setup(
    name='cachet_netbox_sync',
    version='0.0.1',
    description='Take things from netbox and add them as components in netbox.',
    author='uberspace.de',
    author_email='hallo@uberspace.de',
    url='https://github.com/uberspace/cachet_netbox_sync',
    packages=[
        'cachet_netbox_sync',
    ],
    entry_points={
        'console_scripts': ['cachet_netbox_sync=cachet_netbox_sync.hashbang:main'],
    },
    install_requires=[
        'cachet-client==3.0.*',
        'pynetbox==4.3.*',
    ],
    extras_require={
        'dev': [
            'black',
            'pre-commit',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Systems Administration',
        'Programming Language :: Python :: 3.6',
    ],
    zip_safe=True,
)
