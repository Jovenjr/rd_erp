from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in csf_rd/__init__.py
from csf_rd import __version__ as version

setup(
	name="csf_rd",
	version=version,
	description="Country Specific Functionality for República Dominicana",
	author="CSF RD Team",
	author_email="support@csf-rd.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
