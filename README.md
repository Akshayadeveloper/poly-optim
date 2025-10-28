# poly-optim
<b>Focus: </b>Dynamic optimization and performance acceleration of multi-language codebases.

<b>Core Problem Solved :</b>

Identifies and replaces performance bottlenecks in high-level languages (like Python) by compiling and executing those critical sections in a unified, faster environment (like C/Rust or a custom intermediate representation) at runtime, transparently, and only when profiling deems it necessary. This is an advanced form of selective Just-In-Time (JIT) optimization.

<b>The Solution Mechanism (Python) :</b>

A Python decorator-based system that profiles function execution and, if a threshold is crossed, triggers an external 'compiled' (mocked) function call instead of the native Python execution.
