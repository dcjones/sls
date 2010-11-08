Stochastic L-Systems
====================

SLS is a system for drawing a generalized Lindenmayer Systems. In particular, two
generalizations are made:

1. Context-free grammars are generalized to stochastic context-free grammars.
2. Drawing primitives take parameters which can be computed with a restricted
   subset of Python.


Writing SLS Programs
--------------------

Some prior familiarity with `L-systems <http://en.wikipedia.org/wiki/L-systems>`_
will be useful, but not necessary.


Drawing Primitives
^^^^^^^^^^^^^^^^^^

Drawing is performed using "turtle graphics". The commands control, in essence, a
little turtle who leaves a trail wherever he travels. The following commands are
recognized,

:F: Move forward.
:B: Move backwards.
:+: Turn right.
:-: Turn left.

All movement is relative to the turtle's current position and orientation.


Axioms
^^^^^^

All programs must start out with::
    
    S = ...

Where `...` is a list of primitives. This is the *axiom*, the initial rule
that is applied to draw the image. For example,::

    S = F+F-F

will draw an image by instructing the turtle to move forward, turn right, move
forward, turn left, then move forward once again.

Stacking States
^^^^^^^^^^^^^^^

Each drawing primitive changes the state of the turtle. Sometimes it is useful
to return to a previous state only to move off in another direction. This is done
with the stack commands,

:[: push/save   state
:]: pop/restore state

The ``[`` command saves the state and the ``]`` command restores the last state
that was saved.

For example, the following program draws a Y while avoiding backtracking. (Make
sure you understand why!)::

    S = F[+F]-F




Rules
^^^^^

Much more interesting images are created by repeatedly applying substitution
rules. All SLS programs are simply a list of these rules. A rule specifies a
symbol [#]_ that may be replaced by a one or more other symbols. For example,::

    X = YZ


Says that ``X`` may be replaced by ``XY``.

SLS draws images by exhaustively following these rules to build a long
list of turtle commands. Consider the program::

    S = X+F
    X = -F

Here, SLS will apply all of the rules, collapsing the axiom down to the
equivalent SLS program::

    S = [-F]+F

Note the brackets. The state is saved before each rule is applied and
restored afterward.

Now, for out first interesting example, consider the following program,::

    S = X
    X = F+X

Applying the ``X`` rule once gives us,::

    S = [F+X]
    X = F+X

Applying it a second time,::

    S = [F+[F+X]]
    X = F+X

And a third time,::

    S = [F+[F+[F+X]]]
    X = F+X

We could continue infinitely of course. In practice, SLS will only continue
following rules until a certain *depth* is reached. This program will draw a
pleasant spiral.

Why a spiral and not a polygon or circle? Because the default behavior of SLS is
that ``F`` moves the turtle less and less as more and more rules are applied.
This facilitate making self-similar fractal-like images, but is not hard-coded.
Varying the angle of turns and distance of moves is coming up. Stay tuned.



Symbol Reuse
^^^^^^^^^^^^
Particularly devious readers may ask the natural question. What if rules are
written replacing the drawing primitives?::

    S = F
    F = F

Ah, a tautology! In such an instance, the drawing command (``F``) is *both* performed
and replaced. The grammar above is equivalent to,::
    
    S = FX
    X = FX

Both are reducible to the program,::

    S = FFFFF...


Stochastic Rules
^^^^^^^^^^^^^^^^

We now arrive at the first generalization of standard L-systems.

Suppose we write a program with two competing rules::
    
    S = X
    X = +FX
    X = -FX

There are two rules to replace ``X``. How does SLS choose which one to apply?
Randomly, of course! Every time it wants to replace an X, it simply flips a coin
to choose which rule to apply.

We can also bias this coin toss by weighting rules, using a special syntax::

    S = X
    X:1 = +FX
    X:2 = -FX

Here the second rule is twice as likely to be chosen as the first. Weight may be
chosen to be any non-negative number. By default, every rule has a weight of 1.


Primitive Parameters
^^^^^^^^^^^^^^^^^^^^

By default, drawing primitives take fixed sized steps and turn by fixed angles.
These parameters can be varied by treating the primitives as functions
and passing parameters to them,::

    S = F(100)+(0.25)F(50)

This program instructs the turtle to move forward by 100,
turn right by 0.25, then move forward by 50.

Angles in SLS are specified on a [0,1] scale. So that angle ``t`` corresponds to
``2*t*pi`` radians or ``360*t`` degrees. Lengths are measured in pixels.


Expressions
^^^^^^^^^^^

Arguments to drawing primitives are evaluated with a restricted subset of
Python. The syntax is that of Python, but with the potentially dangerous bits
disabled to allow SLS to be run publicly.

In practice, this means that the parameters passed to drawing primitives can be
computed with almost arbitrary complex Python expressions. These expressions can
also involve (pseudo-)random numbers. Thus, we can send our intrepid little
turtle on a drunkard's walk::

    S = +(runif())F(runif(10,20))S

The ``runif(a,b)`` function generates a uniform number between ``a`` and ``b``,
where ``a = 0`` and ``b = 1`` by default.

A small set of functions are provided allowing for basic math and
random number generation. In addition, several constants are defined giving
information about the current state when the expression is evaluated.


Constants
^^^^^^^^^

:k: current iteration depth

:h: height of the image being generated

:w: width of the image being generated


Functions
^^^^^^^^^
:runif(low=0,high=1): random uniformly distributed number

:rnorm(mean=0,std=1): random Gaussian distributed number



Todo
----

Here a list of future work that could be done.

* Efficiency: SLS is rather slow right now, mostly as a result of evaluating
  python expressions. This could be improved by memoizing the results of
  expressions whose values will not change.

* More drawing primitives: in particular

  - Color
  - Curves
  - Polygons

* Random examples: come up with some handsome examples and provide an option in
  the website to draw one randomly.

* Allow comments within SLS programs.


Footnotes
---------

.. [#] A "symbol" in SLS is any letter, upper or lower case, followed by any
       number of digits.


