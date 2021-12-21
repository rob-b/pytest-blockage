from setuptools import setup


setup(
    name='pytest-blockage',
    version='0.2.3',
    description='Disable network requests during a test run.',
    long_description=(open('README.rst').read() +
                      open('CHANGELOG.rst').read()),
    long_description_content_type='text/x-rst',
    license='BSD',
    install_requires=['pytest'],
    py_modules=['pytest_blockage'],
    entry_points={'pytest11': ['blockage = pytest_blockage']},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ]
)
