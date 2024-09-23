# tests/test_scheduler.py
import pytest
from pysat.formula import WCNF
from pysat.card import CardEnc
from pysat.examples.rc2 import RC2
from src.models.scheduler import Scheduler

def test_set_lits():
    scheduler = Scheduler()
    literals = [1, 2, 3]
    scheduler.set_lits(literals)
    assert scheduler.lits == literals

def test_set_soft():
    scheduler = Scheduler()
    soft_clauses = [([1, 2], 1), ([2, 3], 2)]
    scheduler.set_soft(soft_clauses)
    assert scheduler.soft == soft_clauses

def test_set_hard():
    scheduler = Scheduler()
    hard_clauses = [[1], [2, 3]]
    scheduler.set_hard(hard_clauses)
    assert scheduler.hard == hard_clauses

def test_solve_schedule():
    scheduler = Scheduler()
    
    # Set up test literals
    literals = [1, 2, 3, 4]
    scheduler.set_lits(literals)
    
    # Set up hard clauses
    hard_clauses = [[1, 2], [-3]]  # Example hard constraints
    scheduler.set_hard(hard_clauses)
    
    # Set up soft clauses with weights
    soft_clauses = [([3, 4], 1), ([2, 3], 2)]  # Example soft constraints
    scheduler.set_soft(soft_clauses)
    
    # Solve with k = 2 (we want exactly 2 literals to be true)
    cost = scheduler.solve_schedule(k=2)

    # Check that the cost is not None (solution found)
    assert cost == 1