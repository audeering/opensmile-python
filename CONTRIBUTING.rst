Contributing
============

Everyone is invited to contribute to this project.
Feel free to create a `pull request`_ .
If you find errors, omissions, inconsistencies or other things
that need improvement, please create an issue_.

.. _issue: https://github.com/audeering/opensmile-python/issues/new/
.. _pull request: https://github.com/audeering/opensmile-python/compare/


Development Installation
------------------------

Instead of pip-installing the latest release from PyPI_,
you should get the newest development version from Github_::

   git clone https://github.com/audeering/opensmile-python/
   cd opensmile-python
   # Create virutal environment for this project
   # e.g.
   # virtualenv --python="python3"  $HOME/.envs/opensmile-python
   # source $HOME/.envs/opensmile-python/bin/activate
   pip install -r requirements.txt


This way,
your installation always stays up-to-date,
even if you pull new changes from the Github repository.

.. _PyPI: https://pypi.org/project/opensmile-python/
.. _Github: https://github.com/audeering/opensmile-python/


Coding Convention
-----------------

We follow the PEP8_ convention for Python code
and check for correct syntax with flake8_.
Exceptions are defined under the ``[flake8]`` section
in :file:`setup.cfg`.

The checks are executed in the CI using `pre-commit`_.
You can enable those checks locally by executing::

    pip install -r tests/requirements.txt
    pre-commit install
    pre-commit run --all-files

Afterwards flake8_ is executed
every time you create a commit.

You can also install flake8_
and call it directly::

    pip install flake8  # you might consider system wide installation
    flake8

It can be restricted to specific folders::

    flake8 audfoo/ tests/

.. _PEP8: http://www.python.org/dev/peps/pep-0008/
.. _flake8: https://flake8.pycqa.org/en/latest/index.html
.. _pre-commit: https://pre-commit.com


Building the Documentation
--------------------------

If you make changes to the documentation,
you can re-create the HTML pages using Sphinx_.
You can install it and a few other necessary packages with::

   pip install -r docs/requirements.txt

To create the HTML pages, use::

   python -m sphinx docs/ build/sphinx/html -b html

The generated files will be available
in the directory :file:`build/sphinx/html/`.

It is also possible to automatically check if all links are still valid::

   python -m sphinx docs/ build/sphinx/html -b linkcheck

.. _Sphinx: http://sphinx-doc.org/


Running the Tests
-----------------

You'll need pytest_ for that.
It can be installed with::

   pip install -r tests/requirements.txt

To execute the tests, simply run::

   python -m pytest

.. _pytest: https://pytest.org/


Creating a New Release
----------------------

New releases are made using the following steps:

#. Update ``CHANGELOG.rst``
#. Commit those changes as "Release X.Y.Z"
#. Create an (annotated) tag with ``git tag -a X.Y.Z``
#. Push the commit and the tag to Github
