from setuptools import setup, find_packages

SETUP = {
    'name': 'ancestry',
    'extras_require': {
        'development': [
            'autopep8 ~= 1.4.3',
            'flake8 ~= 3.7.0',
        ],
    },
    'packages': find_packages(),
}

if __name__ == '__main__':
    setup(**SETUP)
