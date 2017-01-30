.. warning::

    CBA is alpha with all well known consequences.

Component Based Applications
============================

CBA is a framework to create web applications based on components. Components
are buttons, input fields, links, etc.

Overview
========

- An application based on CBA is completely build with components provided by
  CBA.
- All components and their values are accessible during run time.
- All components can be changed and refreshed separately.
- The whole application can be build with ``Python`` only (but don't have to.
  Own CSS and Javascript can be provided as well).
- CBA comes with a set of core components, see :ref:`the API documentation
  <default-components-label>` for more. Own components can be added easily.
- CBA is build on top of ``Django``, which means, all ``Django`` features are
  available, e.g. the ORM, the authentication system or the i18n framework.
- CBA is inspired by EPFL http://pyramid-epfl.readthedocs.io/.

Example
=======

The following is a simplified example.

.. code-block:: Python

    class MyAppRoot(components.Group):
        def init_components(self):
            self.initial_components = [
                components.TextInput(
                    id="my-input",
                    label="Name",
                ),
                components.Button(
                    id="my-button",
                    value="Save!",
                    handler={"click": "server:handle_save"},
                ),
                components.HTML(
                    id="my-div"
                    tag="div",
                ),
            ]

        def handle_save(self):
            my_input = self.get_component("my-input")
            my_div = self.get_component("my-div")

            my_div.text = my_input.value
            my_div.refresh()

    class MyAppView(CBAView):
        root = MyAppRoot

Contents
========

.. toctree::
   :maxdepth: 2

   installation.rst
   misc.rst
   todos.rst
   api.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

