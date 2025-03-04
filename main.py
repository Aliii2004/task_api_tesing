from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List


app = FastAPI()

class Student(BaseModel):
    id: int = Field(..., description="Unique identifier for the student")
    name: str = Field(..., min_length=2, max_length=50, description="Student's full name")
    email: str = Field(..., description="Student's email address")
    tests_taken: List[int] = ()

class Test(BaseModel):
    id: int = Field(..., description="Unique identifier for the test")
    name: str = Field(..., min_length=2, max_length=100, description="Name of the test")
    max_score: int = Field(..., description="Maximum possible score")

class TestResult(BaseModel):
    student_id: int = Field(..., description="ID of the student taking the test")
    test_id: int = Field(..., description="ID of the test taken")
    score: int = Field(..., description="Score obtained in the test")

class ResponseMessage(BaseModel):
    message: str

db = {
    "students": {
        1: {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "tests_taken": []
        },
        2: {
            "id": 2,
            "name": "Joe",
            "email": "joe@example.com",
            "tests_taken": []
        }
    },
    "tests": {
        1: {
            "id": 1,
            "name": "Math",
            "max_score": 100
        },
        2: {
            "id": 2,
            "name": "Math Quiz",
            "max_score": 100
        }

    },
    "results": [
        {
            "student_id": 1,
            "test_id": 1,
            "score": 90
        },
        {
            "student_id": 1,
            "test_id": 2,
            "score": 95
        },
{
            "student_id": 2,
            "test_id": 2,
            "score": 90
        }

    ]
}

#1
@app.post("/students/", response_model=ResponseMessage, tags=["students"])
async def create_student(student: Student):
    if student.id in db["students"]:
        raise HTTPException(status_code=400, detail="Student already exists")

    db["students"][student.id] = student
    return ResponseMessage(message="Student created successfully")

#2
@app.get("/students/{student_id}", response_model=Student, tags=["students"])
async def get_student(student_id: int):
    if student_id not in db["students"]:
        raise HTTPException(status_code=404, detail="Student does not exist")
    return db["students"][student_id]

#3
@app.get("/students/", response_model=List[Student], tags=["students"])
async def get_students():
    if len(db["students"]) == 0:
        raise HTTPException(status_code=404, detail="Student does not exist")
    return db["students"].values()

#4
@app.post("/tests/", response_model=ResponseMessage, tags=["tests"])
async def create_test(test: Test):
    if test.id in db["tests"]:
        raise HTTPException(status_code=400, detail="Test already exists")
    db["tests"][test.id] = test
    return ResponseMessage(message="Test created successfully")

#5
@app.get("/tests/{test_id}", response_model=Test, tags=["tests"])
async def get_test(test_id: int):
    if len(db["tests"][test_id]) == 0:
        raise HTTPException(status_code=404, detail="Test does not exist")
    if test_id not in db["tests"]:
        raise HTTPException(status_code=400, detail="Test does not exist")
    return db["tests"][test_id]

#6
@app.get("/tests/", response_model=List[Test], tags=["tests"])
async def get_tests():
    if len(db["tests"]) == 0:
        raise HTTPException(status_code=404, detail="Test does not exist")
    return db["tests"].values()

#7
@app.post("/results/", response_model=ResponseMessage, tags=["results"])
async def create_result(result: TestResult):
    if result.student_id in db["results"] and result.test_id in db["results"]:
        raise HTTPException(status_code=400, detail="Result already exists")
    db["results"] = result
    return ResponseMessage(message="Result created successfully")

#8
@app.get("/results/students/{student_id}/", response_model=List[TestResult], tags=["results"])
async def get_result_students(student_id: int):
    if len(db["results"][student_id]) == 0:
        raise HTTPException(status_code=404, detail="Result does not exist")
    results_of_student = []
    for i in db["results"]:
        if i["student_id"] == student_id:
            results_of_student.append(i)
    if len(results_of_student) == 0:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")
    return results_of_student




#9
@app.get("/results/test/{test_id}/", response_model=List[TestResult], tags=["results"])
async def get_result_test(test_id: int):
    if len(db["results"][test_id]) == 0:
        raise HTTPException(status_code=404, detail=f"Result does not exist")
    results_of_specific_test = []
    for i in db["results"]:
        if i["test_id"] == test_id:
            results_of_specific_test.append(i)
    if len(results_of_specific_test) == 0:
        raise HTTPException(status_code=404, detail=f"Test with ID {test_id} not found")
    return results_of_specific_test

#10
@app.get("/results/test/{test_id}/average", response_model=dict[str, float], tags=["results"])
async def get_result_average(test_id: int):
    average_score = -1
    count_of_tests = 0
    if test_id not in db["results"]:
        raise HTTPException(status_code=404, detail=f"Test with ID {test_id} not found")
    for i in db["results"]:
        if i["test_id"] == test_id:
            average_score += i["score"]
            count_of_tests += 1
    average_score /= count_of_tests
    if average_score < 0:
        raise HTTPException(status_code=404, detail=f"Test with ID {test_id} not found")
    return {"Average score": average_score}


#11
@app.get("/results/test/{test_id}/highest", response_model=dict[str, int], tags=["results"])
async def get_result_highest(test_id: int):
    if test_id not in db["results"]:
        raise HTTPException(status_code=404, detail=f"Test with ID {test_id} not found")
    highest_score = -1
    for i in db["results"]:
        if i["test_id"] == test_id:
            highest_score = max(int(highest_score), int(i["score"]))
    if highest_score < 0:
        raise HTTPException(status_code=404, detail=f"Test with ID {test_id} not found")
    return {"Highest score": highest_score}

#12
@app.get("/students/{student_id}/", response_model=ResponseMessage, tags=["students"])
async def delete_student(student_id: int):
    if student_id not in db["students"]:
        raise HTTPException(status_code=404, detail="Student does not exist")
    del db["students"][student_id]
    db["results"] = [result for result in db["results"] if result["student_id"] != student_id]
    return ResponseMessage(message="Student deleted successfully")