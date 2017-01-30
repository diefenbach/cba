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
