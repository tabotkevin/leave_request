from setuptools import find_packages, setup


packages = [
    "pytest<7,>=5",
    "pytest-django",
    "pytest-sugar",
    "pytest-timeout",
]

setup(
    name="django-leave-request",
    version="1.0.0",
    author="Devskiller",
    author_email="support@devskiller.com",
    packages=find_packages(),
    python_requires=">=3.5",
    include_package_data=True,
    zip_safe=False,
    install_requires=packages
    + [
        "wheel==0.34.2",
        "django==2.2.16",
        "setuptools==44.1.0",
        "factory-boy==2.12.0",
        "faker==4.1.1",
        "python-dateutil==2.8.1",
        "lxml==4.5.1",
        "pycountry==20.7.3",
        "pytz==2020.1",
    ],
    setup_requires=["pytest-runner"],
    tests_require=packages,
)
