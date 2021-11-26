import time
from .interface.defs import Method, Endpoint
from .request import TransactionError
from typing import Callable


children_attr_name = 'Children'


def get_window_content(harness, sleep_before_dump_time=0):
    time.sleep(sleep_before_dump_time)
    body = {"ui": True, "getWindow": True}
    retval = None
    try:
        retval = harness.request(Endpoint.DEVELOPERMODE, Method.GET, body).response
    except TransactionError as e:
        if e.status == 406:
            retval = harness.request(Endpoint.DEVELOPERMODE, Method.GET, body).response
        else:
            raise
    if retval is None:
        raise RuntimeError('dom was not requested!')
    if 'dom' in retval.body:
        return retval.body['dom']
    else:
        raise RuntimeError(f"dom dump failure with: {retval}")


def item_contains(body: dict, attr_name, attr_value):
    if attr_name in body:
        return body[attr_name] == attr_value


# extends item_contains to check children
def item_contains_recursively(body: dict, attr_name, attr_value):
    if len(body) == 1:
        return item_contains_recursively(next(iter(body.values())), attr_name, attr_value)

    if item_contains(body, attr_name, attr_value):
        return True

    if children_attr_name in body:
        for child in body[children_attr_name]:
            value_found = item_contains_recursively(child, attr_name, attr_value)
            if value_found:
                return True
    return False


# extends item_contains_recursively to support list of attribute name-value pairs
def item_contains_multiple_recursively(body: dict, attr_name_value_pairs):
    for name, value in attr_name_value_pairs:
        if not item_contains_recursively(body, name, value):
            return False
    return True


# restricts item_contains_multiple_recursively to check only children
def item_has_child_that_contains_recursively(body :dict, attr_name_value_pairs) :
    if len(body) == 1:
        return item_has_child_that_contains_recursively(next(iter(body.values())), attr_name_value_pairs)

    if children_attr_name in body:
        for child in body[children_attr_name] :
            if item_contains_multiple_recursively(child, attr_name_value_pairs) :
                return True
    return False


# in children, finds child that contains given name-value attribute pairs and returns the child index
# useful in ListView navigation
def get_child_number_that_contains_recursively(body:dict, attr_name_value_pairs):
    if len(body) == 1:
        return get_child_number_that_contains_recursively(next(iter(body.values())), attr_name_value_pairs)

    if children_attr_name in body:
        child_index = 0
        for child in body[children_attr_name]:
            if item_contains_multiple_recursively(child, attr_name_value_pairs):
                return child_index
            child_index += 1

    return -1


def find_parent(body: dict, child_name) -> dict:
    if len(body) == 1:
        return find_parent(next(iter(body.values())), child_name)

    if children_attr_name in body:
        for child in body[children_attr_name]:
            if next(iter(child)) == child_name:
                return body
            result = find_parent(next(iter(child.values())), child_name)
            if result:
                return result
    return {}


def find_child_that_contains(body: dict, attr_name, attr_value) -> dict:
    if len(body) == 1:
        return find_child_that_contains(next(iter(body.values())), attr_name, attr_value)
    if children_attr_name in body:
        for child in body[children_attr_name]:
            if item_contains_recursively(child, attr_name, attr_value):
                return child

    return {}


def find_item_depth_first(body: dict, attr_name) -> dict:
    if attr_name in body:
        return body[attr_name]
    if children_attr_name in body:
        for child in body[children_attr_name]:
            result = find_item_depth_first(child, attr_name)
            if result:
                return result
    elif len(body) == 1:
        return find_item_depth_first(next(iter(body.values())), attr_name)
    return {}


def get_direct_children_of_element(body: dict) -> list:
    children = []
    if children_attr_name in body:
        for child in body[children_attr_name]:
            children.append(child)
    return children


class DomNode:
    dom_depth = 0

    def __init__(self, data: dict):
        if type(data) is not dict:
            raise RuntimeError("DOM parsing error: bad typeY")
        if len(data.keys()) == 0:
            raise RuntimeError("DOM parsing error: bad empty dict")
        # there is needless nesting here
        self.type_name = list(data.keys())[0]
        # log.debug("    " * (DomNode.dom_depth + 1) + f"parsing: {self.type_name}")
        self.data = data[self.type_name]
        self._set_params(self.data)
        self.children = []
        if self.children_count > 0:
            self._populate_children(self.data)

    def hasChildren(self):
        return self.children is not None

    def _set_params(self, data):
        try:
            self.active = data["Active"]        # bool
            self.focus = data["Focus"]          # bool
            self.type = data["ItemType"]        # int
            self.visible = data["Visible"]      # bool
            self.children_count = data['ChildrenCount']
        except KeyError as e:
            # log.error(f"invalid data to parse! lacking: {e} in {data}")
            raise RuntimeError("cant parse dom")

    def _populate_children(self, data):
        self.children = []
        if self.children_count > 0:
            DomNode.dom_depth = DomNode.dom_depth + 1
        for val in data['Children']:
            self.children.append(DomNode(val))
        if self.children_count > 0:
            DomNode.dom_depth = DomNode.dom_depth - 1


def find_all(root: DomNode, filter: Callable[[DomNode], bool]) -> list:
    '''
    filter out all elements meeting the requirements
    '''
    limit = 1000
    li = []

    def r(body: DomNode, filter: Callable):
        nonlocal limit, li
        limit = limit - 1
        if limit == 0:
            raise RuntimeError("DOM parsing hit recursion depth")
        if body is None:
            return
        if filter(body):
            li.append(body)
        for v in body.children:
            r(v, filter)

    r(root, filter)
    return li
