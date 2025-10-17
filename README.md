# Meeting Management System

A complete full-stack meeting management application with FastAPI backend and vanilla JavaScript frontend.

## Features

- **Full CRUD Operations**: Create, Read, Update, Delete meetings
- **Complete Meeting Details**:
  - Meeting Title
  - Date & Time
  - Participants (add/remove with tags)
  - Agenda
  - Notes
- **Real-time Data Sync**: All changes save to `data.json`
- **Password Protection**: Secure access with password authentication
- **Import/Export**: Export and import meeting data as JSON
- **Auto-refresh**: Data refreshes every 5 seconds

## Project Structure

```
meeting/
├── main.py           # FastAPI backend with full CRUD API
├── index.html        # Frontend interface
├── data.json         # Data storage (auto-created)
└── README.md         # This file
```

## Setup & Installation

### 1. Install Dependencies

```bash
pip install fastapi uvicorn pydantic
```

### 2. Start the Backend Server

```bash
python main.py
```

The server will start at `http://localhost:8000`

### 3. Open the Frontend

Open `index.html` in your web browser.

**Default Password**: `netpace2025`

## API Endpoints

### Base URL: `http://localhost:8000`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/api/meetings` | Get all meetings |
| GET | `/api/meetings/{id}` | Get specific meeting |
| POST | `/api/meetings` | Create new meeting |
| PUT | `/api/meetings/{id}` | Update meeting |
| DELETE | `/api/meetings/{id}` | Delete meeting |
| POST | `/api/meetings/bulk` | Bulk save all meetings |

## Data Structure

### Meeting Object

```json
{
  "id": "unique-id",
  "title": "Meeting Title",
  "date": "2025-10-16",
  "time": "14:30",
  "participants": ["John Doe", "Jane Smith"],
  "agenda": "Discuss project timeline",
  "notes": "Meeting notes and discussions"
}
```

### data.json Format

```json
{
  "meetings": [
    {
      "id": "meeting-123",
      "title": "Team Sync",
      "date": "2025-10-16",
      "time": "10:00",
      "participants": ["Alice", "Bob"],
      "agenda": "Weekly sync",
      "notes": "Discussed progress on current tasks"
    }
  ]
}
```

## Usage Guide

### Adding a Meeting

1. Click **"+ Add New Meeting"**
2. Fill in the meeting details
3. Add participants by typing name and pressing Enter
4. Click **"Save"**

### Editing a Meeting

1. Modify any field in the meeting card
2. Click **"Save"** to persist changes

### Deleting a Meeting

1. Click **"Delete"** button on the meeting card
2. Confirm deletion

### Export/Import Data

- **Export**: Click **"Export Data"** to download `data.json`
- **Import**: Click **"Import Data"** and select a JSON file

## Backend Features

### CRUD Operations

- **Create**: Auto-generates unique UUID for each meeting
- **Read**: Fetch all or specific meetings
- **Update**: Partial updates supported (only changed fields)
- **Delete**: Safe deletion with error handling

### Data Validation

- Pydantic models ensure data integrity
- Optional fields allow flexible data entry
- Extra fields allowed for extensibility

### Error Handling

- HTTP 404 for not found resources
- HTTP 500 for server errors
- Descriptive error messages

## Security

- Password protection with session timeout (30 minutes)
- CORS enabled for development
- XSS protection via HTML escaping

## Testing the API

### Using cURL

```bash
# Get all meetings
curl http://localhost:8000/api/meetings

# Create a meeting
curl -X POST http://localhost:8000/api/meetings \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Meeting","date":"2025-10-16","time":"10:00"}'

# Update a meeting
curl -X PUT http://localhost:8000/api/meetings/{meeting_id} \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated Title"}'

# Delete a meeting
curl -X DELETE http://localhost:8000/api/meetings/{meeting_id}
```

## Troubleshooting

### Backend not starting?

- Check if port 8000 is available
- Verify Python and dependencies are installed
- Check for errors in terminal

### Frontend not connecting?

- Ensure backend is running on `http://localhost:8000`
- Check browser console for CORS errors
- Verify API_BASE_URL in index.html (line 670)

### Data not saving?

- Check if data.json is writable
- Verify backend logs for errors
- Ensure proper JSON structure

## Development

### Modifying the Password

Edit `index.html` line 540:

```javascript
const APP_PASSWORD = 'your-new-password';
```

### Changing API Port

In `main.py` line 337, modify:

```python
uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

In `index.html` line 670, update:

```javascript
const API_BASE_URL = 'http://localhost:YOUR_PORT';
```

## Tech Stack

- **Backend**: FastAPI, Python 3.13+, Pydantic, Uvicorn
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Storage**: JSON file-based storage
- **API**: RESTful API with full CRUD operations

## License

MIT License - Feel free to use and modify as needed.
