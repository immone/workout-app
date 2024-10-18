# tests/test_scheduler.py
import pytest
from pysat.formula import WCNF
from pysat.card import CardEnc
from pysat.examples.rc2 import RC2
from src.models.scheduler import Scheduler

@pytest.fixture
def scheduler():
    return Scheduler()

def test_set_lits(scheduler):
    literals = [1, 2, 3]
    scheduler.set_lits(literals)
    assert scheduler.lits == literals

def test_set_lits_invalid():
    scheduler = Scheduler()
    with pytest.raises(ValueError):
        scheduler.set_lits("not a list")

def test_set_soft(scheduler):
    soft_clauses = [([1, 2], 1), ([2, 3], 2)]
    scheduler.set_soft(soft_clauses)
    assert scheduler.soft == soft_clauses

def test_set_hard(scheduler):
    hard_clauses = [[1], [2, 3]]
    scheduler.set_hard(hard_clauses)
    assert scheduler.hard == hard_clauses

def test_set_penalty(scheduler):
    penalty_clauses = [[1, 2], [3, 4]]
    scheduler.set_penalty(penalty_clauses)
    assert scheduler.penalty == penalty_clauses

def test_solve_schedule(scheduler):
    literals = [1, 2, 3, 4]
    scheduler.set_lits(literals)
    hard_clauses = [[1, 2], [-3]]
    scheduler.set_hard(hard_clauses)
    soft_clauses = [([3, 4], 1), ([2, 3], 2)]
    scheduler.set_soft(soft_clauses)

    cost = scheduler.solve_schedule(k=2)
    assert cost is not None  # Ensure a solution was found

def test_solve_schedule_no_literals():
    scheduler = Scheduler()
    scheduler.set_lits([])
    scheduler.set_hard([])
    scheduler.set_soft([])
    with pytest.raises(ValueError):
        scheduler.solve_schedule(k=1)

def test_solve_schedule_no_valid_schedule():
    scheduler = Scheduler()
    scheduler.set_lits([1, 2])
    scheduler.set_hard([[1], [-1]])  # Conflicting hard clauses
    cost = scheduler.solve_schedule(k=1)
    assert cost is None

def test_solve_schedule_multiple_schedules():
    scheduler = Scheduler()
    scheduler.set_lits([1, 2, 3])
    scheduler.set_hard([[1], [-2]])  # Hard constraints
    scheduler.set_soft( [(1, 1)] )  # Soft constraint
    scheduler.set_soft( [ (3, 1), (1,1)  ])

    cost1, model1 = scheduler.solve_schedule(k=1)
    assert cost1 is not None  

    cost2, model2 = scheduler.solve_schedule(k=2)
    assert cost2 is not None  
    assert cost2 <= cost1  # Soft clauses should minimize cost

def test_set_soft_with_weights(scheduler):
    soft_clauses = [([1, 2], 5), ([2, 3], 3)]
    scheduler.set_soft(soft_clauses)
    assert scheduler.soft == soft_clauses
