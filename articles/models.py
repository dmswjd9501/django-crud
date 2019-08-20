from django.db import models

# Create your models here.
# 1. 모델(스키마) 정의
# 데이터베이스 테이블을 정의하고, 
# 각각의 컬럼(필드) 정의
class Article(models.Model):
    # id : integer 자동으로 정의(Primary Key)
    # id = models.AutoField(primary_key=True) -> Integer 값이 자동으로 하나씩 증가(AUTOINCREMENT)
    # Charfield = 필수인자로 max_length 지정
    title = models.CharField(max_length=10)
    content = models.TextField()
    # DatetimeField
    #   auto_now_add : 생성시 자동으로 입력
    #   auto_now : 수정시 자동으로 저장
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} - {self.title}'

# models.py : python 클래스 정의
#           : 모델 설계도
# makemigrations: migration 파일 생성
#           : DB 설계도 작성
# migrate : migration 파일 DB 반영