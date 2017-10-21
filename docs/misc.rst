Components
==========

id
--
The id of the element. This corresponds to the HTML id, hence it must be unique
throughout the document. If not given, this will be set with a unique UUID4.

cid
---
The CBA internal component id of a component. If not set this defaults to the
´´id´´.

The cid is used to get the component out of the component tree.

component-value
---------------
The CBA internal value of a component. If not set this defaults to the
``cid`` of the components.


First call
==========

1. Django -> cba.views.get() -> root() -> root.init_components() -> components.init_components()
2. Django -> cba.views.get() -> root.render() -> [components.render()]


There are two ways to add intial sub components to a component

1. With construction (__init__)


  .. code-block:: python

    components.Group(
        initial_components=[
            components.HTML(content="Hello"),
            components.Button(value="OK!"),
        ]
    )

2. Subclass, overwrite the init_components method and set self.initial_components
   within it.

  .. code-block:: python

    class MyGroup(components.Group)
        def init_components(self):
            self.initial_components = [
                components.HTML(content="Hello"),
                components.Button(value="OK!"),
            ]

