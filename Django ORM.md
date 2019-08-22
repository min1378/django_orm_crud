# Django ORM

## Create

#### 기초설정

- Shell

  ```bash
  $ python manage.py shell
  ```

- import model

  ```python
  from articles.models import Article
  ```



#### 데이터를 저장하는 3가지 방법

1. 첫번째 방식

   - ORM을 쓰는 이유? => DB를 조작하는 것을 객체지향 프로그래밍(클래스)처럼 하기 위해서

     ```shell
     >>> Article.objects.all()
     <QuerySet [<Article: Article object (1)>]>
     
     >>> article = Article()
     >>> article
     <Article: Article object (None)>
     
     >>> article.title = 'First article'
     >>> article.content = 'Hello, article?'
     >>> article.title
     'First article'
     
     >>> article.content
     'Hello, article?'
     
     >>> article.save()
     >>> Article.objects.all()
     <QuerySet [<Article: Article object (1)>]>
     ```

2. 두번째 방식

   - 함수에서 `keyword` 넘기기 방식과 동일

     ```shell
     >>> article = Article(title='second article', content='hihi')
     >>> article.save()
     >>> Article.objects.all()
     <QuerySet [<Article: Article object (1)>, <Article: Article object (2)>]>
     
     >>> article
     <Article: Article object (2)>
     ```

3. 세번째 방식

   - `create()`를 사용하면 쿼리셋 객체를 생성하고 저장하는 로직이 한번의 스텝

     ```shell
     >>> Article.objects.create(title='third', content='django')
     <Article: Article object (3)>
     
     >>> article
     <Article: Article object (2)>
     
     >>> Article.objects.all()
     <QuerySet [<Article: Article object (1)>, <Article: Article object (2)>, <Article: Article object (3)>]>
     ```

4. 검증

   - `full_clean()`함수를 통해 저장하기 전 데이터 검증을 할 수 있다.

     ```python
     >>> article = Article()
     >>> article.title = 'Pythono is good'
     >>> article.full_clean()
     Traceback (most recent call last):
       File "<console>", line 1, in <module>
       File "C:\Users\student\development\django\django_orm_crud\venv\lib\site-packages\django\db\models\base.py", line 1203, in full_clean
         raise ValidationError(errors)
     django.core.exceptions.ValidationError: {'content': ['이 필드는 빈 칸으로 둘 수 없습니다.']}
     ```





--------------------------------------

## READ

#### 모든 객체

- 기본방법

    ```shell
    >>> Article.objects.all()
    <QuerySet [<Article: Article object (1)>, <Article: Article object (2)>, <Article: Article object (3)>]>
    ```

  

#### 객체표현 변경

- python

    ```python
    class Article(models.Model):
        ...
        
        def __str__(self):
            return f'{self.id}번 글 - {self.title} : {self.content}'
    ```
    


- shell

    ```shell
    >>> from articles.models import Article
    >>> Article.objects.all()
    <QuerySet [<Article: 1번 글 - First article : Hello, article?>, <Article: 2번 글 - second article : hihi>, <Article: 3번 글 - third : django>]>
    ```



#### DB에 저장된 글 중에서 title이 Second인 글만 가져오기

- title로 가져오기

    ```shell
    >>> Article.objects.filter(title='second article')
    <QuerySet [<Article: 2번 글 - second article : hihi>]>
    
    
    (중복일 때)
    >>> Article.objects.filter(title='second article')
    <QuerySet [<Article: 2번 글 - second article : hihi>, <Article: 4번 글 - second article : hihihi>]>
    ```

- title이 중복될 때 그 중에 첫 번째 글만 가져오기

  ```shell
  >>> querySet = Article.objects.filter(title='second article')
  >>> querySet
  <QuerySet [<Article: 2번 글 - second article : hihi>, <Article: 4번 글 - second article : hihihi>]>
  
  >>> querySet.first()
  <Article: 2번 글 - second article : hihi>
  
  
  (chaining)
  >>> Article.objects.filter(title='second article').first()
  <Article: 2번 글 - second article : hihi>
  ```



#### DB에 저장된 글 중에서 pk가 1인 글만 가져오기

- pk만 `get()`으로 가져올 수 있다.

  ```shell
  >>> Article.objects.get(pk=1)  // get은 유일한 값일 때 가져올 수 있음
  <Article: 1번 글 - First article : Hello, article?>
  ```

- `get()`의 오류반환

  ```shell
  >>> Article.objects.get(pk=10)  // 존재하지 않는 값
  Traceback (most recent call last):
    File "<console>", line 1, in <module>
    File "C:\Users\student\development\django\django_orm_crud\venv\lib\site-packages\django\db\models\manager.py", line 82, in manager_method
      return getattr(self.get_queryset(), name)(*args, **kwargs)
    File "C:\Users\student\development\django\django_orm_crud\venv\lib\site-packages\django\db\models\query.py", line 408, in get
      self.model._meta.object_name
  articles.models.Article.DoesNotExist: Article matching query does not exist.
  
  >>> Article.objects.get(title='second article')  // 중복되는 값
  Traceback (most recent call last):
    File "<console>", line 1, in <module>
    File "C:\Users\student\development\django\django_orm_crud\venv\lib\site-packages\django\db\models\manager.py", line 82, in manager_method
      return getattr(self.get_queryset(), name)(*args, **kwargs)
    File "C:\Users\student\development\django\django_orm_crud\venv\lib\site-packages\django\db\models\query.py", line 412, in get
      (self.model._meta.object_name, num)
  articles.models.Article.MultipleObjectsReturned: get() returned more than one Article -- it returned 2!
  
  // filter의 경우 오류를 반환하지 않음
  >>> Article.objects.filter(pk=10)
  <QuerySet []>
  ```




#### 데이터에 접근하는 기타 방법들

- 오름차순

  ```shell
  >>> articles = Article.objects.order_by('pk')
  >>> articles
  <QuerySet [<Article: 1번 글 - First article : Hello, article?>, <Article: 2번 글 - second article : hihi>, <Article: 3번 글 - third : django>, <Article: 4번 글 - second article : hihihi>]>
  ```

- 내림차순

  ```shell
  >>> articles = Article.objects.order_by('-pk')
  >>> articles
  <QuerySet [<Article: 4번 글 - second article : hihihi>, <Article: 3번 글 - third : django>, <Article: 2번 글 - second article : hihi>, <Article: 1번 글 - First article : Hello, article?>]>
  ```

- 인덱스 접근 가능

  ```shell
  (오름차순, 내림차순 정렬 후)
  >>> article = articles[2]
  >>> article
  <Article: 2번 글 - second article : hihi>
  
  >>> articles = Article.objects.all()[1:3]
  >>> articles
  <QuerySet [<Article: 2번 글 - second article : hihi>, <Article: 3번 글 - third : django>]>
  ```

- LIKE - 문자열을 포함하고 있는 값을 가지고 옴

  (장고 ORM은 이름(title)과 필터(contains)를 더블 언더스코어로 구분함)

  ```shell
  >>> articles = Article.objects.filter(title__contains='sec')
  >>> articles
  <QuerySet [<Article: 2번 글 - second article : hihi>, <Article: 4번 글 - second article : hihihi>]>
  ```

- startswith

  ```shell
  >>> articles = Article.objects.filter(title__startswith='First')
  >>> articles
  <QuerySet [<Article: 1번 글 - First article : Hello, article?>]>
  ```

- endswith

  ```shell
  >>> articles = Article.objects.filter(content__endswith='article?')
  >>> articles
  <QuerySet [<Article: 1번 글 - First article : Hello, article?>]>
  ```





-------------------------

## Delete

- 인스턴스 생성 후 `delete()`함수 실행

  ```shell
  >>> article = Article.objects.get(pk=2)
  >>> article.delete()
  (1, {'articles.Article': 1})
  ```





--------------------------------------------

## Update

- 인스턴스 호출 후 값 변경하여 `.save()` 함수 실행

  ```shell
  >>> article = Article.objects.get(pk=4)
  >>> article.content
  'hihihi'
  
  >>> article.content = 'new content'
  >>> article.save()
  >>> article.content
  'new content'
  ```

  

