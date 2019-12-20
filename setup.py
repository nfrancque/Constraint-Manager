from setuptools import setup, find_packages


setup(
    name='constraint_manager',
    version='0.1',
    description='An automatic constraint generation tool.',
    packages=find_packages(),
    # package_dir={
    #     'constraint_manager':'constraint_manager'
    # },
    package_data={'constraint_manager': ['../interfaces/*', '../parts/*', '../sample/*']},
    include_package_data=True,
    install_requires=[
    	'PyYAML>=5.2'
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest'
    ],
    entry_points = {
    	'console_scripts' :[
    	 'constraint-manager=constraint_manager.constraint_manager:main'
    	]
    }

)