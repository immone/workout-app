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
        # List of hard clauses
        self.hard = []

    def set_lits(self, literals):
        """Set the literals for the scheduling problem."""
        self.lits = literals

    def set_soft(self, soft_clauses):
        """Set the soft clauses for the scheduling problem."""
        self.soft = soft_clauses

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
        # Create a weighted CNF formula
        wcnf = WCNF()
        
        # Create an Exactly-K constraint using the literals
        enc = CardEnc.equals(lits=self.lits, bound=k)
        wcnf.extend(enc)  # Add the cardinality constraint to the WCNF

        # Initialize the RC2 solver with the WCNF
        rc2 = RC2(wcnf)

        # Add hard clauses to the solver
        for clause in self.hard:
            rc2.add_clause(clause)  # Hard constraints must be satisfied

        # Add soft clauses to the solver with their respective weights
        for clause, weight in self.soft:
            rc2.add_clause(clause, weight)  # Weights allow for flexibility in solutions

        # Compute the solution using the RC2 solver
        model = rc2.compute()
        
        # Return the cost of the solution; may want to handle if no solution exists
        return rc2.cost if model else None