from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Any
import json
import os
from pathlib import Path
import uuid

app = FastAPI(title="Meeting API", version="1.0.0")

# CORS configuration - allows all origins like the PHP version
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data file path
DATA_FILE = Path(__file__).parent / "data.json"

# Pydantic models for request/response validation
class Meeting(BaseModel):
    """Individual meeting data structure"""
    id: Optional[str] = None
    title: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    participants: Optional[List[str]] = None
    agenda: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        extra = "allow"  # Allow additional fields


class MeetingCreate(BaseModel):
    """Model for creating a new meeting (without ID)"""
    title: str
    date: Optional[str] = None
    time: Optional[str] = None
    participants: Optional[List[str]] = None
    agenda: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        extra = "allow"


class MeetingUpdate(BaseModel):
    """Model for updating an existing meeting (all fields optional)"""
    title: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    participants: Optional[List[str]] = None
    agenda: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        extra = "allow"


class MeetingsData(BaseModel):
    """Main data structure containing all meetings"""
    meetings: List[dict]


class SuccessResponse(BaseModel):
    """Success response model"""
    success: bool
    message: str
    data: Optional[Any] = None


def ensure_data_file():
    """Ensure the data file exists with initial structure"""
    if not DATA_FILE.exists():
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump({"meetings": []}, f, indent=2)


def read_data() -> dict:
    """Read data from the JSON file"""
    ensure_data_file()
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content.strip():
                return {"meetings": []}
            return json.loads(content)
    except json.JSONDecodeError:
        return {"meetings": []}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to read data: {str(e)}"
        )


def write_data(data: dict) -> bool:
    """Write data to the JSON file"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to write data: {str(e)}"
        )


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": "Meeting API with Full CRUD Operations",
        "version": "2.0.0",
        "endpoints": {
            "GET /api/meetings": "Get all meetings",
            "POST /api/meetings": "Create a new meeting",
            "GET /api/meetings/{meeting_id}": "Get a specific meeting",
            "PUT /api/meetings/{meeting_id}": "Update a meeting",
            "DELETE /api/meetings/{meeting_id}": "Delete a meeting",
            "POST /api/meetings/bulk": "Save all meetings data (bulk)",
            "GET /health": "Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Meeting API"}


# ==================== CRUD OPERATIONS ====================

@app.get("/api/meetings", response_model=MeetingsData)
async def get_all_meetings():
    """
    GET - Read all meetings

    Returns the complete meetings data structure from data.json
    """
    data = read_data()
    return data


@app.post("/api/meetings", response_model=SuccessResponse)
async def create_meeting(meeting: MeetingCreate):
    """
    CREATE - Create a new meeting

    Automatically generates a unique ID for the new meeting
    """
    try:
        # Read current data
        data = read_data()

        # Generate unique ID
        meeting_id = str(uuid.uuid4())

        # Create meeting dict with ID
        new_meeting = meeting.model_dump()
        new_meeting['id'] = meeting_id

        # Add to meetings array
        data['meetings'].append(new_meeting)

        # Write to file
        write_data(data)

        return SuccessResponse(
            success=True,
            message="Meeting created successfully",
            data=new_meeting
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create meeting: {str(e)}"
        )


@app.get("/api/meetings/{meeting_id}")
async def get_meeting_by_id(meeting_id: str):
    """
    READ - Get a specific meeting by ID

    Returns a single meeting matching the provided ID
    """
    data = read_data()

    # Find meeting by ID
    for meeting in data['meetings']:
        if meeting.get('id') == meeting_id:
            return meeting

    # Meeting not found
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Meeting with ID '{meeting_id}' not found"
    )


@app.put("/api/meetings/{meeting_id}", response_model=SuccessResponse)
async def update_meeting(meeting_id: str, meeting_update: MeetingUpdate):
    """
    UPDATE - Update an existing meeting

    Updates only the fields provided in the request body
    """
    try:
        data = read_data()

        # Find and update meeting
        meeting_found = False
        for i, meeting in enumerate(data['meetings']):
            if meeting.get('id') == meeting_id:
                meeting_found = True

                # Update only provided fields
                update_data = meeting_update.model_dump(exclude_unset=True)
                data['meetings'][i].update(update_data)

                # Write to file
                write_data(data)

                return SuccessResponse(
                    success=True,
                    message="Meeting updated successfully",
                    data=data['meetings'][i]
                )

        # Meeting not found
        if not meeting_found:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Meeting with ID '{meeting_id}' not found"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update meeting: {str(e)}"
        )


@app.delete("/api/meetings/{meeting_id}", response_model=SuccessResponse)
async def delete_meeting(meeting_id: str):
    """
    DELETE - Delete a meeting

    Removes the meeting with the specified ID from data.json
    """
    try:
        data = read_data()

        # Find and delete meeting
        initial_length = len(data['meetings'])
        data['meetings'] = [m for m in data['meetings'] if m.get('id') != meeting_id]

        # Check if meeting was found and deleted
        if len(data['meetings']) == initial_length:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Meeting with ID '{meeting_id}' not found"
            )

        # Write to file
        write_data(data)

        return SuccessResponse(
            success=True,
            message="Meeting deleted successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete meeting: {str(e)}"
        )


# ==================== BULK OPERATIONS ====================

@app.post("/api/meetings/bulk", response_model=SuccessResponse)
async def save_all_meetings(data: MeetingsData):
    """
    BULK SAVE - Replace all meetings data

    Accepts a JSON object with a 'meetings' array and replaces all data in data.json
    (For backwards compatibility with the old PHP endpoint)
    """
    try:
        # Validate that meetings key exists
        if not hasattr(data, 'meetings'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JSON data: 'meetings' key required"
            )

        # Convert Pydantic model to dict
        data_dict = data.model_dump()

        # Write to file
        write_data(data_dict)

        return SuccessResponse(
            success=True,
            message="All meetings data saved successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save data: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    # Initialize data file
    ensure_data_file()
    # Run the server
    uvicorn.run("main:app", host="0.0.0.0", port=5051, reload=True)
