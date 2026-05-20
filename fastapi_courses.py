from fastapi import HTTPException, status, FastAPI, APIRouter
from pydantic import BaseModel, RootModel


class CourseIn(BaseModel):
    title: str
    max_score: int
    min_score: int
    description: str

class CourseOut(CourseIn):
    id: int

class CoursesStore(RootModel):
    root: list[CourseOut]

    def find(self, course_id: int) -> CourseOut | None:
        return next(filter(lambda course: course.id == course_id, self.root), None)

    def create(self, course_in: CourseIn) -> CourseOut:
        course = CourseOut(id=len(self.root) +1, **course_in.model_dump())
        self.root = self.root.append(course)
        return course

    def update(self, course_id: int, course_in: CourseIn) -> CourseOut:
        index = next(index for index, course in enumerate(self.root) if course.id == course_id)
        updated = CourseOut(id=course_id, **course_in.model_dump())
        self.root[index] = updated
        return updated

    def delete(self, course_id: int) -> CourseOut | None:
        self.root = [course for course in self.root if course_id != course_id]

store = CoursesStore(root=[])

courses_router = APIRouter(
    prefix="/api/v1/courses",
    tags=["courses-service"]
)

app = FastAPI()

@courses_router.get("/{course_id}", response_model=list[CourseOut])
async def get_course(course_id: int) -> CourseOut:
    if not (course := store.find(course_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course {course_id} not found"
        )
    return course


@courses_router.get("", response_model=list[CourseOut])
async def get_courses():
    return store.root


@courses_router.post("", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
async def create_course(course: CourseIn) -> CourseOut:
    return store.create(course)


@courses_router.put("/{course_id}", response_model=CourseOut)
async def update_course(course: CourseIn) -> CourseOut:
    if not (course := store.find(course.id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course {course.id} not found"
        )
    return store.update(course.id, course)

@courses_router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course: CourseIn):
    if not (course := store.find(course.id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course {course.id} not found"
        )
    store.delete(course.id)

app.include_router(courses_router)

