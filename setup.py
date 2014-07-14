from setuptools import setup, find_packages
from io import open

setup(
    name='django-mstats',
    version='0.1.2',
    description='Simple, re-usable, stateless Django app for visualizing and browsing '
                'statistics, mainly based on your existing Django models.',
    long_description=open('README.rst', encoding='utf-8').read(),
    author='Jonatan Heyman',
    author_email='jonatan@heyman.info',
    url='https://github.com/heyman/django-mstats',
    download_url='https://pypi.python.org/pypi/django-mstats',
    license='BSD',
    packages=find_packages(exclude=('tests', 'example')),
    install_requires=[
        'django>=1.5.0',
    ],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)