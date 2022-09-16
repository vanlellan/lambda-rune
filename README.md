# lambda-rune
A system for graphically representing the [Lambda Calculus](https://en.wikipedia.org/wiki/Lambda_calculus), a Turing-complete functional model of computation.

For a simple test, try `python rune.py "Labc.babc"`.

For something more complicated, try `python rune.py "Lnfx.n[Lgh.hgf][Lu.x][Lu.u]"`.

How to read a rune
---
![successor](https://user-images.githubusercontent.com/19508710/190049088-36df366d-42c4-496e-9139-f5ca5ec7aef3.png)
 - The outer ring is the *head* of the lambda expression. The small circle at the top is the start node.
 - Begin reading this outer ring clockwise from the start node. Each vertex in the inscribed polygon (other than the start node) indicates the presence of a variable in the head.
    - For example, if the inscribed shape is a square, there are three variables present in the head of the lambda expression.
 - Once you've looped around the outer ring once, jump to the location on the inner ring that is directly inward from the start node. This is the *body* of the lambda expression.
 - Read clockwise around the body. Each vertex (or "node") in the polygon inscribed in the inner ring indicates the position of a variable in the body.
     - Arcs between inner nodes and outer nodes are used to indicate which variables are which.
     - Thin arcs between empty spaces on the inner circle are used to indicate groupings of variables, like parentheses. Expressions are left-associative, e.g. a variable is applied to the variable or group of variables immediately clockwise around the circle from it.
     
The nodes in the outer ring of the rune above can be assigned arbitrary variables, such as a, b, and c. The inner ring then reads b (a b c), according to the arcs linking the nodes of the outer ring to the inner ring. Thus, this rune represents the lambda expression Labc.b(abc), which is the SUCCESSOR function.
