# UnitTest Resolver

Execute all unittests that refers to a specific function in python. Build as an extension to Contour.

## Goal
1. Extract unittest separately.
2. Run the specific scope through ast compilation.


## Random Thoughts
1. Context object should have an object of the declaration itself
2. Search must use a recursion unless you want to use a Tuple to keep track of the contexts
3. Paths resolve the problem with collision.w