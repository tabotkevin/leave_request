import base64
import unittest

import leave.views


class StructureTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.MODULE = leave.views

    def test_class_exists_leaverequestcreate(self):
        classes = _get_class_names(self.MODULE)
        self.assertIn(
            base64.b64decode(b"TGVhdmVSZXF1ZXN0Q3JlYXRl").decode(),
            classes,
            msg=f"The class "
            f"`{base64.b64decode(b'TGVhdmVSZXF1ZXN0Q3JlYXRl').decode()}` "
            f"is not found, but it was marked as required.",
        )

    def test_class_exists_leaverequestdetail(self):
        classes = _get_class_names(self.MODULE)
        self.assertIn(
            base64.b64decode(b"TGVhdmVSZXF1ZXN0RGV0YWls").decode(),
            classes,
            msg=f"The class "
            f"`{base64.b64decode(b'TGVhdmVSZXF1ZXN0RGV0YWls').decode()}` "
            f"is not found, but it was marked as required.",
        )

    def test_class_exists_leaverequestlist(self):
        classes = _get_class_names(self.MODULE)
        self.assertIn(
            base64.b64decode(b"TGVhdmVSZXF1ZXN0TGlzdA==").decode(),
            classes,
            msg=f"The class "
            f"`{base64.b64decode(b'TGVhdmVSZXF1ZXN0TGlzdA==').decode()}` "
            f"is not found, but it was marked as required.",
        )

    def test_class_exists_leaverequestupdate(self):
        classes = _get_class_names(self.MODULE)
        self.assertIn(
            base64.b64decode(b"TGVhdmVSZXF1ZXN0VXBkYXRl").decode(),
            classes,
            msg=f"The class "
            f"`{base64.b64decode(b'TGVhdmVSZXF1ZXN0VXBkYXRl').decode()}` "
            f"is not found, but it was marked as required.",
        )

StructureTestVerificationSuite = StructureTestSuite


# === Internal functions, do not modify ===
import inspect

from types import ModuleType
from typing import List


def _get_function_names(module: ModuleType) -> List[str]:
    names = []
    functions = inspect.getmembers(module, lambda member: inspect.isfunction(member))
    for name, fn in functions:
        if fn.__module__ == module.__name__:
            names.append(name)
    return names


def _get_function_arg_names(module: ModuleType, fn_name: str) -> List[str]:
    arg_names = []
    functions = inspect.getmembers(module, lambda member: inspect.isfunction(member))
    for name, fn in functions:
        if fn.__module__ == module.__name__:
            if fn.__qualname__ == fn_name:
                args_spec = inspect.getfullargspec(fn)
                arg_names = args_spec.args
                if args_spec.varargs is not None:
                    arg_names.extend(args_spec.varargs)
                if args_spec.varkw is not None:
                    arg_names.extend(args_spec.varkw)
                arg_names.extend(args_spec.kwonlyargs)
                break
    return arg_names


def _get_class_names(module: ModuleType) -> List[str]:
    names = []
    classes = inspect.getmembers(module, lambda member: inspect.isclass(member))
    for name, cls in classes:
        if cls.__module__ == module.__name__:
            names.append(name)
    return names


def _get_class_function_names(module: ModuleType, cls_name: str) -> List[str]:
    fn_names = []
    classes = inspect.getmembers(module, lambda member: inspect.isclass(member))
    for cls_name_, cls in classes:
        if cls.__module__ == module.__name__:
            if cls_name_ == cls_name:
                functions = inspect.getmembers(
                    cls,
                    lambda member: inspect.ismethod(member)
                    or inspect.isfunction(member),
                )
                for fn_name, fn in functions:
                    fn_names.append(fn.__qualname__)
                break
    return fn_names


def _get_class_function_arg_names(
    module: ModuleType, cls_name: str, fn_name: str
) -> List[str]:
    arg_names = []
    classes = inspect.getmembers(module, lambda member: inspect.isclass(member))
    for cls_name_, cls in classes:
        if cls.__module__ == module.__name__:
            if cls_name_ == cls_name:
                functions = inspect.getmembers(
                    cls,
                    lambda member: inspect.ismethod(member)
                    or inspect.isfunction(member),
                )
                for fn_name_, fn in functions:
                    if fn.__qualname__ == fn_name:
                        args_spec = inspect.getfullargspec(fn)
                        arg_names = args_spec.args
                        if args_spec.varargs is not None:
                            arg_names.extend(args_spec.varargs)
                        if args_spec.varkw is not None:
                            arg_names.extend(args_spec.varkw)
                        arg_names.extend(args_spec.kwonlyargs)
                        break
                break
    return arg_names
