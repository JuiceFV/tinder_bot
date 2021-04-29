from setuptools import setup, find_packages
import pathlib
import pkg_resources

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

setup(
    name="Tinder Bot",
    version="1.0.1",
    description="The bot which decide to like or dislike a tinder date, depends on you prefers.",
    author="Aleksandr Kasian",
    author_email="aleksandr.juicefv@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=install_requires,
    entry_points={
        'console_scripts':[
            'bot_start = application.entry',
            'validation = application.validation_entry',
            'img_scrap = application.image_sorting_entry'
        ]
    }
)