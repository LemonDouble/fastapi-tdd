# fastapi-tdd

Udemy의 [Try FastAPI Test Driven Development 2024](https://www.udemy.com/course/try-fastapi-api-test-driven-development/) 강의 들으면서 따라해보는 레포지토리

### Albemic으로 Database Migration 하는 법

#### Migration 생성
```
alembic -n devdb revision --autogenerate -m "마이그레이션명"
```

#### 최신 버전으로 업데이트
```
alembic -n devdb upgrade head
```