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
   # Install with development dependencies
   uv sync


This way,
your installation always stays up-to-date,
even if you pull new changes from the Github repository.

.. _PyPI: https://pypi.org/project/opensmile/
.. _Github: https://github.com/audeering/opensmile-python/


Coding Convention
-----------------

We follow the PEP8_ convention for Python code
and use ruff_ as a linter and code formatter.
In addition,
we check for common spelling errors with codespell_.
Both tools and possible exceptions
are defined in :file:`pyproject.toml`.

The checks are executed in the CI using `pre-commit`_.
You can enable those checks locally by executing::

    uvx pre-commit install
    uvx pre-commit run --all-files

Afterwards ruff_ and codespell_ are executed
every time you create a commit.

You can also call ruff_ and codespell_ directly::

    uvx ruff check --fix .  # lint all Python files, and fix any fixable errors
    uvx ruff format .  # format code of all Python files
    uvx codespell

It can be restricted to specific folders::

    $ uvx ruff check opensmile/ tests/
    $ uvx codespell opensmile/ tests/


.. _codespell: https://github.com/codespell-project/codespell/
.. _PEP8: http://www.python.org/dev/peps/pep-0008/
.. _pre-commit: https://pre-commit.com
.. _ruff: https://beta.ruff.rs


Building the Documentation
--------------------------

If you make changes to the documentation,
you can re-create the HTML pages using Sphinx_.

To create the HTML pages, use::

    $ uv run --python 3.12 sphinx-build docs/ build/sphinx/html -b html

The generated files will be available
in the directory :file:`build/sphinx/html/`.

It is also possible to automatically check if all links are still valid::

    $ uv run --python 3.12 sphinx-build docs/ build/sphinx/html -b linkcheck

.. _Sphinx: http://sphinx-doc.org


Running the Tests
-----------------

You'll need pytest_ for that.

To execute the tests, simply run::

    $ uv run pytest

.. _pytest: https://pytest.org


Creating a New Release
----------------------

New releases are made using the following steps:

#. Update ``CHANGELOG.rst``
#. Commit those changes as "Release X.Y.Z"
#. Create an (annotated) tag with ``git tag -a X.Y.Z``
#. Push the commit and the tag to Github
