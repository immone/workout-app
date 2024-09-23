# Scheduler 

## SAT 
A SAT (Boolean Satisfiability) problem asks whether there exists a valuation (an assignment of truth values, true or false, to each variable) that makes a given Boolean formula true. The formula is typically in Conjunctive Normal Form (CNF), meaning it is a conjunction (AND) of clauses, where each clause is a disjunction (OR) of literals (variables or their negations).

## CNF
A propositional logic sentence $\varphi$ is said to be in CNF if it is formed by taking a conjunction over disjunctions, i.e.,

$$ 
    \varphi = \bigwedge_{i} \left( \bigvee_j x_{ij} \right)
$$

An extension of CNF is achieved by associating a weight $c_{ij}: x_{ij} \mapsto c \in \mathbb{R}$ for each $x_{ij}$.

## MAXSAT
The scheduler is based on solving a [MAX-SAT problem](https://en.wikipedia.org/wiki/Maximum_satisfiability_problem), which is an example of a weighted CNF based on the idea of *soft* and *hard* clauses.

## PySAT
The scheduler uses [PySAT](https://pysathq.github.io) to compute and solve the `MAX-SAT` problem. PySAT is a Python toolkit for solving Boolean Satisfiability (SAT) problems. SAT problems involve determining whether there exists an assignment of truth values to variables that satisfies a given Boolean formula. PySAT provides an interface to a variety of SAT solvers, allowing users to model, solve, and analyze SAT problems within Python.
