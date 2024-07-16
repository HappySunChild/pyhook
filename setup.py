import setuptools

setup_info = {
	'name': 'pyhook',
	'version': '1.0.5',
	'author': 'HappySunChild',
	'description': 'A python for interfacing with Discord\'s webhook API. Designed to work with python 3.9+',
	'url': 'https://github.com/HappySunChild/pyhook',
	'packages': setuptools.find_packages(),
	'python_requires': '>=3.9',
	'install_requires': [
		'requests>=2.25.1',
		'python-dateutil>=2.8.0'
	]
}

setuptools.setup(**setup_info)