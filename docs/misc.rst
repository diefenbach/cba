Components
==========

id
--
The id of the element. This corresponds to the HTML id, hence it must be unique
throughout the document. If not given, this will be set with a unique UUID4.

cid
---
The CBA internal component id of a component. If not set this defaults to the
´´element id´´.

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
2. Subclass, overwrite the init_components method and set self.init_components
   within it.
