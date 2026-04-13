"""
Tests for DELETE /activities/{activity_name}/participants/{email} endpoint using AAA pattern.
"""

import pytest


class TestRemoveParticipant:
    """Test suite for removing a student from an activity."""

    def test_remove_participant_returns_200_on_success(self, client, fresh_activities):
        """
        Test that successful removal returns HTTP 200 status code.
        
        Arrange: Valid activity and existing participant
        Act: DELETE participant endpoint
        Assert: Status code is 200
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Existing participant
        expected_status = 200
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == expected_status

    def test_remove_participant_returns_success_message(self, client, fresh_activities):
        """
        Test that removal returns a success message.
        
        Arrange: Valid activity and participant
        Act: DELETE participant
        Assert: Response contains success message with email and activity name
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        data = response.json()
        
        # Assert
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_remove_participant_actually_removes_from_list(self, client, fresh_activities):
        """
        Test that removal actually removes the participant from the activity.
        
        Arrange: Get initial participant count and list
        Act: Remove a participant
        Assert: Participant count decreased and email no longer in list
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        initial_count = len(fresh_activities[activity_name]["participants"])
        
        # Act
        client.delete(f"/activities/{activity_name}/participants/{email}")
        response = client.get("/activities")
        updated_participants = response.json()[activity_name]["participants"]
        
        # Assert
        assert len(updated_participants) == initial_count - 1
        assert email not in updated_participants

    def test_remove_participant_nonexistent_activity_returns_404(self, client, fresh_activities):
        """
        Test that removing from nonexistent activity returns 404.
        
        Arrange: Nonexistent activity name
        Act: DELETE from nonexistent activity
        Assert: Status code is 404
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        expected_status = 404
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == expected_status
        assert response.json()["detail"] == "Activity not found"

    def test_remove_nonexistent_participant_returns_404(self, client, fresh_activities):
        """
        Test that removing nonexistent participant returns 404.
        
        Arrange: Valid activity but participant not in list
        Act: DELETE nonexistent participant
        Assert: Status code is 404 and error message provided
        """
        # Arrange
        activity_name = "Chess Club"
        email = "nonexistent@mergington.edu"
        expected_status = 404
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == expected_status
        assert "not signed up" in response.json()["detail"].lower()

    def test_remove_participant_from_activity_with_one_participant(self, client, fresh_activities):
        """
        Test removing the only participant from an activity.
        
        Arrange: Activity with one participant (Art Studio has isabella@mergington.edu)
        Act: Remove the participant
        Assert: Participants list becomes empty
        """
        # Arrange
        activity_name = "Gym Class"
        email = "john@mergington.edu"
        
        # Act
        client.delete(f"/activities/{activity_name}/participants/{email}")
        client.delete(f"/activities/{activity_name}/participants/olivia@mergington.edu")
        response = client.get("/activities")
        
        # Assert
        participants = response.json()[activity_name]["participants"]
        assert len(participants) == 0

    def test_remove_first_participant_from_list(self, client, fresh_activities):
        """
        Test removing the first participant from a list.
        
        Arrange: Activity with multiple participants
        Act: Remove the first participant
        Assert: First participant removed but others remain
        """
        # Arrange
        activity_name = "Chess Club"
        first_email = "michael@mergington.edu"
        second_email = "daniel@mergington.edu"
        
        # Act
        client.delete(f"/activities/{activity_name}/participants/{first_email}")
        response = client.get("/activities")
        
        # Assert
        participants = response.json()[activity_name]["participants"]
        assert first_email not in participants
        assert second_email in participants

    def test_remove_last_participant_from_list(self, client, fresh_activities):
        """
        Test removing the last participant from a list.
        
        Arrange: Activity with multiple participants
        Act: Remove the last participant
        Assert: Last participant removed but others remain
        """
        # Arrange
        activity_name = "Chess Club"
        first_email = "michael@mergington.edu"
        second_email = "daniel@mergington.edu"
        
        # Act
        client.delete(f"/activities/{activity_name}/participants/{second_email}")
        response = client.get("/activities")
        
        # Assert
        participants = response.json()[activity_name]["participants"]
        assert first_email in participants
        assert second_email not in participants

    def test_remove_only_removes_exact_email(self, client, fresh_activities):
        """
        Test that removal only removes exact email match.
        
        Arrange: Participant with similar but different email
        Act: Try to remove with partial or modified email
        Assert: Original participant remains, 404 returned
        """
        # Arrange
        activity_name = "Chess Club"
        correct_email = "michael@mergington.edu"
        wrong_email = "michael@mergington.com"  # Different domain
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{wrong_email}"
        )
        activities_response = client.get("/activities")
        
        # Assert
        assert response.status_code == 404
        assert correct_email in activities_response.json()[activity_name]["participants"]

    def test_remove_participant_activity_name_is_case_sensitive(self, client, fresh_activities):
        """
        Test that activity names are case-sensitive in removal.
        
        Arrange: Wrong case activity name
        Act: DELETE with wrong case
        Assert: Returns 404
        """
        # Arrange
        activity_name = "chess club"  # Wrong case
        email = "michael@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 404

    def test_remove_and_resign_up_same_participant(self, client, fresh_activities):
        """
        Test that a removed participant can sign up again.
        
        Arrange: Participant in activity
        Act: Remove then sign up again
        Assert: Participant is back in the list
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        client.delete(f"/activities/{activity_name}/participants/{email}")
        removal_response = client.get("/activities")
        
        client.post(f"/activities/{activity_name}/signup", params={"email": email})
        signup_response = client.get("/activities")
        
        # Assert
        removed_participants = removal_response.json()[activity_name]["participants"]
        assert email not in removed_participants
        
        readded_participants = signup_response.json()[activity_name]["participants"]
        assert email in readded_participants
