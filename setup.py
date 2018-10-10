from distutils.core import setup

setup(
    name='cnemc-calculator',
    version='0.1.0',
    author='CoeusITE',
    author_email='CoeusITE@Posteo.ORG',
    packages=['cnemc-calculator', 'cnemc-calculator.test'],
    scripts=[],
    url='https://github.com/coeusite/cnemc-calculator',
    license='LICENSE',
    description='Unofficial calculator for air quality factors.',
    long_description=open('README.txt').read(),
    install_requires=[
        "pandas >= 0.20.1",
    ],
)