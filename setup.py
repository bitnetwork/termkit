from setuptools import setup, find_packages

setup(
  name="termkit",
  version="0.1",
  packages=["termkit"],
  # package_dir={"termkit": "src/termkit"}
  package_data={
    "termkit": ["terms/*.json"],
  },
  # zip_safe=True,

  # metadata to display on PyPI
  author="Me",
  author_email="me@example.com",
  description="This is an Example Package",
  license="MIT",
  keywords="",
  url="http://github.com/bitnetwork/termkit/",
  project_urls={
    "Bug Tracker": "http://github.com/bitnetwork/termkit/issues",
    "Documentation": "http://github.com/bitnetwork/termkit/wiki",
    "Source Code": "https://github.com/bitnetwork/termkit",
  }
)
