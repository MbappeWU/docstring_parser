"""Test for utility functions."""

from docstring_parser import parse
from docstring_parser.common import DocstringReturns, DocstringStyle
from docstring_parser.util import combine_docstrings


def test_combine_docstrings() -> None:
    """Test combine_docstrings wrapper."""

    def fun1(arg_a, arg_b, arg_c, arg_d):
        """short_description: fun1

        :param arg_a: fun1
        :param arg_b: fun1
        :return: fun1
        """
        assert arg_a and arg_b and arg_c and arg_d

    def fun2(arg_b, arg_c, arg_d, arg_e):
        """short_description: fun2

        long_description: fun2

        :param arg_b: fun2
        :param arg_c: fun2
        :param arg_e: fun2
        """
        assert arg_b and arg_c and arg_d and arg_e

    @combine_docstrings(fun1, fun2)
    def decorated1(arg_a, arg_b, arg_c, arg_d, arg_e, arg_f):
        """
        :param arg_e: decorated
        :param arg_f: decorated
        """
        assert arg_a and arg_b and arg_c and arg_d and arg_e and arg_f

    assert decorated1.__doc__ == (
        "short_description: fun2\n"
        "\n"
        "long_description: fun2\n"
        "\n"
        ":param arg_a: fun1\n"
        ":param arg_b: fun1\n"
        ":param arg_c: fun2\n"
        ":param arg_e: fun2\n"
        ":param arg_f: decorated\n"
        ":returns: fun1"
    )

    @combine_docstrings(fun1, fun2, exclude=[DocstringReturns])
    def decorated2(arg_a, arg_b, arg_c, arg_d, arg_e, arg_f):
        assert arg_a and arg_b and arg_c and arg_d and arg_e and arg_f

    assert decorated2.__doc__ == (
        "short_description: fun2\n"
        "\n"
        "long_description: fun2\n"
        "\n"
        ":param arg_a: fun1\n"
        ":param arg_b: fun1\n"
        ":param arg_c: fun2\n"
        ":param arg_e: fun2"
    )


def test_combine_preserves_attribute_priority() -> None:
    """Keep attribute precedence separate from function parameters."""

    def source_one(value):
        """:attribute value: source one
        :attribute other: other source
        """
        return value

    def source_two(value):
        """:attribute value: source two"""
        return value

    @combine_docstrings(source_one, source_two)
    def decorated(value):
        """:param value: function value
        :attribute value: wrapped attribute
        """
        return value

    docstring = parse(decorated.__doc__, style=DocstringStyle.REST)
    assert [
        (item.arg_name, item.description) for item in docstring.params
    ] == [("value", "function value")]
    assert [
        (item.arg_name, item.description) for item in docstring.attributes
    ] == [("value", "source one"), ("other", "other source")]
