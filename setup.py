from setuptools import find_packages
from setuptools import setup


setup(
    name="dj-rest-auth-mfa",
    # entry_points={
    #     "pytest11": [
    #         "pytest_minio_mock = pytest_minio_mock.plugin",
    #     ],
    # },
    packages=find_packages(exclude=("tests",)),
    platforms="any",
    python_requires=">=3.6",
    install_requires=
    [
        "Django>=4.1.7",
        "djangorestframework>3.14.0", 
        "djangorestframework-simplejwt", 
        "django-cors-headers",
        "dj-rest-auth",
        "django-allauth==0.57.0",
        "django-mfa2"
    ],
    url="https://github.com/oussjarrousse/dj-rest-auth-saml",
    license="MIT",
    author="Oussama Jarrousse",
    author_email="oussama@jarrousse.org",
    description="A Django App that adds MFA endpoints to dj-rest-auth",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    keywords="Django REST allauth dj-rest-auth mfa totp 2fa authentication otp",
    extras_require={"dev": ["pre-commit", "tox"]},
    version="0.0.1",
    long_description_content_type="text/markdown",
    classifiers=[
        "Framework :: Pytest",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Testing",
    ],
    project_urls={
        # "Documentation": "https://dj-rest-auth-saml.readthedocs.io/en/latest/",
        # "Changelog": "https://dj-rest-auth-saml.readthedocs.io/en/latest/changelog.html",
        "Source": "https://github.com/oussjarrousse/dj-rest-auth-mfa/",
        "Tracker": "https://github.com/oussjarrousse/dj-rest-auth-mfa/issues",
    },
)
