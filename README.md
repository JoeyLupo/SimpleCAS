On a computer with Python 3 installed, you can run SimpleCAS by opening a terminal in the SimpleCAS folder and typing

$> python -i CAS.py

SimpleCAS allows users to declare symbolic variables and interactively build and manipulate expressions using the Python interpreter. Additive and multiplicative expressions are created by using Python's +, -, *, and / operators, which correspond to symbolic addition, subtraction, multiplication, and division, respectively. 

For example, to represent the expression 2(x + 1) + 5y + z in SimpleCAS, one way would be the following:

>>> x = SymbolicVar("x")
>>> y = SymbolicVar("y")
>>> z = SymbolicVar("z")
>>> expr = SymbolicNum(2) * (x + SymbolicNum(1)) + SymbolicNum(5)*y + z
>>> print(expr)
(((2 × (x + 1)) + (5 × y)) + z)

The 'SymbolicNum' type is used to represent all integer constants in SimpleCAS and enforces the non-negativity requirement of the spec. However, we also permit building expressions using the built-in 'int' type, which makes it easier to work with SimpleCAS from inside the terminal. In particular, we can equivalently write:

```python
>>> x = SymbolicVar("x")
>>> y = SymbolicVar("y")
>>> z = SymbolicVar("z")
>>> expr = 2 * (x + 1) + 5*y + z
>>> print(expr)
(((2 × (x + 1)) + (5 × y)) + z)
```

You can also commute the sub-expressions:

>>> expr.commute()
>>> print(expr)
(z + ((2 × (x + 1)) + (5 × y)))

Internally, symbolic expressions are represented as binary trees. For instance, the expression 
2 * (x + 1) + 5*y + z is represented by the binary tree below:

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


Calling the commute() function on the above expression is just the operation of swapping the two sub-trees at the root.

I have also included function declarations in CAS.py for some functions we might want to add in a future version of SimpleCAS, such as a 
specialization method which transforms a SymbolicVar to a SymbolicNum, or a method which automatically simplifies a CompoundExpression 
A op B where both A and B are instances of SymbolicNum (at least when the result satisfies the non-negative requirement of a SymbolicNum).
