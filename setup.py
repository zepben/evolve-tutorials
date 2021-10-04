from setuptools import setup, find_packages

test_deps = ["pytest"]
setup(name="evolve-src",
      packages=find_packages('src'),
      version="0.1.0",
      package_dir={"": "src"},
      install_requires=
      ["zepben.evolve == 0.25.0",
       "zepben.eas == 0.5.0"],
      extras_require={
          "tests": test_deps
      })
