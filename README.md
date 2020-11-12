<h1>To start project:</h1>
(used python3.9)
<ul>
  <li>Install&Run redis</li>
  <li>Init project (make init)</li>
  <li>Start project ("make dev" or "make start_daphne")</li>
</ul>
<hr>
<h1>Тренировка</h1>
Для трениовок используются вопросы из общей базы, имеющие параметры:
<ul>
  <li>premoderate=False</li>
  <li>public=True</li>
</ul>
И выбранные по шаблону для текущей лиги, взятой из профиля. (Для анонимных пользователей - дефолтная лига: 'Z (знаток)')
Шаблон:

```python
def get_template_questions(u):
  u = u.split(' ')[0]
  if u == 'J':
      return 10, 10, 10, 10, 20, 20, 20, 20, 30, 30, 30, 30,
  if u == 'L':
      return 10, 10, 10, 20, 20, 20, 30, 30, 30, 40, 40, 50,
  if u == 'Z':
      return 10, 10, 20, 20, 20, 30, 30, 30, 40, 40, 50, 50,
  if u == 'M':
      return 20, 20, 20, 30, 30, 30, 30, 40, 40, 40, 50, 50,
  if u == 'P':
      return 30, 30, 30, 30, 40, 40, 40, 40, 50, 50, 50, 50,
```

