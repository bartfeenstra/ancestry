from setuptools import setup, find_packages


SETUP = {
    'name': 'ancestry',
    'python_requires': '~= 3.11',
    'install_requires': [
        'betty == 0.3.0b2',
    ],
    'extras_require': {
        'development': [
            'autopep8 ~= 2.0.4',
            'basedmypy ~= 2.0, >= 2.2.1',
            'flake8 ~= 6.1.0',
        ],
    },
    'entry_points': {
        'betty.extensions': [
            'ancestry.extension.PublishPeople=ancestry.extension.PublishPeople',
        ],
    },
    'packages': find_packages(),
}

if __name__ == '__main__':
    setup(**SETUP)
