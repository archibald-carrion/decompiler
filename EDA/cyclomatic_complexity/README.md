# Cyclomatic Complexity Analysis

This repository contains tools for analyzing code metrics in C functions, including cyclomatic complexity.

## What is Cyclomatic Complexity?

Cyclomatic complexity is a software metric used to indicate the complexity of a program. It directly measures the number of linearly independent paths through a program's source code.

### Definition

Developed by Thomas J. McCabe in 1976, cyclomatic complexity measures the number of decision points in a program plus one. Decision points include:

- `if` statements
- `for` and `while` loops
- `case` statements in a `switch`
- Logical operators (`&&`, `||`) in conditions
- Conditional expressions (`? :`)

### Formula

The formula for cyclomatic complexity can be expressed as:

```
M = E - N + 2P
```

Where:
- M = Cyclomatic complexity
- E = Number of edges in the control flow graph
- N = Number of nodes in the control flow graph
- P = Number of connected components (usually 1 for a single function)

In practice, a simpler way to calculate it is:

```
M = Number of decision points + 1
```

### Interpretation

Cyclomatic complexity values typically indicate:

| Complexity | Risk Level | Interpretation |
|------------|------------|----------------|
| 1-10       | Low        | Well-structured and stable code |
| 11-20      | Moderate   | Moderately complex, moderate risk |
| 21-50      | High       | Complex code, high risk |
| >50        | Very High  | Unstable code, very high risk |

### Why It Matters

High cyclomatic complexity indicates:

1. **Increased testing effort**: More test cases are needed to achieve full path coverage
2. **Higher maintenance costs**: Complex code is harder to understand and modify
3. **Greater bug risk**: Complex code is more likely to contain defects
4. **Reduced readability**: Complex code is harder for developers to comprehend

### Best Practices

To reduce cyclomatic complexity:

- Extract complex conditional logic into separate functions
- Use early returns instead of deeply nested conditionals
- Refactor large functions into smaller, more focused functions
- Use polymorphism instead of complex switch statements
- Simplify boolean expressions

## Using the Scripts

The scripts in this repository allow you to:

1. Extract function definitions from C code
2. Calculate cyclomatic complexity using the lizard library
3. Visualize the distribution of complexity across functions
4. Identify high-complexity functions that may need refactoring

### Requirements

- Python 3.6+
- lizard
- matplotlib
- numpy
- zstandard

Install requirements with:

```bash
pip install lizard matplotlib numpy zstandard
```

### Example Usage

```bash
python cyclomatic_complexity_analysis.py
```