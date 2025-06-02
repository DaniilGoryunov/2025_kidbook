from gigachat import GigaChat
from langchain_core.prompts import PromptTemplate
from pathlib import Path

# Настройка директории для сохранения файлов
animation_dir = Path("animation_concepts")
animation_dir.mkdir(parents=True, exist_ok=True)

# Список анимационных понятий
concepts = [
    "Мультфильм", "Анимация", "Спрайт", "Рендер", "Раскадровка",
    "Фреймрейт", "Моушн-дизайн", "Скелетная анимация", "Стоп-моушн",
    "Твининг", "Аниматик", "Фоли", "Lip Sync", "CGI", "Анимационный цикл"
]

def create_markdown_file(filename, content):
    """Создает MD-файл с контентом"""
    filepath = animation_dir / f"{filename}.md"
    filepath.write_text(content, encoding="utf-8")
    print(f"Создан файл: {filepath}")

# Инициализация GigaChat
api_code = ''
llm = GigaChat(credentials=api_code, verify_ssl_certs=False, model='GigaChat-Pro')

# Промпт с адаптированными требованиями
template = """
Ты - эксперт по анимации с талантом объяснять сложное детям 10-12 лет. Создай увлекательное объяснение 
понятия из мира анимации, используя:

1. 🔥 Яркие сравнения ("Это как...")
2. 🎬 Примеры из известных мультфильмов
3. 🤹 Интерактивные элементы ("Представь, что...")
4. 💡 Практическое применение
5. 🔗 Перекрестные ссылки на другие понятия

Технические требования:
- Формат: Markdown
- Обязательные разделы:
  ## Определение (с эмодзи)
  ## Как это работает? 
  ## Пример из мультфильма
  ## Попробуй сам! (совет для ребенка)
- Используй минимум 5 эмодзи
- Свяжи с другими понятиями: {linked_concepts}

Понятие: {query}
"""

# Генерация контента для каждого понятия
for concept in concepts:
    # Исключаем текущее понятие из списка ссылок
    linked = [c for c in concepts if c != concept]
    prompt = PromptTemplate(
        input_variables=['query', 'linked_concepts'],
        template=template
    ).format(
        query=concept,
        linked_concepts=", ".join(f'"{c}"' for c in linked)
    )
    
    # Добавляем контекстные примеры для конкретных понятий
    if concept == "Мультфильм":
        prompt += "\nОбязательно упомяни разницу между 2D и 3D, используя примеры [Disney](^2d^) и [Pixar](^3d^)."
    elif concept == "Скелетная анимация":
        prompt += "\nПокажи аналогию с марионеткой, где [кости](^rigging^) - это нитки кукловода."
    
    response = llm.chat(prompt)
    create_markdown_file(concept, response.choices[0].message.content)