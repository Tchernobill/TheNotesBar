import datetime
import sqlite3

DB_NAME = "notes.db"

class Note:
    def __init__(self, title="New Note", content="", note_type="Standard", note_id=None):
        self.id = note_id if note_id is not None else datetime.datetime.now().timestamp()  # Using timestamp as a unique ID
        self.title = title
        self.content = content
        self.type = note_type  # New "type" attribute
        self.creation_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def update_content(self, content):
        self.content = content

    def update_title(self, title):
        self.title = title

    def update_type(self, note_type):
        self.type = note_type

    def to_dict(self):
        """Convert the note to a dictionary for easier serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'type': self.type,  # Include the type in serialization
            'creation_date': self.creation_date
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Note instance from a dictionary."""
        note = cls(data['title'], data['content'], data['type'], data['id'])
        note.creation_date = data['creation_date']
        return note

class NotesManager:
    def __init__(self):
        # Create the database and table if they don't exist
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS notes
                               (id INTEGER PRIMARY KEY, title TEXT, content TEXT, type TEXT, creation_date TEXT)''')
        self.conn.commit()

    def add_note(self, title, content, note_type="text"):
        creation_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute("INSERT INTO notes (title, content, type, creation_date) VALUES (?, ?, ?, ?)",
                            (title, content, note_type, creation_date))
        self.conn.commit()

    def load_notes(self):
        self.cursor.execute("SELECT id, title, content, type, creation_date FROM notes")
        rows = self.cursor.fetchall()
        return [Note(title=row[1], content=row[2], note_id=row[0], note_type=row[3]) for row in rows]

    # ... [other functions unchanged]

    def populate_sample_notes(self):
        sample_notes = [
            ("Test Note 1", "This is the content for Test Note 1", "text"),
            ("Sample Note 2", "This is for the Sample Note 2", "text"),
            ("Other Note 3", "This is the content for Sample Note 3", "text"),
            ("Sample Note 4", "This is the content for Sample Note 4", "text"),
            ("Sample Note 5", "This is the content for Sample Note 5", "text"),
            ("Sample Note 6", "This is the content for Sample Note 6", "text"),
        ]
        
        for title, content, note_type in sample_notes:
            self.add_note(title, content, note_type)

    # Don't forget to close the connection when the manager is deleted
    def __del__(self):
        self.conn.close()