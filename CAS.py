"""
A simple computer algebra system which extends the Python interpreter.

EXAMPLES::

>>> a = SymbolicVar("a")
>>> ten = SymbolicNum(10)
>>> print(a + ten)
(a + 10)

::

>>> a = SymbolicVar("a")
>>> b = SymbolicVar("b")
>>> expr1 = a + 1
>>> expr2 = 2 - b + 3*a
>>> print(expr1 - expr2)
((a + 1) - ((2 - b) + (3 × a)))

::

>>> x = SymbolicVar("x")
>>> y = SymbolicVar("y")
>>> z = SymbolicVar("z")
>>> expr = 2 * (x+1) + 5*y + z
>>> print(expr)
(((2 × (x + 1)) + (5 × y)) + z)
>>> expr.commute()
>>> print(expr)
(z + ((2 × (x + 1)) + (5 × y)))

AUTHORS:

- Joey Lupo (03/22/2022): initial version

"""

from enum import Enum
from typing import Any, Optional

class Node:
    """A node in a binary tree."""

    def __init__(
            self, 
            val : Any,
            left: Optional["Node"] = None, 
            right: Optional["Node"] = None) -> None:
        """Init a Node."""
        self.val = val
        self.left = left
        self.right = right
    
    def __str__(self) -> str:
        """Print the value stored at the Node."""
        return str(self.val)

class Operator(Enum):
    """
    Math operators for addition, subtraction, multiplication, and division.
    
    Values are given as the Unicode code points of the respective math symbol.
    In order to better interface with Python, we would probably want to 
    replace the '×' multiplication character (U+00D7) with the '*' character
    (U+002A) and the '÷' division character (U+00F7) with the '/' character
    (U+002F).
    
    EXAMPLE:

    >>> for op in Operator:
    >>>     print(op)
    +
    -
    ×
    ÷
    """

    add = 0x2B 
    sub = 0x2D
    mul = 0xD7 
    div = 0xF7  

    def __str__(self) -> str:
        """Print the Unicode representation of the operator."""
        return chr(self.value)

class Expression(Node):
    """
    A symbolic expression, represented as a binary tree.

    The binary tree is stored implicitly as a Node (the root of the tree). 
    All symbolic expressions are represented in SimpleCAS as one of:

    (1) SymbolicVar
    (2) SymbolicNum
    (3) CompoundExpression

    For (1) and (2), the underlying tree is a Node with no children, whereas
    for (3), the root of the binary tree is a Node with an Expression
    (represented recursively as a binary tree) on each of the two branches.
    """
    
    def _op(
            self, 
            other: Any, 
            op: "Operator", 
            right: bool = False) -> "CompoundExpression":
        """
        Build a CompoundExpression from an Operator and two 'Expression's.
        
        We also handle the case that the user builds an expression with a
        Python 'int' in place of a SymbolicNum, so that writing

        >>> expr = 5 * SymbolicVar("a")

        is equivalent to writing

        >>> expr = SymbolicNum(5) * SymbolicVar("a")
        """
        if isinstance(other, int):
            if not right:
                return CompoundExpression(op, self, SymbolicNum(other))
            else:
                return CompoundExpression(op, SymbolicNum(other), self)
        elif isinstance(other, Expression):
            if not right:
                return CompoundExpression(op, self, other)
            else:
                return CompoundExpression(op, other, self)
        else:
            return NotImplemented

    def __add__(self, other: Any) -> "CompoundExpression":
        """
        Overload Python's '+' operator to combine two 'Expression's.
        
        Expression.__add__ is invoked in the case that we have a (Python)
        expression of the form A + B, where A is an instance of Expression.
        The __<op>__ methods below are invoked similarly for the respective
        <op>'s. 
        """
        return self._op(other, Operator.add)

    def __radd__(self, other: Any) -> "CompoundExpression":
        """
        Overload Python's '+' operator to combine two 'Expression's.
        
        Here, Expression.__radd__ is invoked in the case that we have a 
        (Python) expression of the form A + B, where B is an instance of 
        Expression. The __r<op>___ methods below are invoked similarly for
        the respective <op>'s.
        """
        return self._op(other, Operator.add, right=True)

    def __sub__(self, other: Any) -> "CompoundExpression":
        """Overload Python's '-' operator to combine two 'Expression's."""
        return self._op(other, Operator.sub)

    def __rsub__(self, other: Any) -> "CompoundExpression":
        """Overload Python's '-' operator to combine two 'Expression's."""
        return self._op(other, Operator.sub, right=True)

    def __mul__(self, other: Any) -> "CompoundExpression":
        """Overload Python's '*' operator to combine two 'Expression's."""
        return self._op(other, Operator.mul)

    def __rmul__(self, other: Any) -> "CompoundExpression":
        """Overload Python's '*' operator to combine two 'Expression's."""
        return self._op(other, Operator.mul, right=True)
    
    def __truediv__(self, other: Any) -> "CompoundExpression":
        """Overload Python's '/' operator to combine two 'Expression's."""
        return self._op(other, Operator.div)

    def __rtruediv__(self, other: Any) -> "CompoundExpression":
        """Overload Python's '/' operator to combine two 'Expression's."""
        return self._op(other, Operator.div, right=True)

    def __eq__(self, other: Any) -> bool:
        """
        Determine if two 'Expression's are equal.

        There are a couple interpretations/directions we could go with to 
        define equality. It could be a strict equality in the sense of a 
        theorem prover where Expression A is represented by a string which is
        exactly identical to the string representation of Expression B (since)
        the parentheses in the output string group together the sub-
        expression components. To implement this in SimpleCAS, we could do a 
        traversal of the two binary trees underlying each A and B and 
        determine if they are identical. 
        
        However, equality gets trickier to implement if we want to, e.g. have 
        (A + B) + C == A + (B + C) return True. This type of equality would 
        involve some level of automation to simplify/rewrite one side using 
        laws such as associativity, commutativity, distributivity, etc. 
        """
        pass

    def __str__(self) -> str:
        """
        Recursively print an expression using in-order traversal of the tree.

        The parentheses in the output delineate compound expressions. A more 
        complex implementation of this function might better decide when
        parentheses should be printed. For example, instead of the current
        implementation returning "((A + B) + 5)", we might want to return
        "A + B + 5" instead.
        """
        left = str(self.left) if self.left is not None else ""
        right = str(self.right) if self.right is not None else ""
        if left == "" and right == "":
            return str(self.val)
        else:
            return "(" + left + " " + str(self.val) + " " + right + ")"

class CompoundExpression(Expression):
    r"""
    Represent expressions which are expressions composed with operators.

    A CompoundExpression is an expression of the form A op B, where A and B
    are instances of Expression and op is an Operator. In SimpleCAS, we rep-
    resent an additive or a multiplicative expression as an instance of
    CompoundExpression. For example, the additive expression a + b + 5 is 
    represented as A op B, where A := SymbolicVar("a") + SymbolicVar("b"), 
    op := Operator.add, and B := SymbolicNum(5). Note that A is itself a
    CompoundExpression.

    The underlying representation of a CompoundExpression is then a binary
    tree with an Operator as the value in the root Node, and an Expression as 
    the left child and an Expression as the right child. For example,for the 
    CompoundExpression defined by (a + b) - 5, the underlying binary tree 
    looks like this:

                                (-)
                               /   \
                             (+)   (5)
                             / \
                           (a) (b)
    """

    def __init__(
            self, 
            op: "Operator", 
            left: "Expression", 
            right: "Expression") -> None:
        """Init CompoundExpression from an Operator and two 'Expression's."""
        if (not isinstance(left, Expression) 
                or not isinstance(right, Expression)):
            raise TypeError("'left' and 'right' must be of type Expression.")
        super().__init__(op, left, right)

    def additive(self) -> bool:
        """
        For a CompoundExpression A op B, return True iff op is + or -.

        EXAMPLES:

        >>> a = SymbolicVar("a")
        >>> b = SymbolicVar("b")
        >>> expr = 10*a + b
        >>> print(expr)
        ((10 × a) + b)
        >>> expr.additive()
        True

        ::

        >>> a = SymbolicVar("a")
        >>> b = Symbolicvar("b")
        >>> expr = 10 * (a+b)
        >>> print(expr)
        (10 × (a + b))
        >>> expr.additive()
        False
        """
        return self.val == Operator.add or self.val == Operator.sub

    def multiplicative(self) -> bool:
        """
        For a CompoundExpression A op B, return True iff op is × or ÷.

        EXAMPLES:

        >>> a = SymbolicVar("a")
        >>> b = SymbolicVar("b")
        >>> expr = 10*a + b
        >>> print(expr)
        ((10 × a) + b)
        >>> expr.multiplicative()
        False

        ::

        >>> a = SymbolicVar("a")
        >>> b = Symbolicvar("b")
        >>> expr = 10 * (a+b)
        >>> print(expr)
        (10 × (a + b))
        >>> expr.multiplicative()
        True
        """ 
        return self.val == Operator.mul or self.val == Operator.div

    def assoc_right(self) -> None: 
        """Transform a CompoundExpression (A op B) op C -> A op (B op C)."""
        pass

    def assoc_left(self) -> None:
        """Transform a CompoundExpression A op (B op C) -> (A op B) op C."""
        pass

    def commute(self) -> None:
        """
        Transform a CompoundExpression A op B -> B op A.

        We swap the two branches of the binary tree. Note that the spec 
        doesn't specify whether to make sure this operation makes sense 
        mathematically, i.e. we don't check whether op is actually a 
        commutative operator (e.g. add and mul), though these checks could be
        added.

        EXAMPLES: 
        >>> a = SymbolicVar("a")
        >>> b = SymbolicVar("b")
        >>> expr = a + b
        >>> expr.commute()
        >>> print(expr)
        (b + a)

        ::

        >>> x = SymbolicVar("x")
        >>> y = SymbolicVar("y")
        >>> z = SymbolicVar("z")
        >>> expr = 2 * (x+1) + 5*y + z
        >>> print(expr)
        (((2 × (x + 1)) + (5 × y)) + z)
        >>> expr.commute()
        >>> print(expr)
        (z + ((2 × (x + 1)) + (5 × y)))
        """
        self.left, self.right = self.right, self.left

class SymbolicVar(Expression):
    """
    A single character symbol expression. 

    This type corresponds to the first expression type described in the spec.

    EXAMPLES:

    >>> a = SymbolicVar("a") 
    >>> expr = a + SymbolicVar("b")
    >>> print(expr)
    (a + b)

    ::

    >>> abc = SymbolicVar("abc")
    ValueError: Symbol name must be an upper or lower-case string of length 1.
    """

    def __init__(self, name: str) -> None:
        """Init a single character symbol."""
        if (len(name) == 1
                and isinstance(name, str)
                and ((97 <= ord(name) <= 122) or (65 <= ord(name) <= 90))):
            super().__init__(Node(name))
        else:
            raise ValueError("Symbol name must be an upper or lower-case " 
                "string of length 1.")

    def specialize(self, val: int) -> "SymbolicNum":
        """
        Here we might want to implement functionality to specialize a variable
        to some value. In the case of the spec, this specialization would 
        most likely be to a non-negative integer.
        """
        pass

class SymbolicNum(Expression):
    """
    A non-negative, unbounded integer.
    
    This type corresponds to the second expression type described in the spec.
    An alternate construction would be to subclass the built-in 'int' type.

    EXAMPLES:

    >>> ten = SymbolicNum(10)
    >>> a = SymbolicVar("a")
    >>> print(a + ten)
    (a + 10)

    ::

    >>> neg = SymbolicNum(-1)
    ValueError: Constant must be a non-negative integer.
    """

    def __init__(self, val: int) -> None:
        """Init a SymbolicNum from a non-negative integer."""
        if isinstance(val, int) and 0 <= val:
            super().__init__(Node(val))
        else:
            raise ValueError("Constant must be a non-negative integer.")

    def _op(
            self, 
            other: Any, 
            op: Operator, 
            right: bool = False) -> "Expression":
        """
        Here we could overwrite Expression._op as well as the __add__,
        __mul__, etc. methods to automatically reduce an expression of the
        form SymbolicNum(i) op SymbolicNum(j) -> SymbolicNum(i op j) whenever
        i op j forms a valid non-negative integer. However, since the spec 
        does not say to make such simplifications, we do not implement this
        functionality. 
        """
        pass
