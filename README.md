On a computer with Python 3 installed, you can run SimpleCAS by opening a terminal in the SimpleCAS folder and typing

```console
$> python -i CAS.py
```

SimpleCAS allows users to declare symbolic variables and interactively build and manipulate expressions using the Python interpreter. Additive and multiplicative expressions are created by using Python's `+`, `-`, `*`, and `/` operators, which correspond to symbolic addition, subtraction, multiplication, and division, respectively. 

For example, to represent the expression `2(x + 1) + 5y + z` in SimpleCAS, one way would be the following:

```python
>>> x = SymbolicVar("x")
>>> y = SymbolicVar("y")
>>> z = SymbolicVar("z")
>>> expr = SymbolicNum(2) * (x + SymbolicNum(1)) + SymbolicNum(5)*y + z
>>> print(expr)
(((2 × (x + 1)) + (5 × y)) + z)
```

You can also commute the sub-expressions:

```python
>>> expr.commute()
>>> print(expr)
(z + ((2 × (x + 1)) + (5 × y)))
```

The `SymbolicNum` type is used to represent all integer constants in SimpleCAS and enforces the non-negativity requirement of the spec. However, we also permit building expressions using the built-in `int` type, which makes it easier to work with SimpleCAS from inside the terminal. In particular, we can equivalently write:

```python
>>> x = SymbolicVar("x")
>>> y = SymbolicVar("y")
>>> z = SymbolicVar("z")
>>> expr = 2 * (x + 1) + 5*y + z
>>> print(expr)
(((2 × (x + 1)) + (5 × y)) + z)
```

However, note that a Python `int` will be converted to a `SymbolicNum` only when it is an operand in an expression involving a SimpleCAS `Expression`. For example, consider

```python
>>> a = SymbolicNum("a")
>>> print(a + 1 + 2)
((a + 1) + 2)
```

Here, the first operation executed in Python is `(a + 1)`, which involves the `SymbolicVar` (a subclass of `Expression`) `a` and the `int` 1. The `int` is converted into a `SymbolicNum` and then the resulting `CompoundExpression` is an operand in the second operation with the `int` 2, which is again converted to a `SymbolicNum`. On the other hand, consider

```python
>>> a = SymbolicNum("a")
>>> print(a + 1 * 2)
((a + 2)
```

Here, the first operation executed in Python is `(1 * 2)`, which is an expression involving only `int`s that evaluates to `2`. So to express `(a + 1 * 2)` (which is a valid expression as defined in the spec) in SimpleCAS, you would have to write:

```python
>>> a = SymbolicNum("a")
>>> print(a + SymbolicNum(1) * 2)
(a + (1 × 2))
```

Internally, symbolic expressions are represented as binary trees. For instance, the expression 
`2 * (x + 1) + 5*y + z` is represented by the binary tree below:

                                (+)
                              /     \
                            (+)     (z)
                           /    \
                         (×)    (×)
                        /   \   /  \
                       /     \ (5) (y)
                     (2)     (+)
                             /  \
                           (x)  (1)


Calling the `commute()` function on the above expression is just the operation of swapping the two sub-trees at the root.

I have included a few function declarations in CAS.py for some functions we might want to add in a future version of SimpleCAS, such as a 
specialization method which transforms a `SymbolicVar` to a `SymbolicNum`, or a method which automatically simplifies a `CompoundExpression` 
`A op B` where both `A` and `B` are instances of `SymbolicNum` (at least when the result satisfies the non-negative requirement of a `SymbolicNum`).
