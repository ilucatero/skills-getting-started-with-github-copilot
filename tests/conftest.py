"""
Pytest configuration and shared fixtures for FastAPI tests.
"""

import pytest
from fastapi.testclient import TestClient
import src.app as app_module


@pytest.fixture
def client():
    """
    Fixture providing a TestClient for the FastAPI app.
    """
    return TestClient(app_module.app)


@pytest.fixture
def fresh_activities(monkeypatch):
    """
    Fixture resetting activities to initial state before each test.
    This ensures test isolation - each test starts with a clean state.
    """
    initial_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }
    
    # Replace the activities dictionary in the app module
    monkeypatch.setattr(app_module, "activities", initial_activities)
    return initial_activities
