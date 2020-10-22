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
