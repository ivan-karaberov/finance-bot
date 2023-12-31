from typing import List, NamedTuple

import db


class Category(NamedTuple):
    """Структура категории"""
    codename: str
    name: str
    is_base_expense: bool
    aliases: List[str]


class Categories:
    async def _load_categories(self) -> List[Category]:
        """Возвращает справочник категорий из БД"""
        categories = await db.fetch_all(
            """SELECT codename, name, is_base_expense, aliases FROM category"""
        )
        categories = self._fill_aliases(categories)
        return categories

    def _fill_aliases(self, categories: List[Category]) -> List[Category]:
        """Заполняет aliases для каждой категории"""
        categories_result = []
        for category in categories:
            aliases = category["aliases"].split(",")
            aliases = list(filter(None, map(str.strip, aliases)))
            aliases.append(category["codename"])
            aliases.append(category["name"])
            categories_result.append(
                Category(
                    codename=category['codename'],
                    name=category['name'],
                    is_base_expense=category['is_base_expense'],
                    aliases=aliases
                )
            )
        return categories_result

    async def get_category(self, category_name: str) -> Category:
        """Возвращает категорию по назаванию категории"""
        finded = None
        other_category = None
        categories = await self._load_categories()

        for category in categories:
            if category.codename == 'other':
                other_category = category
            for alias in category.aliases:
                if category_name == alias:
                    finded = category
                    break

        if not finded:
            finded = other_category

        return finded
