from fastapi import FastAPI, HTTPException
import boto3
from pydantic import BaseModel
import uuid

# Initialize FastAPI
app = FastAPI()

# Connect to DynamoDB
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

# Create tables if not exist (Run this manually in AWS Console if needed)
teacher_table = dynamodb.Table("Teachers")
student_table = dynamodb.Table("Students")


# Models for API requests
class TeacherCreate(BaseModel):
    email: str
    name: str
    license_count: int


class StudentCreate(BaseModel):
    teacher_id: str
    email: str
    name: str


class ProgressUpdate(BaseModel):
    student_id: str
    progress: dict  # Example: {"course1": "50%", "course2": "Completed"}


@app.post("/register-teacher")
def register_teacher(teacher: TeacherCreate):
    teacher_id = str(uuid.uuid4())

    teacher_table.put_item(
        Item={
            "teacher_id": teacher_id,
            "email": teacher.email,
            "name": teacher.name,
            "license_count": teacher.license_count,
        }
    )
    return {"message": "Teacher registered", "teacher_id": teacher_id}


@app.post("/add-student")
def add_student(student: StudentCreate):
    # Check if teacher exists
    response = teacher_table.get_item(Key={"teacher_id": student.teacher_id})
    if "Item" not in response:
        raise HTTPException(status_code=404, detail="Teacher not found")

    student_id = str(uuid.uuid4())

    student_table.put_item(
        Item={
            "student_id": student_id,
            "teacher_id": student.teacher_id,
            "email": student.email,
            "name": student.name,
            "progress": {},
        }
    )
    return {"message": "Student added", "student_id": student_id}


@app.get("/get-students/{teacher_id}")
def get_students(teacher_id: str):
    response = student_table.scan(
        FilterExpression="teacher_id = :t",
        ExpressionAttributeValues={":t": teacher_id},
    )
    return response.get("Items", [])


@app.get("/get-progress/{student_id}")
def get_progress(student_id: str):
    response = student_table.get_item(Key={"student_id": student_id})
    if "Item" not in response:
        raise HTTPException(status_code=404, detail="Student not found")

    return response["Item"]["progress"]


@app.put("/update-progress")
def update_progress(progress: ProgressUpdate):
    student_table.update_item(
        Key={"student_id": progress.student_id},
        UpdateExpression="SET progress = :p",
        ExpressionAttributeValues={":p": progress.progress},
    )
    return {"message": "Progress updated"}
