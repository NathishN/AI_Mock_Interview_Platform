"""Generator for Category D: Python and Programming Fundamentals (60 questions).
20 questions in 01.json, 20 in 02.json, 20 in 03.json.
Technical category: questions include concise code snippets, explanations, key points, common mistakes, follow-ups.
"""
import json
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parents[2] / "data" / "src" / "D_python"

PART1 = [
    {
        "q": "What is the core difference between mutable and immutable data types in Python? Give examples of each.",
        "sub": "Data Types & Mutability",
        "d": "Beginner",
        "ans": "In Python, mutability defines whether an object's state or contents can be altered in place after creation without changing its memory identity (id). Mutable types allow in-place modification (e.g., list, dict, set, bytearray). Immutable types cannot be altered once created; any modification produces a completely new object in memory (e.g., int, float, str, tuple, frozenset, bool, bytes). For example, appending to a list keeps the same id(my_list), whereas appending to a string creates a new string object with a different id. Understanding this distinction is vital to prevent unintentional side effects when passing objects as function arguments.",
        "kp": ["Mutable objects can be modified in place with unchanged id()", "Immutable objects create a new memory object on modification", "Mutable examples: list, dict, set; Immutable: int, float, str, tuple", "Function argument side effects differ based on mutability"],
        "cm": ["Believing tuples are mutable if they contain lists", "Confusing variable reassignment with in-place mutation", "Using mutable default arguments in functions"],
        "fu": ["What happens if an immutable tuple contains a mutable list element?", "How does Python optimize small integers and short strings in memory via interning?"],
        "tags": ["python", "mutability", "data-types", "memory"]
    },
    {
        "q": "Why is using a mutable default argument like `def func(x=[])` considered a dangerous anti-pattern in Python?",
        "sub": "Functions & Scoping",
        "d": "Intermediate",
        "ans": "In Python, default parameter expressions are evaluated once at function definition time (when the module is loaded), not each time the function is invoked. If a mutable object like a list `[]` or dictionary `{}` is used as a default, that single object instance is shared across all subsequent invocations that do not explicitly supply an argument. Calling `func(1)` and then `func(2)` will cause the list to accumulate both values: `[1, 2]`. The idiomatic and safe pattern is to use `None` as the default sentinel and initialize a new container inside the function body: `def func(x=None): if x is None: x = []`.",
        "kp": ["Default arguments evaluated once at definition time, not call time", "Mutable defaults persist state across function calls", "Can cause severe unintended side effects and bugs", "Safe idiom: use None as default and instantiate inside function body"],
        "cm": ["Believing a new list is created on every function invocation", "Using dict or set literals as default arguments", "Relying on shared default state as a hacky cache"],
        "fu": ["How can you inspect a function's default arguments using the `__defaults__` attribute?", "Are there any rare cases where mutable defaults are used intentionally?"],
        "tags": ["python", "functions", "anti-patterns", "scoping"]
    },
    {
        "q": "Compare lists, tuples, sets, and dictionaries in Python in terms of ordering, indexing, and lookup complexity.",
        "sub": "Data Structures",
        "d": "Beginner",
        "ans": "Lists and tuples are ordered sequences; lists are mutable with O(1) indexed lookup and O(n) membership search, whereas tuples are immutable with the same complexity but lower memory footprint and hashability. Sets are unordered, mutable collections of unique, hashable elements; they provide average O(1) membership testing and insertion via hash tables. Dictionaries are ordered (since Python 3.7) key-value mappings requiring unique hashable keys; they offer average O(1) key retrieval, insertion, and deletion. Choosing the right structure depends on requirements for order, uniqueness, mutability, and fast search.",
        "kp": ["List: ordered, mutable, indexed, O(n) search", "Tuple: ordered, immutable, indexed, hashable if items are hashable", "Set: unordered, unique elements, hash-based O(1) lookup", "Dict: key-value pairs, insertion-ordered, hash-based O(1) lookup"],
        "cm": ["Using a list for frequent membership checks (`if item in collection`) instead of a set", "Attempting to use unhashable lists as dictionary keys", "Assuming sets maintain element insertion order like lists"],
        "fu": ["Why do sets and dicts provide O(1) lookups whereas lists require O(n)?", "What causes hash collisions in Python dictionaries and how does Python resolve them?"],
        "tags": ["python", "data-structures", "time-complexity", "hash-table"]
    },
    {
        "q": "What is the difference between shallow copy and deep copy in Python? How do you implement each?",
        "sub": "Memory & Copying",
        "d": "Intermediate",
        "ans": "A shallow copy creates a new compound object, but populates it with references to the child objects found in the original. Consequently, mutating a nested mutable child inside a shallow copy reflects in the original object. A deep copy, created via `copy.deepcopy()`, recursively clones both the compound object and all child objects it contains, ensuring complete memory isolation. Shallow copies can be created using `copy.copy()`, slicing `[:]`, or constructors `list(orig)`. Deep copies require the `copy` module. Deep copying has higher memory and computational overhead and may encounter recursion limits with circular references.",
        "kp": ["Shallow copy creates new outer container with shared child references", "Deep copy recursively copies all nested objects for full isolation", "Shallow copy methods: copy.copy(), [:], list() constructor", "Deep copy method: copy.deepcopy()"],
        "cm": ["Assuming list.copy() or slicing [:] creates a deep copy of nested lists", "Using deepcopy unnecessarily when shallow copy suffices, wasting CPU/memory", "Not realizing that simple variable assignment (b = a) creates no copy at all"],
        "fu": ["What happens when deepcopy encounters a self-referential or cyclic data structure?", "How does the `__deepcopy__` dunder method allow custom copying behavior?"],
        "tags": ["python", "shallow-copy", "deep-copy", "memory"]
    },
    {
        "q": "How does Python handle memory management and garbage collection under the hood?",
        "sub": "Memory Management",
        "d": "Advanced",
        "ans": "CPython manages memory primarily through reference counting supplemented by a generational cyclic garbage collector. Every object contains an internal reference counter (`ob_refcnt`) tracking how many references point to it. When an object's reference count drops to zero, its memory is deallocated immediately. However, reference counting fails on circular references (e.g., Object A references B, and B references A). To reclaim circular references, CPython's cyclic garbage collector (`gc` module) periodically inspects objects divided into three generations (Gen 0, 1, 2). Younger generations are collected more frequently using reachability graph traversal.",
        "kp": ["Primary mechanism: Reference counting with immediate deallocation at count zero", "Secondary mechanism: Generational cyclic garbage collection (3 generations)", "Circular references resolved via reachability graph traversal", "Python small object allocator (PyMalloc) optimizes allocations <= 512 bytes"],
        "cm": ["Believing Python only uses a Java-style mark-and-sweep garbage collector", "Assuming del object immediately frees memory without considering lingering references", "Ignoring memory leaks caused by circular references holding external resources"],
        "fu": ["How can you inspect an object's current reference count using `sys.getrefcount()`?", "How does the `weakref` module help prevent cyclic reference memory leaks?"],
        "tags": ["python", "garbage-collection", "memory", "cpython", "internals"]
    },
    {
        "q": "What is the Global Interpreter Lock (GIL) in CPython, and how does it affect multithreading vs multiprocessing?",
        "sub": "Concurrency & GIL",
        "d": "Advanced",
        "ans": "The Global Interpreter Lock (GIL) is a mutex in CPython that restricts execution of Python bytecode to a single OS thread at a time, even on multi-core processors. It protects CPython's memory management and reference counting from race conditions. As a result, standard multithreading (`threading` module) does not achieve CPU parallelism for CPU-bound tasks like mathematical computation or image processing. However, multithreading is highly effective for I/O-bound tasks (network requests, disk I/O, database queries) because threads release the GIL while waiting on I/O. For CPU-bound tasks, multiprocessing (`multiprocessing` module) bypasses the GIL by spawning separate OS processes with dedicated interpreter instances and memory spaces.",
        "kp": ["GIL ensures only one thread executes Python bytecode at any moment", "Protects CPython reference counting and internal memory state", "Multithreading accelerates I/O-bound tasks by releasing GIL during I/O waits", "Multiprocessing achieves true multi-core CPU parallelism by using separate processes"],
        "cm": ["Assuming multithreading will speed up CPU-heavy mathematical loops in Python", "Believing the GIL prevents race conditions in application-level shared data", "Ignoring inter-process communication (IPC) serialization overhead in multiprocessing"],
        "fu": ["Why does Python 3.13 introduce experimental free-threaded (no-GIL) Python?", "When would you prefer asyncio over threading for high-concurrency network services?"],
        "tags": ["python", "gil", "multithreading", "multiprocessing", "concurrency"]
    },
    {
        "q": "Explain the difference between an iterable, an iterator, and a generator in Python.",
        "sub": "Iterators & Generators",
        "d": "Intermediate",
        "ans": "An iterable is any object capable of returning its members one at a time; it implements the `__iter__()` method (e.g., list, str, dict). An iterator is a stateful object that produces successive values via the `__next__()` method and raises `StopIteration` when exhausted; it also implements `__iter__()` returning self. A generator is a specialized, concise iterator written either as a function using the `yield` keyword or as a generator expression `(x for x in data)`. When a generator function yields, its execution frame and local variable state are suspended and resumed on subsequent `next()` calls, enabling lazy, memory-efficient streaming of large sequences.",
        "kp": ["Iterable implements `__iter__()` returning an iterator", "Iterator implements `__next__()` and raises `StopIteration` when done", "Generator functions use `yield` to pause and resume execution", "Lazy evaluation avoids loading entire datasets into memory at once"],
        "cm": ["Attempting to call next() directly on a list iterable without calling iter() first", "Thinking generator functions execute completely upon initial call rather than on next()", "Trying to reuse an exhausted iterator or generator"],
        "fu": ["What is the memory difference between `[x*2 for x in range(1000000)]` and `(x*2 for x in range(1000000))`?", "How does the `yield from` syntax simplify nested generator delegation?"],
        "tags": ["python", "iterators", "generators", "yield", "lazy-evaluation"]
    },
    {
        "q": "What is a decorator in Python, and how does `functools.wraps` preserve metadata?",
        "sub": "Decorators",
        "d": "Intermediate",
        "ans": "A decorator is a callable that takes another function as an argument, extends or modifies its behavior without modifying its source code, and returns a callable. Decorators are applied using the `@decorator` syntax. Common use cases include logging, authentication, caching, and execution timing. Because the inner wrapper function replaces the original function, metadata such as `__name__`, `__doc__`, and parameter signatures are overwritten by the wrapper. Applying `@functools.wraps(func)` to the inner wrapper copies the original function's attributes, ensuring docstrings, debugging tools, and reflection work correctly.",
        "kp": ["Decorators wrap functions to extend behavior without modifying source", "Syntax `@dec` is syntactic sugar for `func = dec(func)`", "Decorators take a function, define an inner wrapper, and return the wrapper", "functools.wraps preserves `__name__`, `__doc__`, and signature metadata"],
        "cm": ["Forgetting to use @functools.wraps, losing original function docstrings and names", "Forgetting to return the inner wrapper from the outer decorator function", "Not accepting *args and **kwargs in the wrapper, breaking varied argument signatures"],
        "fu": ["How do you write a decorator that accepts its own configuration arguments (e.g., `@repeat(num=3)`)?", "In what order are stacked decorators evaluated and executed?"],
        "tags": ["python", "decorators", "functools", "meta-programming"]
    },
    {
        "q": "Explain `*args` and `**kwargs` in Python function definitions and how argument unpacking works.",
        "sub": "Functions & Arguments",
        "d": "Beginner",
        "ans": "`*args` allows a function to accept an arbitrary number of positional arguments as a tuple, while `**kwargs` allows it to accept an arbitrary number of keyword arguments as a dictionary. The identifiers `args` and `kwargs` are conventions; the preceding asterisks `*` and `**` perform the syntactic unpacking. In function definitions, parameter order must be: standard positional parameters, `*args`, keyword-only parameters, and finally `**kwargs`. In function calls, `*iterable` unpacks sequence items into separate positional arguments, and `**dict` unpacks key-value pairs into keyword arguments.",
        "kp": ["`*args` collects extra positional arguments into a tuple", "`**kwargs` collects extra keyword arguments into a dictionary", "Order: positional -> `*args` -> keyword-only -> `**kwargs`", "Can be used in function calls to unpack iterables and dictionaries"],
        "cm": ["Placing positional arguments after `*args` without treating them as keyword-only", "Using `**kwargs` before `*args` in function signatures (causes SyntaxError)", "Thinking the words must strictly be 'args' and 'kwargs' instead of the asterisk prefix"],
        "fu": ["What are keyword-only arguments and how do you define them using a bare `*`?", "How can dictionary unpacking `**` be used to merge two dictionaries in Python 3.5+?"],
        "tags": ["python", "functions", "args-kwargs", "unpacking"]
    },
    {
        "q": "How does Object-Oriented Programming in Python implement inheritance, polymorphism, and encapsulation?",
        "sub": "OOP Fundamentals",
        "d": "Intermediate",
        "ans": "Python implements OOP through classes: 1) Inheritance allows a child class to inherit attributes and methods from a parent class using `class Child(Parent):`, with `super()` used to call parent methods. 2) Polymorphism enables different classes to implement methods with the same name, allowing uniform treatment via duck typing ('if it walks like a duck and quacks like a duck, it is a duck'). 3) Encapsulation restricts direct access to internal state through naming conventions: a single leading underscore `_attr` signals a protected attribute (by convention), while a double leading underscore `__attr` triggers name mangling (`_ClassName__attr`) to prevent accidental subclass overrides. Python does not enforce private attributes with hard keywords.",
        "kp": ["Inheritance via `class Sub(Super):` and `super().__init__()`", "Polymorphism achieved through duck typing and uniform method interfaces", "Encapsulation via naming conventions: `_protected` and `__private` (name mangling)", "No strict private keywords; Python favors the 'consenting adults' philosophy"],
        "cm": ["Assuming double underscore `__` provides absolute cryptographic privacy", "Failing to call super().__init__() in derived class constructors", "Overusing deep inheritance hierarchies instead of object composition"],
        "fu": ["How does Method Resolution Order (MRO) and the C3 linearization algorithm work in multiple inheritance?", "What is the role of the `@property` decorator in pythonic encapsulation?"],
        "tags": ["python", "oop", "inheritance", "polymorphism", "encapsulation"]
    },
    {
        "q": "What is the difference between `__str__` and `__repr__` in Python? When should you implement each?",
        "sub": "Dunder Methods",
        "d": "Intermediate",
        "ans": "Both are special dunder methods that return string representations of an object. `__repr__` is intended for developers; its goal is to be unambiguous, detailed, and ideally valid Python code that could recreate the object (e.g., `Car(make='Toyota', year=2022)`). It is invoked by `repr()`, interactive shells, and inside container displays. `__str__` is intended for end users; its goal is to be readable, concise, and clean (e.g., `Toyota (2022)`). It is invoked by `str()` and `print()`. If `__str__` is not defined on a class, Python falls back automatically to `__repr__`. Therefore, best practice is to always implement `__repr__` first.",
        "kp": ["`__repr__`: unambiguous, developer-focused, used by debugger and interactive REPL", "`__str__`: readable, user-friendly, used by print() and str()", "Python falls back to `__repr__` if `__str__` is absent", "Rule of thumb: always define `__repr__` at minimum"],
        "cm": ["Defining `__str__` while leaving `__repr__` undefined, causing lists of objects to show default memory pointers", "Returning non-string types from either method, which raises TypeError", "Writing overly long, unreadable repr strings"],
        "fu": ["Why does printing a list of custom objects `[obj]` call `__repr__` on each element instead of `__str__`?", "How does the `!r` format specifier work in f-strings like `f'{val!r}'`?"],
        "tags": ["python", "dunder-methods", "oop", "debugging"]
    },
    {
        "q": "How do list comprehensions differ from generator expressions in performance and memory usage?",
        "sub": "Comprehensions",
        "d": "Beginner",
        "ans": "A list comprehension `[expr for item in iterable if condition]` evaluates eagerly, constructing and allocating the entire list in memory immediately. It offers fast iteration speed because bytecode operations are optimized in C, but consumes O(n) memory proportional to the collection size. A generator expression `(expr for item in iterable if condition)` evaluates lazily, producing values on-demand one item at a time via the iterator protocol with O(1) constant memory overhead. Use list comprehensions when you need multiple passes, indexing, or len(); use generator expressions when streaming large data sequences, pipelines, or feeding single-pass reductions like `sum()` or `any()`.",
        "kp": ["List comprehension: eager evaluation, O(n) memory allocation, fast multiple-pass access", "Generator expression: lazy evaluation, O(1) memory, computes on demand", "Syntax: brackets `[...]` vs parentheses `(...)`", "Generator expressions ideal for streaming and memory-constrained environments"],
        "cm": ["Loading multi-gigabyte files into memory using list comprehensions", "Attempting to index or check len() on a generator expression", "Nesting 3+ comprehensions together, destroying code readability"],
        "fu": ["Can you write a dictionary comprehension and set comprehension example?", "Why is `sum(x for x in data)` memory-superior to `sum([x for x in data])`?"],
        "tags": ["python", "list-comprehension", "generators", "memory-optimization"]
    },
    {
        "q": "How does Python's `try...except...else...finally` block work? When does the `else` clause execute?",
        "sub": "Exception Handling",
        "d": "Beginner",
        "ans": "Python's exception handling structure has four distinct parts: 1) `try` contains code that may raise an exception. 2) `except` catches and handles specific matching exceptions. 3) `else` runs strictly if the `try` block completed without raising any exceptions; it separates normal follow-up code from code that requires try-catching, preventing accidental handling of unexpected errors. 4) `finally` runs unconditionally before exiting the construct, regardless of whether exceptions were raised, caught, or unhandled—even if return statements occur inside try or except blocks. `finally` is used for guaranteed resource cleanup (closing files, releasing locks).",
        "kp": ["`try`: wraps risky code", "`except`: catches specific exception types (never bare except)", "`else`: executes only if try succeeded with zero exceptions", "`finally`: executes guaranteed cleanup under all circumstances"],
        "cm": ["Using bare `except:` or `except Exception:` blindly, hiding syntax and interrupt errors", "Placing all code inside `try` instead of using `else` for code that shouldn't throw", "Assuming `finally` can be skipped by putting a `return` in `try`"],
        "fu": ["What happens if both `try` and `finally` contain `return` statements?", "Why is catching `BaseException` directly strongly discouraged?"],
        "tags": ["python", "exception-handling", "control-flow", "error-handling"]
    },
    {
        "q": "What are context managers in Python? How does the `with` statement work and how do you write a custom one?",
        "sub": "Context Managers",
        "d": "Intermediate",
        "ans": "Context managers govern runtime context for code blocks, ensuring deterministic acquisition and release of resources (e.g., file descriptors, database connections, locks). The `with` statement triggers the context management protocol: it calls `__enter__()` before the block executes and guarantees `__exit__(exc_type, exc_val, exc_tb)` is called when leaving the block, even if an exception occurs. To build a custom context manager, you can implement a class with `__enter__` and `__exit__`, or write a generator function decorated with `@contextlib.contextmanager`, placing setup before `yield` and teardown in a `finally` block.",
        "kp": ["Deterministic resource cleanup via `__enter__` and `__exit__` protocol", "`with` statement eliminates manual try-finally cleanup blocks", "Custom creation via class protocol or `@contextlib.contextmanager` decorator", "`__exit__` receives exception details and can suppress errors by returning True"],
        "cm": ["Forgetting to close opened file handles when avoiding `with` blocks", "Not placing teardown logic inside `finally` when using `@contextmanager`", "Accidentally suppressing all exceptions by returning a truthy value in `__exit__`"],
        "fu": ["How does `__exit__` suppress an exception versus letting it propagate upward?", "What is `contextlib.ExitStack` and when is it useful for managing dynamic resources?"],
        "tags": ["python", "context-manager", "with-statement", "resource-management"]
    },
    {
        "q": "What is the difference between `is` and `==` in Python? Give an example where they produce different results.",
        "sub": "Operators & Identity",
        "d": "Beginner",
        "ans": "`==` checks for equality of value (whether two objects hold equivalent contents according to `__eq__`), whereas `is` checks for identity of memory (whether both variables point to the exact same memory address according to `id(a) == id(b)`). For instance, two independently created lists `a = [1, 2, 3]` and `b = [1, 2, 3]` evaluate `a == b` as `True` (same values), but `a is b` as `False` (distinct memory allocations). Conversely, `c = a` makes `c is a` evaluate to `True`. The `is` operator should primarily be reserved for singleton checks, most notably `if val is None:`.",
        "kp": ["`==` compares value / state equality via `__eq__`", "`is` compares memory identity / object reference via `id()`", "Two distinct objects can be equal in value (`==`) but not identical (`is`)", "Always use `is None` or `is not None` for checking singleton None"],
        "cm": ["Using `if val == None` instead of idiomatic `if val is None`", "Relying on `is` for integers or strings due to accidental Python interning behavior", "Assuming identical values guarantee identical object memory locations"],
        "fu": ["Why does `x = 256; y = 256; x is y` evaluate to True, but `x = 257; y = 257; x is y` may evaluate to False?", "What is integer interning and string interning in CPython?"],
        "tags": ["python", "identity", "equality", "operators"]
    },
    {
        "q": "What is the difference between a function and a method in Python? What does `self` represent?",
        "sub": "OOP & Functions",
        "d": "Beginner",
        "ans": "A function is an independent, callable block of code defined using `def` outside of a class; it takes explicit arguments and lives in a module namespace. A method is a function defined inside a class body that is bound to an object instance (or class). When an instance method is called via `obj.method()`, Python's descriptor protocol automatically passes the object instance as the first argument, conventionally named `self`. `self` is not a language keyword, but an explicit parameter name representing the current object instance, allowing methods to read and modify the instance's attributes.",
        "kp": ["Function: standalone callable defined in a module scope", "Method: callable bound to a class or instance via descriptor protocol", "`self`: explicit reference to the current instance object passed as first parameter", "Self allows instance-specific attribute access and method dispatch"],
        "cm": ["Forgetting `self` in instance method definitions, causing TypeError when called", "Thinking `self` is a reserved language keyword like `this` in Java/C++", "Confusing instance methods, `@classmethod` (`cls`), and `@staticmethod`"],
        "fu": ["What is the difference between `@classmethod` and `@staticmethod`?", "How does Python's descriptor protocol transform a function into a bound method?"],
        "tags": ["python", "oop", "methods", "functions", "self"]
    },
    {
        "q": "What are lambda functions in Python? What are their limitations and idiomatic use cases?",
        "sub": "Lambda Functions",
        "d": "Beginner",
        "ans": "Lambda functions in Python are small, anonymous, single-expression functions created using the syntax `lambda arguments: expression`. They implicitly return the value of their single expression without an explicit `return` keyword. Idiomatic use cases include short, throwaway callback functions, such as sorting keys: `sorted(users, key=lambda u: u['age'])` or functional transformations with `map()` and `filter()`. Limitations: they can only contain a single expression (no statements, loops, assignments, or docstrings allowed). If a lambda requires assignment to a variable or multi-line logic, defining a standard named function with `def` is preferred for readability and better traceback debugging.",
        "kp": ["Syntax: `lambda args: expression` with implicit return", "Anonymous and defined inline without a name identifier", "Strictly limited to a single expression (no statements or loops)", "Idiomatic for sorting keys and simple functional arguments"],
        "cm": ["Assigning lambdas to variable names (`f = lambda x: x*2`) instead of writing a standard def", "Cramming complex ternary logic into lambdas, making code unreadable", "Using lambdas when standard built-in functions (like `str.lower` or `operator.itemgetter`) suffice"],
        "fu": ["How does `operator.itemgetter('key')` provide a faster alternative to `lambda d: d['key']`?", "Why do tracebacks with lambda functions make debugging harder in production?"],
        "tags": ["python", "lambda", "functional-programming", "sorting"]
    },
    {
        "q": "How do you achieve method overriding and multiple inheritance in Python? What is MRO?",
        "sub": "Inheritance & MRO",
        "d": "Intermediate",
        "ans": "Method overriding occurs when a subclass defines a method with the same signature as its superclass, replacing the parent implementation. The subclass can extend the parent method by calling `super().method_name(*args)`. Multiple inheritance allows a class to inherit from multiple parents: `class Sub(ParentA, ParentB):`. To resolve which parent method executes when names collide (the 'Diamond Problem'), Python uses Method Resolution Order (MRO) computed via the C3 Linearization algorithm. MRO enforces monotonicity and respects subclass-before-parent ordering. You can inspect a class's MRO using `Class.mro()` or `Class.__mro__`.",
        "kp": ["Method overriding replaces parent method; `super()` calls parent implementation", "Multiple inheritance allows classes to inherit from multiple base classes", "Diamond problem resolved deterministically using C3 Linearization algorithm", "MRO inspectable via `Class.mro()`"],
        "cm": ["Hardcoding parent class names `Parent.__init__(self)` instead of using cooperative `super()`", "Creating contradictory inheritance hierarchies that cause MRO TypeError", "Deep multi-inheritance hierarchies that introduce fragile base class problems"],
        "fu": ["What is cooperative multiple inheritance and why does `super()` depend on it?", "What algorithm does Python use to compute MRO?"],
        "tags": ["python", "inheritance", "mro", "oop", "c3-linearization"]
    },
    {
        "q": "Explain Python's duck typing philosophy and how `collections.abc` / Protocols formalize interfaces.",
        "sub": "Duck Typing & Protocols",
        "d": "Intermediate",
        "ans": "Duck typing is Python's dynamic typing philosophy: an object's suitability is determined by the presence of specific methods and properties, rather than its explicit class inheritance hierarchy ('if it walks like a duck and quacks like a duck, it is a duck'). For example, any object implementing `__len__` and `__getitem__` behaves as a sequence. To formalize interfaces without rigid inheritance, Python provides `collections.abc` (Abstract Base Classes) for runtime checks (`isinstance(x, Iterable)`) and `typing.Protocol` (PEP 544) for static duck typing, enabling mypy and IDEs to verify structural subtyping without explicit subclassing.",
        "kp": ["Duck typing evaluates capabilities/methods rather than nominal class type", "Promotes flexible, decoupled APIs that accept any compatible object", "`collections.abc` provides abstract base classes for standard container protocols", "`typing.Protocol` enables static structural subtyping (compile-time duck typing)"],
        "cm": ["Strictly checking `type(x) == list` instead of accepting general iterables", "Over-engineering complex class hierarchies when simple duck typing suffices", "Ignoring runtime AttributeError when expected duck-typed methods are absent"],
        "fu": ["What is the difference between nominal subtyping and structural subtyping?", "How does `abc.ABCMeta` register virtual subclasses without inheritance?"],
        "tags": ["python", "duck-typing", "interfaces", "typing", "protocols"]
    },
    {
        "q": "How do you profile Python code to identify execution bottlenecks, and how do you optimize them?",
        "sub": "Profiling & Optimization",
        "d": "Intermediate",
        "ans": "Profiling identifies where a program spends CPU time or memory. Standard profiling tools include `cProfile` (built-in deterministic C extension), `timeit` for micro-benchmarking snippets, and `memory_profiler` for tracking RAM usage per line. Running `python -m cProfile -s tottime script.py` pinpoints functions consuming the highest cumulative time. Optimization techniques follow an order of impact: 1) Algorithm and data structure improvements (e.g., O(n) to O(1) via set/dict), 2) Built-in C functions (map, list comprehensions, itertools), 3) Caching via `@functools.lru_cache`, and 4) JIT compilers (PyPy) or vectorization (NumPy) for intensive numeric code.",
        "kp": ["Use `cProfile` to measure function call counts and cumulative execution time", "Use `timeit` for accurate micro-benchmarks", "Prioritize algorithmic complexity improvements over micro-optimizations", "Leverage built-in C-optimized functions, sets, and `@lru_cache`"],
        "cm": ["Guessing bottlenecks without empirical profiling measurements", "Optimizing code that accounts for less than 1% of total runtime", "Sacrificing readability for negligible micro-optimizations"],
        "fu": ["What is the difference between `tottime` and `cumtime` in cProfile output?", "How does `@functools.lru_cache` optimize recursive functions like Fibonacci?"],
        "tags": ["python", "profiling", "cprofile", "optimization", "performance"]
    }
]

PART2 = [
    {
        "q": "How do you reverse a string in Python using slicing? What are the time and space complexities?",
        "sub": "String Algorithms",
        "d": "Beginner",
        "ans": "The most pythonic and efficient way to reverse a string `s` is using extended slice notation with a negative step: `reversed_s = s[::-1]`. The slice syntax takes `[start:stop:step]`; omitting start and stop while setting step to `-1` traverses the entire string from right to left. The time complexity is O(n), where n is the length of the string, as every character is copied. The space complexity is O(n) because strings are immutable in Python, requiring a new string object to be allocated in memory. Alternative approaches include `''.join(reversed(s))` which also runs in O(n) time and O(n) auxiliary space.",
        "kp": ["Pythonic syntax: `s[::-1]` uses extended slice with step=-1", "Time complexity: O(n) to copy all characters", "Space complexity: O(n) due to string immutability in Python", "Alternative: `''.join(reversed(s))` using reverse iterator"],
        "cm": ["Assuming strings can be reversed in place like arrays", "Writing manual for-loops with string concatenation (`res += char`), which is O(n^2) due to repeated allocations", "Off-by-one errors in manual index loops"],
        "fu": ["Why is string concatenation inside a loop `res += char` quadratic O(n^2) in time?", "How would you check if a string is a palindrome using this slicing technique?"],
        "tags": ["python", "strings", "slicing", "time-complexity"]
    },
    {
        "q": "Write a pythonic function to count the number of vowels in a given string, ignoring case.",
        "sub": "String Manipulation",
        "d": "Beginner",
        "ans": "A clean, pythonic solution uses a generator expression passed to the built-in `sum()` function, checking against a set of vowels for O(1) membership lookups:\n\n```python\ndef count_vowels(text: str) -> int:\n    vowels = set('aeiouAEIOU')\n    return sum(1 for char in text if char in vowels)\n```\n\nThis approach runs in O(n) time, where n is string length, and O(1) auxiliary space because a set of 10 characters has constant size and the generator streams characters without creating intermediate lists. Alternatively, `collections.Counter` can tally character frequencies across the entire string.",
        "kp": ["Convert vowels to a set (`set('aeiouAEIOU')`) for O(1) lookups", "Use generator expression with `sum()` for O(1) space efficiency", "Time complexity O(n) linear scan", "Case handling via set containing both cases or calling `.lower()`"],
        "cm": ["Checking vowels against a list in a loop (`if char in ['a', 'e', ...]`), which has higher overhead than a set", "Creating a full list comprehension in memory instead of a generator expression", "Forgetting uppercase vowels or forgetting `.lower()`"],
        "fu": ["How would you modify the function to return a dictionary of individual vowel counts?", "What is the computational benefit of using `set('aeiou')` over `'aeiou'` for membership checks?"],
        "tags": ["python", "strings", "vowels", "generator-expression"]
    },
    {
        "q": "How do you determine if two strings are anagrams of each other in Python?",
        "sub": "String Algorithms",
        "d": "Beginner",
        "ans": "Two strings are anagrams if they contain the exact same characters with identical frequencies, possibly in a different order. The most optimal approach uses `collections.Counter` to compare character frequency distributions in O(n) time and O(k) space (where k is alphabet size):\n\n```python\nfrom collections import Counter\n\ndef is_anagram(s1: str, s2: str) -> bool:\n    return Counter(s1.replace(' ', '').lower()) == Counter(s2.replace(' ', '').lower())\n```\n\nAn alternative approach is sorting both strings: `sorted(s1) == sorted(s2)`, which takes O(n log n) time and O(n) space. The Counter approach is preferred for large strings due to its linear time complexity.",
        "kp": ["Optimal approach: `Counter(s1) == Counter(s2)` runs in O(n) time", "Sorting approach: `sorted(s1) == sorted(s2)` runs in O(n log n) time", "Sanitize inputs: strip whitespace and normalize casing if required", "Early exit: return False immediately if sanitized lengths differ"],
        "cm": ["Using nested loops with `s1.count(char)`, resulting in O(n^2) quadratic time", "Forgetting to normalize case or handle spaces", "Sorting very large texts when a linear frequency hash map is faster"],
        "fu": ["What is the Unicode complexity if strings contain accents or combined glyphs?", "How would you implement anagram grouping across a list of 100,000 words?"],
        "tags": ["python", "anagrams", "strings", "collections-counter", "algorithms"]
    },
    {
        "q": "How do you swap two variables in Python without using a temporary variable? How does it work under the hood?",
        "sub": "Python Idioms",
        "d": "Beginner",
        "ans": "In Python, two variables are swapped using tuple packing and unpacking syntax: `a, b = b, a`. This executes in a single line without temporary variable identifiers. Under the hood, Python's bytecode compiler first packs the right-hand expressions into a tuple on the interpreter stack (`b, a`), and then unpacks the tuple elements into the left-hand targets (`a` and `b`) from left to right. This eliminates temporary variables in Python code, avoids arithmetic overflow pitfalls found in XOR/addition tricks, and is optimized at the CPython bytecode level with `ROT_TWO` (in older versions) or stack operations.",
        "kp": ["Syntax: `a, b = b, a` uses tuple packing and unpacking", "Right-hand side evaluated completely into a tuple before assignment occurs", "Safe against arithmetic overflow and type mismatches", "Can be extended to multiple variables: `a, b, c = c, a, b`"],
        "cm": ["Using manual XOR swap tricks (`a ^= b`) in Python, which hurts readability and fails on non-integers", "Attempting sequential assignment `a = b; b = a`, which overwrites `a`'s value", "Not understanding that right-hand side is evaluated first"],
        "fu": ["Can you swap list elements in place using `arr[i], arr[j] = arr[j], arr[i]`?", "What bytecode instructions are generated for `a, b = b, a`?"],
        "tags": ["python", "tuple-unpacking", "idiomatic-python", "variables"]
    },
    {
        "q": "How do you find the second largest element in a list in Python in O(n) time without sorting?",
        "sub": "List Algorithms",
        "d": "Intermediate",
        "ans": "Sorting the list takes O(n log n) time. To achieve optimal O(n) linear time and O(1) space, iterate through the list maintaining two variables, `largest` and `second_largest`, initialized to `-float('inf')`:\n\n```python\ndef find_second_largest(nums: list[int]) -> int | None:\n    if len(nums) < 2:\n        return None\n    largest = second = -float('inf')\n    for n in nums:\n        if n > largest:\n            second = largest\n            largest = n\n        elif largest > n > second:\n            second = n\n    return second if second != -float('inf') else None\n```\n\nThis single-pass algorithm handles duplicates properly (e.g., `[10, 10, 9]` correctly identifies 9) and handles negative numbers.",
        "kp": ["Single-pass O(n) time complexity and O(1) constant auxiliary space", "Initialize tracking variables to negative infinity (`-float('inf')`)", "Correctly handle duplicates where multiple identical max elements exist", "Validate edge cases: lists with fewer than two unique elements"],
        "cm": ["Sorting the list `sorted(nums)[-2]`, which fails on duplicates like `[10, 10, 5]` and takes O(n log n)", "Initializing tracking variables to 0, which fails on lists of negative integers", "Not handling empty lists or single-element inputs"],
        "fu": ["How would you extend this pattern to find the K-th largest element using `heapq`?", "What is the time complexity of `heapq.nlargest(2, nums)`?"],
        "tags": ["python", "algorithms", "arrays", "time-complexity"]
    },
    {
        "q": "How do you remove duplicates from a list in Python while preserving the original element order?",
        "sub": "List Manipulation",
        "d": "Beginner",
        "ans": "Using `list(set(items))` removes duplicates in O(n) time, but destroys the original order because sets are unordered. Since Python 3.7, dictionaries maintain insertion order, allowing an idiomatic one-liner that preserves order in O(n) time and O(n) space:\n\n```python\ndef remove_duplicates_ordered(items: list) -> list:\n    return list(dict.fromkeys(items))\n```\n\n`dict.fromkeys()` inserts keys sequentially while discarding duplicates, and converting keys back to a list preserves original order. For unhashable elements (like nested dicts or lists), a manual loop using a custom seen tracker is necessary.",
        "kp": ["`list(dict.fromkeys(items))` removes duplicates and preserves insertion order", "O(n) linear time complexity and O(n) auxiliary space", "`list(set(items))` removes duplicates but discards insertion order", "Requires elements to be hashable"],
        "cm": ["Using `list(set(items))` and assuming it will preserve order", "Using a nested loop `if item not in seen_list: seen_list.append(item)`, which is O(n^2) quadratic time", "Applying `dict.fromkeys()` on lists containing unhashable objects (like dicts)"],
        "fu": ["How do you preserve order when elements are unhashable (e.g., list of dicts)?", "Why is `dict.fromkeys()` faster than a Python for-loop appending to a set and list?"],
        "tags": ["python", "lists", "duplicates", "dictionaries", "performance"]
    },
    {
        "q": "How do you find the missing number in an array containing numbers from 1 to N in O(n) time and O(1) space?",
        "sub": "Mathematical Algorithms",
        "d": "Beginner",
        "ans": "Given an array of length N-1 containing distinct integers in the range [1, N], the missing number can be found using the Gauss summation formula `expected_sum = N * (N + 1) // 2`. Subtracting the actual sum of array elements from the expected sum yields the missing integer:\n\n```python\ndef find_missing_number(nums: list[int]) -> int:\n    n = len(nums) + 1\n    expected_sum = n * (n + 1) // 2\n    return expected_sum - sum(nums)\n```\n\nThis runs in O(n) time and O(1) auxiliary space. An alternative bitwise approach uses XOR: XORing all indices from 1 to N with all array elements cancels out duplicates, leaving the missing number, which avoids arithmetic overflow in languages without arbitrary-precision integers.",
        "kp": ["Math formula: `N * (N + 1) // 2` gives expected sum in O(1)", "Time complexity: O(n) for single pass `sum(nums)`", "Auxiliary space: O(1) constant memory", "Alternative bitwise XOR approach cancels pairs"],
        "cm": ["Sorting the array first, which degrades time to O(n log n)", "Using a hash set lookup, which uses O(n) unnecessary extra memory", "Off-by-one errors in determining N (`len(nums) + 1`)"],
        "fu": ["How does the XOR bitwise approach prevent integer overflow in C/Java?", "What if two numbers are missing instead of one? How does the approach change?"],
        "tags": ["python", "algorithms", "math", "bitwise", "arrays"]
    },
    {
        "q": "Explain binary search in Python. What are the preconditions, time complexity, and edge cases?",
        "sub": "Search Algorithms",
        "d": "Intermediate",
        "ans": "Binary search is an efficient search algorithm on a sorted array that works by repeatedly dividing the search interval in half. Precondition: the collection must be sorted and support O(1) random indexing. Algorithm: maintain two pointers, `low` and `high`. Compute `mid = (low + high) // 2`. If `target == arr[mid]`, return mid. If `target < arr[mid]`, search left (`high = mid - 1`); if `target > arr[mid]`, search right (`low = mid + 1`). Continue while `low <= high`. Time complexity is O(log n) because the search space halves at every step; space complexity is O(1) iterative. Python provides the built-in `bisect` module for binary search insertions.",
        "kp": ["Precondition: sequence must be sorted with O(1) random access", "Time complexity: O(log n); Space complexity: O(1) iterative", "Pointer updates: `high = mid - 1` and `low = mid + 1` to prevent infinite loops", "Python standard library module: `bisect` (`bisect_left`, `bisect_right`)"],
        "cm": ["Applying binary search on an unsorted collection or linked list", "Calculating mid as `low + high // 2` due to missing parentheses", "Using `low < high` instead of `low <= high`, missing target when it sits at array edges"],
        "fu": ["How does `bisect.bisect_left` differ from `bisect.bisect_right` when elements are duplicated?", "Why does integer overflow in `(low + high) // 2` occur in C/Java but not in Python?"],
        "tags": ["python", "binary-search", "algorithms", "time-complexity", "bisect"]
    },
    {
        "q": "What is the difference between `sort()` and `sorted()` in Python? What algorithm does Python use?",
        "sub": "Sorting",
        "d": "Beginner",
        "ans": "`list.sort()` is an in-place method that modifies the original list and returns `None`. `sorted(iterable)` is a built-in function that accepts any iterable and returns a new sorted list, leaving the original sequence unchanged. Both take optional `key` and `reverse` arguments. Python uses Timsort, a hybrid, stable sorting algorithm derived from Merge Sort and Insertion Sort designed by Tim Peters. Timsort identifies natural contiguous ordered segments ('runs') in real-world data and merges them efficiently. Its worst-case and average-case time complexity is O(n log n), and best-case on already sorted data is O(n). Being a stable sort, it preserves the relative order of elements with equal keys.",
        "kp": ["`list.sort()`: in-place modification, returns None, works only on lists", "`sorted(iterable)`: returns a new sorted list, works on any iterable", "Algorithm: Timsort (hybrid of Merge Sort and Insertion Sort)", "Time complexity: O(n log n) average/worst, O(n) best case; Stable sort"],
        "cm": ["Assigning the result of `list.sort()` to a variable (`my_list = my_list.sort()`), which sets it to None", "Assuming sorting is unstable and changes relative order of equivalent items", "Calling `sort()` on non-list iterables like strings or tuples"],
        "fu": ["What does it mean that a sorting algorithm is 'stable'?", "How does Timsort achieve O(n) time complexity on nearly sorted arrays?"],
        "tags": ["python", "sorting", "timsort", "algorithms", "lists"]
    },
    {
        "q": "How do you count the frequency of all elements in a list using standard library tools?",
        "sub": "Data Counting",
        "d": "Beginner",
        "ans": "The most pythonic, optimized way is using `collections.Counter`:\n\n```python\nfrom collections import Counter\ncounts = Counter(my_list)\n```\n\n`Counter` is a dictionary subclass that tallies element occurrences in O(n) time and O(u) space (where u is unique elements). It provides convenient helper methods like `counts.most_common(k)` to retrieve the top-k most frequent elements. Without Counter, the idiomatic dictionary approach uses `dict.get()`: `for item in my_list: counts[item] = counts.get(item, 0) + 1` or `defaultdict(int)`. Avoid calling `my_list.count(x)` inside a loop, as that results in O(n^2) quadratic time.",
        "kp": ["Use `collections.Counter(my_list)` for idiomatic O(n) counting", "Provides `.most_common(k)` for top-k frequency queries", "Manual idiom: `counts[x] = counts.get(x, 0) + 1` or `defaultdict(int)`", "Avoid `my_list.count()` inside loops to prevent O(n^2) bottleneck"],
        "cm": ["Calling `my_list.count(item)` in a loop or comprehension (O(n^2) performance disaster)", "Using manual try-except KeyError blocks when `get()` or `defaultdict` is cleaner", "Not knowing Counter handles arithmetic operations like addition and subtraction"],
        "fu": ["What is the time complexity of `Counter.most_common(k)`?", "Can `Counter` be used to find multiset intersections between two collections?"],
        "tags": ["python", "collections", "counter", "frequency", "algorithms"]
    },
    {
        "q": "How do you implement the Two Sum problem in Python in O(n) time using a dictionary?",
        "sub": "Dictionary Algorithms",
        "d": "Intermediate",
        "ans": "The Two Sum problem asks for indices of two numbers in an array that add up to a target sum. A brute-force nested loop takes O(n^2) time. We achieve optimal O(n) time and O(n) space using a hash map to track complements in a single pass:\n\n```python\ndef two_sum(nums: list[int], target: int) -> list[int]:\n    seen = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in seen:\n            return [seen[complement], i]\n        seen[num] = i\n    return []\n```\n\nFor every number, we check if `target - num` already exists in `seen`. If found, we return the stored index and current index. If not, we record `seen[num] = i`. Hash lookups are O(1) average, making total time linear.",
        "kp": ["Single-pass hash table achieves O(n) time complexity", "Look up `target - current_number` in dictionary in O(1) average time", "Store number as key and array index as value", "Space complexity is O(n) for the hash map"],
        "cm": ["Brute-force nested loops `for i ... for j ...` taking O(n^2) time", "Storing elements in dictionary before checking, causing identical elements to overwrite each other", "Returning values instead of indices when indices are requested"],
        "fu": ["How does the solution change if the input array is already sorted (Two Pointers approach)?", "How do you handle the 3Sum problem in O(n^2) time?"],
        "tags": ["python", "two-sum", "hash-map", "algorithms", "arrays"]
    },
    {
        "q": "How do you move all zeros to the end of an array in place while maintaining relative order of non-zero elements?",
        "sub": "Array Algorithms",
        "d": "Intermediate",
        "ans": "To move zeros to the end in place in O(n) time and O(1) auxiliary space, use a two-pointer approach:\n\n```python\ndef move_zeroes(nums: list[int]) -> None:\n    insert_pos = 0\n    for i in range(len(nums)):\n        if nums[i] != 0:\n            nums[insert_pos], nums[i] = nums[i], nums[insert_pos]\n            insert_pos += 1\n```\n\nAs we iterate through the array, whenever we encounter a non-zero element, we swap it with the element at `insert_pos` and increment `insert_pos`. All non-zero elements stay in their original relative order, and zeros naturally migrate toward the end. No new list is allocated.",
        "kp": ["Two-pointer in-place swap strategy", "Time complexity: O(n) single pass", "Space complexity: O(1) constant in-place memory", "Preserves relative order of non-zero elements"],
        "cm": ["Using `nums.remove(0)` and `nums.append(0)` in a loop, which is O(n^2) due to list shifting", "Creating a new filtered list when the problem mandates in-place modification", "Losing original relative ordering of non-zero elements"],
        "fu": ["Why is `nums.remove(0)` inside a loop computationally expensive?", "What is the minimum number of write operations needed to move zeros?"],
        "tags": ["python", "two-pointers", "arrays", "in-place", "algorithms"]
    },
    {
        "q": "How do you check if a string contains balanced parentheses `()`, brackets `[]`, and braces `{}` in Python?",
        "sub": "Stack Algorithms",
        "d": "Intermediate",
        "ans": "Use a stack (implemented with a Python list). Scan the string character by character. When encountering an opening bracket `(`, `[`, `{`, push it onto the stack. When encountering a closing bracket `)`, `]`, `}`, check if the stack is non-empty and whether the popped top matches the opening counterpart via a mapping dictionary. If it does not match or the stack was empty, return `False`. After processing, the string is balanced if and only if the stack is completely empty.\n\n```python\ndef is_balanced(s: str) -> bool:\n    mapping = {')': '(', ']': '[', '}': '{'}\n    stack = []\n    for char in s:\n        if char in mapping.values():\n            stack.append(char)\n        elif char in mapping:\n            if not stack or stack.pop() != mapping[char]:\n                return False\n    return len(stack) == 0\n```\nTime is O(n) and space is O(n).",
        "kp": ["Stack data structure handles Last-In-First-Out (LIFO) matching", "Map closing brackets to opening brackets in a dictionary", "Push opening symbols; pop and verify closing symbols", "Final check: stack must be empty (`len(stack) == 0`)"],
        "cm": ["Using simple counters instead of a stack (fails on mixed interleaving like `[(])`)", "Forgetting to check if stack is empty before popping (raises IndexError)", "Forgetting the final `len(stack) == 0` check, missing unclosed openers"],
        "fu": ["Why can a simple integer counter balance `()` but fail on multiple bracket types?", "How do compilers use stack-based parsing for syntax validation?"],
        "tags": ["python", "stack", "algorithms", "parentheses", "data-structures"]
    },
    {
        "q": "Explain recursion in Python. What is the recursion limit and how do you handle base cases?",
        "sub": "Recursion",
        "d": "Beginner",
        "ans": "Recursion is a programming technique where a function calls itself to solve smaller subproblems of the same problem. Every recursive function requires two core components: 1) One or more base cases that terminate recursion without making further self-calls, and 2) A recursive step that reduces the problem size toward the base case. Without a proper base case, infinite recursion occurs, exhausting the call stack and raising `RecursionError: maximum recursion depth exceeded`. In Python, CPython sets a default recursion limit (typically 1000 stack frames) to prevent C stack overflow, inspectable via `sys.getrecursionlimit()`.",
        "kp": ["Base case: termination condition that halts recursion", "Recursive step: reduces problem size toward base case", "RecursionError raised when stack depth exceeds limit (default ~1000)", "Inspect and set via `sys.getrecursionlimit()` and `sys.setrecursionlimit()`"],
        "cm": ["Missing base case, causing infinite loop and stack overflow", "Not moving arguments closer to base case in recursive calls", "Using naive recursion for overlapping subproblems (e.g., Fibonacci) without memoization"],
        "fu": ["Does Python support Tail Call Optimization (TCO)? Why or why not?", "How does `@functools.cache` convert exponential recursive algorithms into linear time?"],
        "tags": ["python", "recursion", "call-stack", "algorithms"]
    },
    {
        "q": "Write an efficient function to compute the N-th Fibonacci number. Compare naive recursion, memoization, and iteration.",
        "sub": "Dynamic Programming",
        "d": "Intermediate",
        "ans": "1) Naive recursion `fib(n-1) + fib(n-2)` has exponential O(2^n) time complexity because it recalculates overlapping subtrees repeatedly. 2) Memoization via `@functools.cache` caches results, reducing time to O(n) with O(n) stack memory. 3) Iteration is the most optimal, running in O(n) time and O(1) space by tracking only the last two values:\n\n```python\ndef fibonacci(n: int) -> int:\n    if n < 0:\n        raise ValueError(\"n must be non-negative\")\n    if n <= 1:\n        return n\n    a, b = 0, 1\n    for _ in range(2, n + 1):\n        a, b = b, a + b\n    return b\n```\nIterative approach avoids both stack overflow and memory allocation overhead.",
        "kp": ["Naive recursion: O(2^n) exponential time due to duplicate subproblems", "Memoization: O(n) time and O(n) memory via cache", "Iterative: O(n) time and O(1) constant memory", "Validate input boundaries for negative numbers"],
        "cm": ["Writing naive recursion for N > 35, causing the program to freeze", "Allocating an entire list of length N when only last two numbers are needed", "Off-by-one errors on N=0 and N=1"],
        "fu": ["What is the closed-form Binet's formula for Fibonacci and what are its floating-point limits?", "Can Fibonacci be computed in O(log n) time using matrix exponentiation?"],
        "tags": ["python", "fibonacci", "dynamic-programming", "memoization", "algorithms"]
    },
    {
        "q": "How do you check if a number is prime in Python? What is the trial division optimization up to sqrt(n)?",
        "sub": "Mathematical Algorithms",
        "d": "Beginner",
        "ans": "A prime number is an integer greater than 1 with no positive divisors other than 1 and itself. A naive check tests divisors from 2 to n-1 in O(n) time. We optimize to O(sqrt(n)) because if n has a factor larger than sqrt(n), its corresponding pair factor must be smaller than sqrt(n):\n\n```python\ndef is_prime(n: int) -> bool:\n    if n <= 1:\n        return False\n    if n <= 3:\n        return True\n    if n % 2 == 0 or n % 3 == 0:\n        return False\n    i = 5\n    while i * i <= n:\n        if n % i == 0 or n % (i + 2) == 0:\n            return False\n        i += 6\n    return True\n```\nChecking up to sqrt(n) with step 6 (testing 6k ± 1) eliminates multiples of 2 and 3, reducing check operations significantly.",
        "kp": ["Prime definition: integer > 1 divisible only by 1 and self", "Trial division up to sqrt(n) runs in O(sqrt(n)) time", "6k ± 1 optimization skips multiples of 2 and 3", "Early exits: numbers <= 1 are not prime; 2 and 3 are prime"],
        "cm": ["Checking up to n instead of sqrt(n), causing unnecessary O(n) iterations", "Considering negative numbers, 0, or 1 as prime", "Using `range(2, int(math.sqrt(n)))` without adding 1, missing exact squares"],
        "fu": ["How does the Sieve of Eratosthenes find all primes up to N in O(N log log N) time?", "What is the Fermat or Miller-Rabin primality test used in cryptography?"],
        "tags": ["python", "primes", "math", "algorithms", "number-theory"]
    },
    {
        "q": "How do you calculate the factorial of a number in Python? Discuss iterative, recursive, and math.factorial approaches.",
        "sub": "Mathematical Algorithms",
        "d": "Beginner",
        "ans": "Factorial of n (n!) is the product of all positive integers <= n; 0! is defined as 1. 1) Recursive: `n * fact(n-1)` with base case `n <= 1: return 1`, running in O(n) time and O(n) stack frames. 2) Iterative: a simple loop accumulating `res *= i` in O(n) time and O(1) space. 3) Standard library: `math.factorial(n)` is implemented in optimized C in CPython, making it significantly faster and safe against recursion limits. Python's arbitrary-precision integers automatically prevent integer overflow, allowing calculation of very large factorials (e.g., 1000!).",
        "kp": ["0! is defined as 1; negative numbers have undefined factorial", "Iterative: O(n) time, O(1) space", "Recursive: O(n) time, O(n) call stack", "Standard library: `math.factorial(n)` is C-optimized and preferred in production"],
        "cm": ["Forgetting base case 0! = 1 in recursive implementations", "Not validating negative inputs (raises ValueError in math.factorial)", "Assuming integer overflow occurs in Python as it does in C/Java"],
        "fu": ["How does Python handle arbitrarily large integers without integer overflow?", "What is Stirling's approximation for estimating large factorials?"],
        "tags": ["python", "factorial", "math", "recursion", "algorithms"]
    },
    {
        "q": "How do you implement Kadane's algorithm to find the maximum subarray sum in Python?",
        "sub": "Array Algorithms",
        "d": "Intermediate",
        "ans": "Kadane's algorithm finds the contiguous subarray with the largest sum in O(n) linear time and O(1) auxiliary space, improving over O(n^2) brute force:\n\n```python\ndef max_sub_array(nums: list[int]) -> int:\n    max_current = max_global = nums[0]\n    for x in nums[1:]:\n        max_current = max(x, max_current + x)\n        if max_current > max_global:\n            max_global = max_current\n    return max_global\n```\n\nAt each index, we decide whether to add the current number to the running subarray (`max_current + x`) or start a fresh subarray at `x` (`max(x, max_current + x)`). `max_global` tracks the highest sum seen so far. Initializing with `nums[0]` correctly handles arrays containing all negative numbers.",
        "kp": ["Kadane's algorithm achieves O(n) time and O(1) space", "Core recurrence: `max_current = max(x, max_current + x)`", "Initializes with `nums[0]` to correctly handle all-negative arrays", "Returns maximum contiguous sum"],
        "cm": ["Initializing max_global to 0, which fails on arrays of all negative numbers (e.g., `[-5, -2, -8]`)", "Using O(n^2) nested loops checking every subarray pair", "Confusing contiguous subarray with non-contiguous subsequence"],
        "fu": ["How would you modify Kadane's algorithm to return the starting and ending indices of the subarray?", "Can Kadane's algorithm be applied to circular arrays?"],
        "tags": ["python", "kadanes-algorithm", "dynamic-programming", "arrays", "algorithms"]
    },
    {
        "q": "What is the difference between `@classmethod`, `@staticmethod`, and instance methods in Python?",
        "sub": "OOP Methods",
        "d": "Intermediate",
        "ans": "1) Instance method: default method receiving `self` as the first argument; has access to instance attributes and class state via `self.__class__`. 2) Class method (`@classmethod`): receives the class `cls` as the first argument instead of an instance; used for alternative constructors (e.g., `from_dict`, `from_json`) and modifying class-level state across all instances. 3) Static method (`@staticmethod`): receives neither `self` nor `cls`; behaves like a plain function scoped inside the class namespace for logical grouping, with no access to instance or class state.",
        "kp": ["Instance method: receives `self`, accesses and mutates instance state", "Class method: receives `cls`, used for alternative constructors and class state", "Static method: receives neither `self` nor `cls`, utility function bound to namespace", "Defined via `@classmethod` and `@staticmethod` decorators"],
        "cm": ["Using `@staticmethod` when the function needs to inspect or create instances of `cls`", "Forgetting `cls` parameter in class methods or `self` in instance methods", "Calling instance methods on classes without an instance object"],
        "fu": ["How do alternative constructors like `datetime.fromtimestamp()` use `@classmethod`?", "When is it better to put a utility function in a module rather than using `@staticmethod`?"],
        "tags": ["python", "oop", "decorators", "classmethod", "staticmethod"]
    },
    {
        "q": "How does Python's `zip()` function work, and what is `itertools.zip_longest()`?",
        "sub": "Built-in Functions",
        "d": "Beginner",
        "ans": "`zip(*iterables)` aggregates elements from each of the provided iterables into tuples and returns an iterator. By default, `zip()` stops when the shortest input iterable is exhausted (truncating longer inputs). In Python 3.10+, `strict=True` can be passed to raise a `ValueError` if the iterables are not of equal length. When you want to continue until the longest iterable is exhausted, `itertools.zip_longest(*iterables, fillvalue=None)` pads shorter iterables with the specified `fillvalue`. Unpacking with zip `zip(*zipped)` reverses the operation.",
        "kp": ["`zip()` pairs elements from multiple iterables into tuples lazily", "Stops at the shortest iterable by default", "Python 3.10+ `zip(..., strict=True)` enforces equal lengths", "`itertools.zip_longest()` continues until longest iterable with `fillvalue` padding"],
        "cm": ["Silent data loss when zipping unequal-length lists without knowing it truncates", "Loading zipped results into memory as a list when simple iteration suffices", "Attempting to index a zip object without converting to list or tuple"],
        "fu": ["How do you transpose a 2D matrix in one line using `zip(*matrix)`?", "How do you create a dictionary from two separate lists of keys and values using `zip()`?"],
        "tags": ["python", "zip", "itertools", "built-in-functions", "iterables"]
    }
]

PART3 = [
    {
        "q": "What are Python's `*args` and `**kwargs` scoping rules inside inner wrapper functions?",
        "sub": "Advanced Decorators",
        "d": "Intermediate",
        "ans": "When writing inner wrapper functions for decorators, standard practice is to accept `*args, **kwargs` and pass them to the wrapped function: `return func(*args, **kwargs)`. This allows the wrapper to be completely agnostic to the wrapped function's signature, handling functions with zero, positional, keyword, or default arguments. Scoping: the inner function forms a closure over `func`, retaining access to the outer function's arguments. If variables in the enclosing scope need to be modified inside the wrapper, the `nonlocal` keyword is required.",
        "kp": ["Signature agnosticism: `*args, **kwargs` accepts any parameter combination", "Unpacking with `*` and `**` forwards arguments accurately", "Closures allow wrappers to retain reference to wrapped `func`", "`nonlocal` keyword permits modifying enclosing scope variables"],
        "cm": ["Defining wrapper with fixed arguments, breaking when decorated on functions with different signatures", "Forgetting to return the result of `func(*args, **kwargs)` from the wrapper", "Confusing `global` with `nonlocal` in nested function closures"],
        "fu": ["What is the difference between `global` and `nonlocal` variable declarations?", "How do you inspect a wrapped function's original signature using `inspect.signature()`?"],
        "tags": ["python", "decorators", "closures", "scoping", "args-kwargs"]
    },
    {
        "q": "Explain the difference between `__init__` and `__new__` in Python class instantiation.",
        "sub": "Metaprogramming & Instantiation",
        "d": "Advanced",
        "ans": "Class instantiation in Python is a two-step process: 1) `__new__(cls, *args, **kwargs)` is the actual constructor method that allocates and returns a new, uninitialized instance of the class in memory. It is a static method that takes `cls` as its first parameter. 2) `__init__(self, *args, **kwargs)` is the initializer method that receives the newly created instance as `self` and sets up instance attributes. `__new__` is overridden in specialized scenarios, such as implementing Singletons, creating custom metaclasses, or subclassing immutable built-in types (int, str, tuple) where values must be set before object creation.",
        "kp": ["`__new__`: creates and returns the new instance object in memory", "`__init__`: initializes attributes on the instance returned by `__new__`", "`__new__` takes `cls` as first argument; `__init__` takes `self`", "Override `__new__` for Singletons and subclassing immutable types"],
        "cm": ["Attempting to return a value other than None from `__init__` (raises TypeError)", "Overriding `__new__` and forgetting to return `super().__new__(cls)`", "Using `__new__` for ordinary attribute setup where `__init__` is standard"],
        "fu": ["How do you implement the Singleton pattern using `__new__`?", "What happens if `__new__` does not return an instance of `cls`?"],
        "tags": ["python", "dunder-methods", "oop", "metaprogramming", "singleton"]
    },
    {
        "q": "What are descriptors in Python, and how do `@property`, `@classmethod`, and ORMs rely on them?",
        "sub": "Descriptors",
        "d": "Advanced",
        "ans": "A descriptor is any object that defines at least one of the methods `__get__()`, `__set__()`, or `__delete__()` in the descriptor protocol. Descriptors customize attribute access, assignment, and deletion on owner classes. Python's attribute lookup checks descriptors before falling back to instance `__dict__`. Built-in features like `@property`, `@classmethod`, `@staticmethod`, and SQLAlchemy ORM model columns are all implemented as descriptors. For example, `@property` creates a descriptor that maps attribute access to getter and setter functions transparently.",
        "kp": ["Descriptor protocol: `__get__`, `__set__`, `__delete__`", "Data descriptors define `__set__`; non-data descriptors define only `__get__`", "Attribute lookup order checks data descriptors before instance `__dict__`", "Powers `@property`, method binding, and ORM column mappings"],
        "cm": ["Instantiating a descriptor on an instance instead of as a class attribute", "Confusing data descriptors with non-data descriptors", "Modifying instance dictionaries directly and bypassing descriptor validation"],
        "fu": ["What is the exact attribute lookup precedence in Python when resolving `obj.attr`?", "How does an ORM like SQLAlchemy use descriptors to track dirty column changes?"],
        "tags": ["python", "descriptors", "properties", "metaprogramming", "orm"]
    },
    {
        "q": "How do Python generators support two-way communication using `.send()`, `.throw()`, and `.close()`?",
        "sub": "Advanced Generators",
        "d": "Advanced",
        "ans": "While generators commonly produce data via `yield`, they can also consume data, acting as coroutines. 1) `.send(value)` resumes the generator and yields a value while passing `value` into the generator as the result of the `yield` expression: `received = yield output`. 2) `.throw(typ, val, tb)` raises an exception at the generator's current yield point, allowing the generator to handle or cleanup via `except`. 3) `.close()` raises `GeneratorExit` at the yield point to terminate the generator cleanly. Two-way generator communication laid the historical foundation for Python's asyncio event loop.",
        "kp": ["`yield` can be an expression that receives values: `val = yield expr`", "`.send(val)` sends data into the generator at the yield suspension point", "`.throw()` injects exceptions; `.close()` terminates via `GeneratorExit`", "Historical foundation for asyncio coroutines prior to `async/await` syntax"],
        "cm": ["Calling `.send(value)` on a freshly created generator before priming it with `next()` or `.send(None)`", "Catching `GeneratorExit` and attempting to yield further values (raises RuntimeError)", "Ignoring generator cleanup in streaming pipelines"],
        "fu": ["Why must a generator be 'primed' with `next()` or `.send(None)` before sending data?", "How did PEP 380's `yield from` syntax enable subgenerator delegation?"],
        "tags": ["python", "generators", "coroutines", "async-foundations"]
    },
    {
        "q": "Explain `asyncio`, event loops, coroutines, and the difference between synchronous and asynchronous code.",
        "sub": "Asynchronous Programming",
        "d": "Advanced",
        "ans": "Synchronous code executes sequentially; blocking operations (like network I/O or sleep) halt the entire execution thread. `asyncio` provides cooperative multitasking using an event loop on a single thread. Coroutines are declared with `async def` and paused at non-blocking I/O points with `await`. While one coroutine awaits network data, the event loop runs other ready tasks, achieving high concurrency without multi-thread context-switching overhead. Asynchronous programming is ideal for I/O-bound operations (e.g., handling 10,000 concurrent HTTP requests in FastAPI), but does not speed up CPU-bound operations.",
        "kp": ["Event loop manages and distributes execution of cooperative tasks", "`async def` defines a coroutine; `await` yields control back to event loop", "Non-blocking concurrency on a single thread eliminates thread switching overhead", "Ideal for I/O-bound workloads; does not accelerate CPU-bound tasks"],
        "cm": ["Using blocking synchronous calls like `time.sleep()` or `requests.get()` inside async functions", "Forgetting to `await` a coroutine, resulting in an unexecuted coroutine object", "Expecting asyncio to speed up heavy mathematical CPU calculations"],
        "fu": ["What happens when a synchronous blocking call is executed inside an asyncio event loop?", "How does `asyncio.to_thread()` offload blocking operations to a threadpool?"],
        "tags": ["python", "asyncio", "concurrency", "event-loop", "fastapi"]
    },
    {
        "q": "What is `__slots__` in Python classes? What are its memory benefits and trade-offs?",
        "sub": "Memory Optimization",
        "d": "Intermediate",
        "ans": "By default, Python instances store attributes in a dynamic dictionary `__dict__`, allowing arbitrary attribute addition at runtime but incurring memory overhead. Declaring `__slots__ = ('name', 'age')` tells Python to allocate a fixed-size array of descriptors for the specified attributes and suppress the creation of `__dict__` and `__weakref__`. This reduces per-instance memory consumption by 40-70%, which is significant when instantiating millions of small objects. Trade-offs: prevents dynamic addition of attributes not listed in slots, complicates multiple inheritance, and requires derived subclasses to also declare `__slots__`.",
        "kp": ["`__slots__` suppresses default per-instance `__dict__` creation", "Substantial memory savings (40-70%) for millions of small objects", "Fast attribute access via fixed array offsets", "Trade-offs: cannot add undeclared attributes dynamically; inheritance complexities"],
        "cm": ["Using `__slots__` prematurely for small numbers of objects with negligible memory impact", "Forgetting to declare `__slots__` in subclasses, which causes Python to generate `__dict__` anyway", "Attempting to assign new attributes at runtime not listed in `__slots__`"],
        "fu": ["How do dataclasses support slots in Python 3.10+ via `@dataclass(slots=True)`?", "Does `__slots__` speed up attribute access times or only reduce memory?"],
        "tags": ["python", "memory-optimization", "slots", "performance", "oop"]
    },
    {
        "q": "What is the difference between `@dataclass`, `namedtuple`, and standard classes in Python?",
        "sub": "Data Containers",
        "d": "Intermediate",
        "ans": "1) Standard class: requires boilerplate for `__init__`, `__repr__`, and `__eq__`. 2) `namedtuple` (from `collections` or `typing.NamedTuple`): lightweight, immutable tuple with named field access; memory-efficient and iterable, but cannot be mutated. 3) `@dataclass` (PEP 557): code generator decorator that automatically writes `__init__`, `__repr__`, `__eq__`, and ordering methods based on type annotations. Dataclasses support mutability (or immutability via `frozen=True`), default values, inheritance, and `__post_init__` hooks. Use `NamedTuple` for simple immutable tuples; use `@dataclass` for rich, maintainable structured domain models.",
        "kp": ["`@dataclass` auto-generates `__init__`, `__repr__`, `__eq__` from type hints", "`NamedTuple` provides lightweight immutable tuple with named access", "Dataclasses support mutable fields, `frozen=True`, and `__post_init__` hooks", "Standard classes preferred when complex custom instantiation is needed"],
        "cm": ["Writing 30 lines of boilerplate `__init__` and `__repr__` manually instead of using `@dataclass`", "Attempting to mutate fields on an immutable `NamedTuple`", "Using mutable defaults like `list` directly in dataclass fields without `field(default_factory=list)`"],
        "fu": ["Why must mutable defaults in dataclasses use `field(default_factory=list)`?", "How does Pydantic build upon the dataclass pattern for runtime validation?"],
        "tags": ["python", "dataclass", "namedtuple", "oop", "type-hints"]
    },
    {
        "q": "How do type hints and the `typing` module work in Python? Does Python enforce types at runtime?",
        "sub": "Type Annotations",
        "d": "Beginner",
        "ans": "Type hints (PEP 484) allow developers to annotate variables, function parameters, and return types (e.g., `def greet(name: str) -> str:`). Python is dynamically typed and does NOT enforce type hints at runtime; passing an integer to a function expecting `str` will not raise a TypeError natively. Type hints are used by static analysis tools (mypy, pyright), IDEs for autocompletion, and libraries like Pydantic and FastAPI that perform runtime validation based on annotations. The `typing` module provides advanced constructs like `Union`, `Optional`, `Any`, `Callable`, `Generic`, and `Literal`.",
        "kp": ["Type hints are annotations; Python does NOT enforce them at runtime natively", "Used by static type checkers (mypy) and IDEs to catch bugs before execution", "Pydantic and FastAPI inspect type annotations for runtime parsing and validation", "Syntax: `var: type = val` and `def func(param: type) -> return_type:`"],
        "cm": ["Assuming Python raises TypeErrors automatically when wrong types are passed", "Using outdated `typing.List[int]` in Python 3.9+ instead of built-in `list[int]`", "Ignoring static type checker warnings during development"],
        "fu": ["What is the difference between `Union[int, None]` and `int | None` in Python 3.10+?", "How does `typing.cast()` instruct static type checkers without changing runtime objects?"],
        "tags": ["python", "typing", "type-hints", "mypy", "static-analysis"]
    },
    {
        "q": "How does the `collections.defaultdict` differ from a standard dictionary in Python?",
        "sub": "Collections",
        "d": "Beginner",
        "ans": "A standard dictionary raises a `KeyError` when attempting to access or modify a key that does not exist. `collections.defaultdict` takes a factory callable (e.g., `int`, `list`, `set`) upon initialization. When a missing key is accessed, it automatically invokes the factory with no arguments, inserts the returned default value into the dictionary for that key, and returns it without raising an error. For example, `d = defaultdict(list); d['fruits'].append('apple')` works immediately without checking `if 'fruits' not in d: d['fruits'] = []`. It inherits all standard dictionary methods.",
        "kp": ["Accepts a default factory callable (`int`, `list`, `set`)", "Automatically initializes missing keys without raising KeyError", "Eliminates boilerplate `if key not in d` checks", "Subclass of dict; identical O(1) performance"],
        "cm": ["Passing an uncalled value instead of a callable factory (e.g., `defaultdict([])` instead of `defaultdict(list)`)", "Accidentally creating keys by merely checking existence (`if d['missing_key']:`)", "Confusing `defaultdict` with `dict.setdefault()`"],
        "fu": ["How does `dict.setdefault()` achieve similar behavior on standard dictionaries?", "Why does checking `if d['key']:` on a defaultdict accidentally insert the key?"],
        "tags": ["python", "collections", "defaultdict", "dictionaries"]
    },
    {
        "q": "Explain string interning in Python. How does it optimize memory and comparison speed?",
        "sub": "CPython Internals",
        "d": "Advanced",
        "ans": "String interning is an optimization in CPython where only one copy of distinct immutable string objects is stored in an internal lookup table. When strings are interned, multiple variables holding the identical string value point to the exact same memory address (`s1 is s2` evaluates to `True`). CPython automatically interns string constants that look like Python identifiers (alphanumeric plus underscores) and small compile-time strings. Interning saves memory by eliminating duplicate string allocations and accelerates comparisons from O(n) character-by-character scans to O(1) pointer identity checks. Manual interning is available via `sys.intern(s)`.",
        "kp": ["Single instance of distinct string values stored in CPython internal table", "Allows O(1) pointer comparisons via `is` instead of O(n) character checks", "CPython automatically interns identifier-like strings and string literals", "Manual interning supported via `sys.intern()` for high-volume dictionary keys"],
        "cm": ["Relying on string interning behavior for program logic instead of using `==`", "Assuming all strings, including user inputs or runtime concatenations, are interned automatically", "Confusing string interning with small integer caching (-5 to 256)"],
        "fu": ["Why does CPython intern small integers in the range `[-5, 256]` at startup?", "Why should application code always use `==` instead of `is` for string comparison?"],
        "tags": ["python", "internals", "string-interning", "memory", "optimization"]
    },
    {
        "q": "What is the difference between `__getattr__` and `__getattribute__` in Python?",
        "sub": "Metaprogramming",
        "d": "Advanced",
        "ans": "1) `__getattribute__(self, name)` is invoked unconditionally for EVERY attribute access on an object, regardless of whether the attribute exists in `__dict__` or not. Overriding it requires extreme caution, as accessing `self.attr` inside it triggers infinite recursion; developers must call `super().__getattribute__(name)`. 2) `__getattr__(self, name)` is a fallback invoked ONLY when the requested attribute was NOT found through normal mechanisms (`__getattribute__`, instance `__dict__`, class descriptors, or parent classes). `__getattr__` is commonly used for dynamic proxies, lazy attribute evaluation, and wrapping external APIs.",
        "kp": ["`__getattribute__`: called unconditionally for every single attribute access", "`__getattr__`: called only as fallback when attribute is missing", "Infinite recursion trap in `__getattribute__` requires `super().__getattribute__`", "Use `__getattr__` for proxies, mocking, and dynamic attribute fallbacks"],
        "cm": ["Accidentally causing infinite recursion inside `__getattribute__` by referencing `self.x`", "Using `__getattribute__` when the simpler `__getattr__` fallback suffices", "Raising AttributeError incorrectly inside dynamic property accessors"],
        "fu": ["How do mock libraries like `unittest.mock.MagicMock` utilize `__getattr__`?", "What is `__setattr__` and how do you prevent infinite recursion inside it?"],
        "tags": ["python", "dunder-methods", "metaprogramming", "getattr", "internals"]
    },
    {
        "q": "How does Python's `itertools` module help write memory-efficient iteration pipelines?",
        "sub": "Itertools",
        "d": "Intermediate",
        "ans": "The `itertools` module provides fast, memory-efficient C-implemented tools for creating iterators. Key utilities: 1) Infinite iterators: `count(start, step)`, `cycle(iterable)`, `repeat(elem)`. 2) Terminating iterators: `chain(*iterables)` concatenates sequences without creating intermediate lists; `islice(iterable, stop)` slices iterators lazily; `compress()`, `dropwhile()`, `takewhile()`. 3) Combinatoric iterators: `product()` (Cartesian product), `permutations()`, `combinations()`. All functions return lazy iterators that compute values on-the-fly, allowing developers to process massive data streams with constant O(1) memory.",
        "kp": ["High-performance C implementations of iterator algebra", "Lazy evaluation avoids intermediate list allocations in memory", "`chain` merges iterables sequentially without list copying", "Combinatorics: `product`, `permutations`, `combinations`"],
        "cm": ["Converting itertools objects immediately to lists with `list()`, destroying memory benefits", "Using nested for-loops instead of `itertools.product()`", "Writing manual stateful generators when built-in itertools functions already exist"],
        "fu": ["How does `itertools.chain.from_iterable()` flatten a list of lists efficiently?", "What is the difference between `combinations` and `permutations`?"],
        "tags": ["python", "itertools", "generators", "memory", "iterators"]
    },
    {
        "q": "How do you write unit tests in Python using `pytest`? What are fixtures and parameterized tests?",
        "sub": "Testing & QA",
        "d": "Intermediate",
        "ans": "`pytest` is Python's leading testing framework. Test functions are named with a `test_` prefix and use simple Python `assert` statements. Key features: 1) Fixtures (`@pytest.fixture`): modular setup and teardown dependencies injected into test functions by name, replacing bulky xUnit setup/teardown classes. Yield fixtures run teardown code after `yield`. 2) Parameterization (`@pytest.mark.parametrize`): runs the same test function across multiple input-output test cases without duplicating code. 3) Automatic test discovery, clean diff assertion reporting, and rich plugin ecosystem (e.g., pytest-cov, pytest-asyncio).",
        "kp": ["Test discovery: files `test_*.py`, functions `test_*`", "Native `assert` statements with detailed introspection output", "Fixtures (`@pytest.fixture`): modular setup/teardown dependency injection", "Parameterization (`@pytest.mark.parametrize`): tests multiple cases cleanly"],
        "cm": ["Using `unittest.TestCase` assert methods (assertEqual) when pytest native assert suffices", "Writing redundant copy-pasted test functions instead of using `@pytest.mark.parametrize`", "Not cleaning up external resources (files, DB rows) in fixture teardown"],
        "fu": ["How do fixture scopes (`function`, `module`, `session`) affect performance?", "How does `monkeypatch` or `unittest.mock.patch` mock external network calls in pytest?"],
        "tags": ["python", "pytest", "unit-testing", "fixtures", "qa"]
    },
    {
        "q": "How do you inspect and debug Python code using the built-in `pdb` / `breakpoint()`?",
        "sub": "Debugging",
        "d": "Beginner",
        "ans": "Python 3.7+ introduces the built-in `breakpoint()` function, which drops the runtime into an interactive debugger (by default `pdb`). Key commands in the pdb console: `n` (next line, steps over functions), `s` (step into function), `c` (continue execution until next breakpoint), `q` (quit execution), `p variable` or `pp variable` (print / pretty-print expression), `l` (list source code around current line), `w` (where: print stack trace), and `u`/`d` (up/down stack frames). Debugging with interactive breakpoints allows inspection of live variable state and local frames without littering code with ad-hoc print statements.",
        "kp": ["Built-in `breakpoint()` drops into interactive pdb session", "Commands: `n` (next), `s` (step in), `c` (continue), `p` (print), `q` (quit)", "Inspect local frame scope, variable values, and call stack (`w`)", "Clean alternative to inserting temporary `print()` statements"],
        "cm": ["Leaving `breakpoint()` or `import pdb; pdb.set_trace()` calls in code committed to Git", "Using print debugging exclusively for complex multi-layer bugs", "Forgetting to quit `q` before running automated test suites, hanging CI runners"],
        "fu": ["How can you configure the `PYTHONBREAKPOINT` environment variable to disable breakpoints in production?", "How do IDE graphical debuggers (VS Code / PyCharm) interface with Python's debugging hooks?"],
        "tags": ["python", "debugging", "pdb", "breakpoint", "troubleshooting"]
    },
    {
        "q": "What is the difference between synchronous file I/O and asynchronous file I/O in Python?",
        "sub": "File I/O & Concurrency",
        "d": "Intermediate",
        "ans": "Standard Python file operations (`open()`, `read()`, `write()`) are synchronous and blocking: the OS thread waits on physical disk I/O before executing subsequent instructions. While synchronous file I/O is simple and adequate for CLI scripts, executing blocking disk operations inside an asynchronous event loop blocks the entire loop, preventing other concurrent network requests from processing. Asynchronous file libraries like `aiofiles` offload disk I/O to a background threadpool using `asyncio.to_thread()`, allowing the main event loop to continue serving concurrent tasks while disk reads or writes complete.",
        "kp": ["Standard `open()` is synchronous and blocks the calling thread during disk I/O", "Blocking I/O inside async event loops halts all concurrent network tasks", "`aiofiles` offloads file operations to threadpools to maintain non-blocking concurrency", "Memory-mapped files (`mmap`) provide efficient random access for massive files"],
        "cm": ["Using synchronous `open().read()` inside FastAPI async endpoints under heavy traffic", "Forgetting to close file handles when not using `with` context managers", "Loading multi-gigabyte files into a single in-memory string variable"],
        "fu": ["How does `mmap` (memory-mapped files) allow reading large files without loading them into RAM?", "Why doesn't the Linux kernel provide fully non-blocking asynchronous disk I/O like epoll does for sockets?"],
        "tags": ["python", "file-io", "async", "aiofiles", "concurrency"]
    },
    {
        "q": "Explain Python's scope resolution rule (LEGB rule) with an illustrative example.",
        "sub": "Variable Scoping",
        "d": "Beginner",
        "ans": "Python resolves variable names using the LEGB rule, searching namespaces in order: 1) Local (L): names defined inside the current function. 2) Enclosing (E): names in the local scope of enclosing/outer functions (closures). 3) Global (G): names defined at the top level of the current module. 4) Built-in (B): pre-assigned built-in names (e.g., `len`, `range`, `print`). If a variable name is not found in any of these four scopes, Python raises a `NameError`. To reassign a global variable inside a local function, use `global var_name`; to reassign a variable from an enclosing outer function, use `nonlocal var_name`.",
        "kp": ["LEGB search order: Local -> Enclosing -> Global -> Built-in", "NameError raised if variable is not found in any of the four scopes", "`global` keyword binds assignment to module-level scope", "`nonlocal` keyword binds assignment to nearest enclosing function scope"],
        "cm": ["Shadowing built-in names (e.g., naming a variable `list = [1, 2]` or `str = 'x'`)", "UnboundLocalError: referencing a global variable locally before assigning to it without `global`", "Confusing enclosing closure scope with global module scope"],
        "fu": ["Why does `UnboundLocalError: local variable referenced before assignment` occur?", "How does Python determine if a variable is local at compile time?"],
        "tags": ["python", "scoping", "legb", "closures", "namespaces"]
    },
    {
        "q": "What are metaclasses in Python? When would you use one versus class decorators?",
        "sub": "Metaprogramming",
        "d": "Advanced",
        "ans": "In Python, classes are themselves objects, and their type is a metaclass. By default, the metaclass of all classes is `type`. A metaclass is a class whose instances are classes. Metaclasses define how classes are constructed by intercepting class creation via `__new__(mcs, name, bases, namespace)`. They are used in frameworks (like Django ORM or Pydantic v1) for automatic field registration, API validation, and enforcing architecture constraints. Rule of thumb: class decorators are simpler, more readable, and preferred for modifying classes; metaclasses are reserved when deep inheritance hooks or pre-creation interception is strictly necessary.",
        "kp": ["Classes are instances of metaclasses; default metaclass is `type`", "Defined by inheriting from `type`: `class Meta(type):`", "Customizes class creation by intercepting `__new__` and `__init__`", "Class decorators are simpler and preferred unless inheritance hooks are required"],
        "cm": ["Using metaclasses for simple tasks solvable with class decorators or `__init_subclass__`", "Tim Peters rule: 'If you wonder whether you need them, you don't'", "Introducing incompatible metaclass conflicts in multiple inheritance"],
        "fu": ["How does `__init_subclass__` in Python 3.6+ replace many common metaclass use cases?", "How does `type(name, bases, dict)` dynamically create classes at runtime?"],
        "tags": ["python", "metaclasses", "metaprogramming", "oop", "advanced"]
    },
    {
        "q": "How does Python's `hash()` function determine hashability? Why can lists not be hashed?",
        "sub": "Hashability & Dunder",
        "d": "Intermediate",
        "ans": "An object is hashable if it has a hash value that remains constant during its lifetime (implements `__hash__()`) and can be compared to other objects for equality (implements `__eq__()`). Hashable objects are required as dictionary keys and set elements. Mutable containers like lists, dicts, and sets are unhashable because modifying their contents changes their semantic equality; if their hash changed while stored in a hash table bucket, they could never be retrieved. By default, custom class instances are hashable based on their object identity id, but implementing `__eq__` without `__hash__` makes them unhashable.",
        "kp": ["Hashable objects require invariant hash code across lifetime and `__eq__` comparison", "Lists and dicts are mutable and unhashable, raising `TypeError: unhashable type`", "Dictionary keys and set elements must be hashable for hash table bucket lookups", "Custom classes implementing `__eq__` must explicitly implement `__hash__`"],
        "cm": ["Attempting to use a list as a dictionary key instead of a tuple", "Implementing `__eq__` on a custom class without implementing `__hash__`, breaking set inclusion", "Assuming tuples are always hashable (tuples containing lists are unhashable)"],
        "fu": ["What happens if two unequal objects produce the same hash value (hash collision)?", "Why does Python randomize hash seeds (`PYTHONHASHSEED`) across process starts?"],
        "tags": ["python", "hashability", "hash-table", "dictionaries", "sets"]
    },
    {
        "q": "What is the difference between string concatenation with `+`, `.join()`, and f-strings?",
        "sub": "String Performance",
        "d": "Beginner",
        "ans": "1) Concatenation with `+`: creates a new string object on every operation; chaining `+` inside a loop takes O(n^2) quadratic time due to repeated memory allocations. 2) `''.join(iterable)`: precalculates total memory length needed for all strings in the iterable and allocates a single destination buffer in C, running in optimal O(n) linear time. 3) f-strings (PEP 498): formatted string literals evaluated at runtime using optimized `BUILD_STRING` bytecode; faster and far more readable than `%` formatting or `.format()`. For joining lists of strings, use `join()`; for template interpolation, use f-strings.",
        "kp": ["`+` in loops causes quadratic O(n^2) time due to string immutability", "`''.join(iterable)` pre-allocates memory and runs in linear O(n) time", "f-strings provide fast, readable expression interpolation at runtime", "Avoid `%` formatting and `.format()` in modern Python code"],
        "cm": ["Accumulating strings inside a loop with `result += chunk`", "Converting non-strings manually before `join()` instead of using generator expressions", "Complex logic expressions inside f-strings that damage readability"],
        "fu": ["How does CPython's `BUILD_STRING` bytecode make f-strings faster than `str.format()`?", "Can f-strings execute arbitrary Python expressions inside `{}`?"],
        "tags": ["python", "strings", "f-strings", "performance", "join"]
    },
    {
        "q": "What are weak references in Python, and how does the `weakref` module help prevent memory leaks?",
        "sub": "Memory Management",
        "d": "Advanced",
        "ans": "A weak reference (`weakref` module) allows referencing an object without increasing its reference count (`ob_refcnt`). When the only remaining references to an object are weak references, CPython's garbage collector deallocates the object and frees its memory immediately. Weak references are used to implement in-memory caches, observer patterns, and circular references (like parent-child graph nodes) without causing circular reference leaks. `weakref.ref(obj)` creates a callable weak reference, while `weakref.WeakValueDictionary` automatically removes entries when their values are garbage collected.",
        "kp": ["Weak references do not increment object reference counts", "Object is deallocated when all strong references are removed", "Prevents memory leaks in parent-child circular relationships and caches", "Provided by `weakref` module (`ref`, `WeakValueDictionary`, `WeakKeyDictionary`)"],
        "cm": ["Attempting to create weak references to built-in types (like int or list) without subclassing", "Not checking if the dereferenced weak reference is None before accessing attributes", "Using standard dictionaries for caching without eviction, leaking memory over time"],
        "fu": ["What does calling a weak reference object `ref()` return when the target object has been deleted?", "How does `weakref.WeakKeyDictionary` differ from `weakref.WeakValueDictionary`?"],
        "tags": ["python", "weakref", "memory-management", "garbage-collection", "caching"]
    }
]

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    f1 = OUT_DIR / "01.json"
    f2 = OUT_DIR / "02.json"
    f3 = OUT_DIR / "03.json"
    f1.write_text(json.dumps(PART1, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    f2.write_text(json.dumps(PART2, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    f3.write_text(json.dumps(PART3, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(PART1)} to 01.json, {len(PART2)} to 02.json, {len(PART3)} to 03.json (Total: {len(PART1) + len(PART2) + len(PART3)})")

if __name__ == "__main__":
    main()
