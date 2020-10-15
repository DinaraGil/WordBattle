import wikipediaapi

wiki = wikipediaapi.Wikipedia('ru')

page = wiki.page(input())

if page.exists():
    print(page.summary)
