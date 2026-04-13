"""
Tests for POST /activities/{activity_name}/signup endpoint using AAA pattern.
"""

import pytest


class TestSignupForActivity:
    """Test suite for signing up a student for an activity."""

    def test_signup_returns_200_on_success(self, client, fresh_activities):
        """
        Test that successful signup returns HTTP 200 status code.
        
        Arrange: Valid activity name and email
        Act: POST to signup endpoint
        Assert: Status code is 200
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        expected_status = 200
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == expected_status

    def test_signup_returns_success_message(self, client, fresh_activities):
        """
        Test that signup returns a success message.
        
        Arrange: Valid activity and email
        Act: POST to signup endpoint
        Assert: Response contains success message with email and activity name
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_adds_participant_to_activity(self, client, fresh_activities):
        """
        Test that signup actually adds the participant to the activity.
        
        Arrange: Get initial participant count for an activity
        Act: Sign up new student
        Assert: Participant count increased and email is in participants list
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        initial_count = len(fresh_activities[activity_name]["participants"])
        
        # Act
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        response = client.get("/activities")
        updated_participants = response.json()[activity_name]["participants"]
        
        # Assert
        assert len(updated_participants) == initial_count + 1
        assert email in updated_participants

    def test_signup_nonexistent_activity_returns_404(self, client, fresh_activities):
        """
        Test that signup to nonexistent activity returns 404.
        
        Arrange: Nonexistent activity name and valid email
        Act: POST to signup endpoint
        Assert: Status code is 404 and error details provided
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        expected_status = 404
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == expected_status
        assert response.json()["detail"] == "Activity not found"

    def test_signup_duplicate_participant_returns_400(self, client, fresh_activities):
        """
        Test that duplicate signup returns 400 Bad Request.
        
        Arrange: Already registered participant and existing activity
        Act: Try to sign up the same student again
        Assert: Status code is 400 and error message indicates already signed up
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in Chess Club
        expected_status = 400
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == expected_status
        assert "already signed up" in response.json()["detail"].lower()

    def test_signup_activity_name_is_case_sensitive(self, client, fresh_activities):
        """
        Test that activity names are case-sensitive.
        
        Arrange: Activity name with different case
        Act: Try to signup with wrong case
        Assert: Returns 404 not found
        """
        # Arrange
        activity_name = "chess club"  # Wrong case
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404

    def test_signup_with_special_characters_in_email(self, client, fresh_activities):
        """
        Test that emails with special characters can be used (no validation).
        
        Arrange: Email with special characters
        Act: Sign up with special character email
        Assert: Returns 200 and email is added
        """
        # Arrange
        activity_name = "Chess Club"
        email = "student+test@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity_name]["participants"]
        assert email in participants

    def test_signup_multiple_students_for_same_activity(self, client, fresh_activities):
        """
        Test that multiple different students can sign up for same activity.
        
        Arrange: Two different emails and one activity
        Act: Sign up both students
        Assert: Both are added to participants list
        """
        # Arrange
        activity_name = "Chess Club"
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        
        # Act
        client.post(f"/activities/{activity_name}/signup", params={"email": email1})
        client.post(f"/activities/{activity_name}/signup", params={"email": email2})
        
        # Assert
        response = client.get("/activities")
        participants = response.json()[activity_name]["participants"]
        assert email1 in participants
        assert email2 in participants

    def test_signup_same_student_different_activities(self, client, fresh_activities):
        """
        Test that same student can sign up for different activities.
        
        Arrange: One student and two different activities
        Act: Sign up student for both activities
        Assert: Student appears in both activities
        """
        # Arrange
        email = "newstudent@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Programming Class"
        
        # Act
        client.post(f"/activities/{activity1}/signup", params={"email": email})
        client.post(f"/activities/{activity2}/signup", params={"email": email})
        
        # Assert
        response = client.get("/activities")
        activities = response.json()
        assert email in activities[activity1]["participants"]
        assert email in activities[activity2]["participants"]
