"""
Tests for GET /activities endpoint using AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestGetActivities:
    """Test suite for retrieving all activities."""

    def test_get_activities_returns_200(self, client, fresh_activities):
        """
        Test that GET /activities returns HTTP 200 status code.
        
        Arrange: TestClient is ready
        Act: Make GET request to /activities
        Assert: Status code is 200
        """
        # Arrange
        expected_status = 200
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == expected_status

    def test_get_activities_returns_dict(self, client, fresh_activities):
        """
        Test that GET /activities returns a dictionary of activities.
        
        Arrange: TestClient is ready
        Act: Make GET request to /activities
        Assert: Response data is a dictionary
        """
        # Arrange
        # (fixture is ready)
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert isinstance(data, dict)

    def test_get_activities_contains_all_activities(self, client, fresh_activities):
        """
        Test that GET /activities returns all expected activities.
        
        Arrange: Fresh activities with 3 expected activities
        Act: Make GET request to /activities
        Assert: Response contains all 3 activities
        """
        # Arrange
        expected_activity_names = ["Chess Club", "Programming Class", "Gym Class"]
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert len(data) == 3
        for activity_name in expected_activity_names:
            assert activity_name in data

    def test_get_activities_returns_complete_activity_object(self, client, fresh_activities):
        """
        Test that each activity contains all required fields.
        
        Arrange: Expected fields for an activity
        Act: Get activities and inspect one
        Assert: Activity has description, schedule, max_participants, participants
        """
        # Arrange
        expected_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        first_activity = activities["Chess Club"]
        
        # Assert
        assert set(first_activity.keys()) == expected_fields

    def test_get_activities_chess_club_data(self, client, fresh_activities):
        """
        Test that Chess Club activity has correct data.
        
        Arrange: Expected Chess Club details
        Act: Get activities and extract Chess Club
        Assert: Verify all fields match expected values
        """
        # Arrange
        expected_chess_club = {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        }
        
        # Act
        response = client.get("/activities")
        chess_club = response.json()["Chess Club"]
        
        # Assert
        assert chess_club == expected_chess_club

    def test_get_activities_participants_is_list(self, client, fresh_activities):
        """
        Test that participants field is always a list.
        
        Arrange: Get activities
        Act: Check participants field type for each activity
        Assert: All participants fields are lists
        """
        # Arrange
        # (fixture is ready)
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["participants"], list)
