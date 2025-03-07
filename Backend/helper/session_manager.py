import uuid

class Session:
    def __init__(self):
        self.extracted = None
        self.user_query = None
        self.news_analysis = None  # used to pass news data to sentiment analysis
        self.stock = None
        self.sentiment = None
        self.news_data = None
        self.citations = None

# Create a SessionManager that manages all sessions.
class SessionManager:
    def __init__(self):
        # Use a dictionary to store sessions by a session_id (could also be a list)
        self.sessions = {}

    def create_session(self):
        # Create a new session with a unique ID.
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = Session()
        return session_id

    def get_session(self, session_id):
        return self.sessions.get(session_id)

    def reset_session(self, session_id):
        # Re-initialize a session for a new query.
        self.sessions[session_id] = Session()
        return self.sessions[session_id]