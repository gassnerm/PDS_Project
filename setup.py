from setuptools import setup

setup(
    name='PDS_Project_nextbike',
    version='0.0.1dev1',
    description="Semester Project -- Programming Data Science",
    author="Student",
    author_email="gassnerm@smail.uni-koeln.de",
    packages=["PDS_Project_nextbike"],
    install_requires=['pandas', 'scikit-learn', 'click', 'numpy'],
    entry_points={
        'console_scripts': ['PDS_Project_nextbike=PDS_Project_nextbike.cli:main']
    }
)
