from flask_sqlalchemy import SQLAlchemy
from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
from pysat.card import CardEnc

class Scheduler:
    def __init__(self):
        # List to store literals for the SAT solver
        self.lits = []
        # List of soft clauses in the form ([clause], weight_of_clause)
        self.soft = []
        # List of hard clauses // Note that this name is a currently little confusing and should be renamed
        self.hard = []
        # List of penalty clauses
        self.penalty = []

    def set_lits(self, literals):
        """Set the literals for the scheduling problem."""
        if not isinstance(literals, list):
            raise ValueError("literals must be a list.")
        self.lits = literals

    def set_soft(self, soft_clauses):
        """Set the soft clauses for the scheduling problem."""
        # Ensure each clause is a list
        self.soft = soft_clauses

    def set_penalty(self, penalty_clauses):
        """Set penalization for same day workouts"""
        self.penalty = penalty_clauses

    def set_hard(self, hard_clauses):
        """Set the hard clauses for the scheduling problem."""
        self.hard = hard_clauses

    def solve_schedule(self, k):
        """
        Use SAT solver to find a valid schedule.

        Args:
            k (int): The bound for the Exactly-K constraint.

        Returns:
            int: The cost of the schedule if found, else None.
        """
        # Check if lits is a list and print debugging information
        if not isinstance(self.lits, list):
            raise ValueError("self.lits is not a list.")
        
        print("Contents of self.lits:", self.lits)
        print("Number of literals:", len(self.lits))
        print("Value of k:", k)
        
        if len(self.lits) < k:
            raise ValueError(f"Cannot create an Exactly-K constraint with k={k} for {len(self.lits)} literals.")

        # Create a weighted CNF formula
        wcnf = WCNF()
        
        # Create an Exactly-K constraint using the literals
        enc = CardEnc.equals(lits=self.lits, bound=k)
        wcnf.extend(enc)  # Add the cardinality constraint to the WCNF

        # Penalize for choosing overlapping times
        for clause in self.hard:
            print("Hard clause:", clause)
            # Negate literals in the hard clause
            wcnf.append(clause, weight=100)

        # Penalize for choosing same days
        for pen in self.penalty:
            print("Penalty clause for same day", pen)
            # Negate literals in the penalty clause
            wcnf.append(pen, weight=100)

        # Add soft clauses with respective weights (negated literals)
        for weight, clause in self.soft:
            print("Soft clause:", clause, "with weight:", weight)
            wcnf.append([-clause], weight)  # Negate literals in the soft clause

        # Initialize the RC2 solver with the WCNF
        rc2 = RC2(wcnf)
        # Compute the solution using the RC2 solver
        print("Solving...")
        model = rc2.compute()
        if model:
            print("Found solution!")
            return (rc2.cost, model)
        else:
            print("No solution found.")
            return None
