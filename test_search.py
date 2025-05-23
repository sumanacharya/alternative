import pytest
from search import google_dork_count

def test_google_dork_count(monkeypatch):
    # Mock response data
    mock_response = {
        "search_information": {
            "total_results": 42
        }
    }
    
    # Mock the GoogleSearch class
    class MockGoogleSearch:
        def __init__(self, params):
            self.params = params
            
        def get_dict(self):
            return mock_response
    
    # Apply the monkeypatch
    monkeypatch.setattr("search.GoogleSearch", MockGoogleSearch)
    
    # Test the function
    result = google_dork_count("test@example.com")
    assert result == 42

def test_google_dork_count_no_results(monkeypatch):
    # Mock response with no results
    mock_response = {
        "search_information": {
            "total_results": 0
        }
    }
    
    class MockGoogleSearch:
        def __init__(self, params):
            self.params = params
            
        def get_dict(self):
            return mock_response
    
    monkeypatch.setattr("search.GoogleSearch", MockGoogleSearch)
    
    result = google_dork_count("nonexistent@example.com")
    assert result == 0

def test_google_dork_count_missing_data(monkeypatch):
    # Mock response with missing data
    mock_response = {}
    
    class MockGoogleSearch:
        def __init__(self, params):
            self.params = params
            
        def get_dict(self):
            return mock_response
    
    monkeypatch.setattr("search.GoogleSearch", MockGoogleSearch)
    
    result = google_dork_count("test@example.com")
    assert result == 0 