from setuptools import setup

setup(
    name='PDS_Project_nextbike',
    version='0.0.2',
    description="Semester Project -- Programming Data Science",
    author="Student",
    author_email="gassnerm@smail.uni-koeln.de",
    packages=['PDS_Project_nextbike', 'PDS_Project_nextbike.io', 'PDS_Project_nextbike.model'],
    install_requires=['pandas', 'scikit-learn', 'click', 'numpy', 'matplotlib', 'tensorflow','keras', 'geopy','folium~= 0.5.0'],
    entry_points={
        'console_scripts': ['PDS_Project_nextbike=PDS_Project_nextbike.cli:main']
    }
)
