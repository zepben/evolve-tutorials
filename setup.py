from setuptools import setup, find_packages

test_deps = ["pytest"]
setup(name="evolve-src",
      packages=find_packages('src'),
      version="0.1.0",
      package_dir={"": "src"},
      install_requires=
      ["zepben.evolve == 0.26.0",
       "zepben.eas == 0.6.0",
       "pandapower == 2.7.0",
       "pp-translator == 0.3.0",
       "geojson", "pytest", "numba"],
      extras_require={
          "tests": test_deps
      })
