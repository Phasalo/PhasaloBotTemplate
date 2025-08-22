from typing import List, Optional
from DB.models import UserModel, QueryModel
from phrases import PHRASES_RU
from DB.models import Pagination
from utils import format_string


def format_user_list(users_info: List[UserModel], pagination: Pagination) -> str:
    txt = [PHRASES_RU.title.users,
           PHRASES_RU.replace('footnote.total', total=pagination.total_items)]

    for user in users_info:
        line_data = {
            'username': f'@{user.username}' if user.username else user.first_name or PHRASES_RU.icon.not_username,
            'user_id': str(user.user_id).ljust(12),
            'query_stat': f'{format_string.get_query_count_emoji(user.query_count)} {user.query_count}',
            'registration_date': user.registration_date.strftime('%d.%m.%Y')
        }

        user_line = PHRASES_RU.replace('template.user', **line_data)

        if user.is_banned:
            txt.append(f'<s>{user_line}</s>')
        elif user.is_admin:
            txt.append(f'<b>{user_line}</b>')
        else:
            txt.append(user_line)

    if pagination.total_pages > 1:
        txt.append(PHRASES_RU.icon.row_placeholder * (pagination.per_page - len(users_info)))

    return ''.join(txt)


def format_queries_text(
        queries: List[QueryModel],
        name: Optional[str] = None,
        user_id: Optional[int] = None,
        footnote_template: str = PHRASES_RU.footnote.user_query,
        line_template: str = PHRASES_RU.template.user_query
) -> str:
    """
    Форматирует список запросов в текстовое сообщение.

    Args:
        queries: Список объектов QueryModel
        name: Юзернейм или имя пользователя (если есть)
        user_id: ID пользователя (если предыдущий аргумент None)
        footnote_template: Шаблон заголовка с {username} placeholder
        line_template: Шаблон строки запроса с {time} и {query} placeholders

    Returns:
        Отформатированная строка с историей запросов
    """
    username_display = name or user_id or PHRASES_RU.error.unknown
    txt = [PHRASES_RU.title.query,
           footnote_template.format(username=username_display, user_id=user_id)]

    for query in queries:
        line_data = {
            'user_id': query.user.user_id,
            'time': query.query_date.strftime('%d.%m.%Y %H:%M:%S') if query.query_date else PHRASES_RU.error.unknown,
            'query': query.query_text,
            'username': f'@{query.user.username}' if query.user and query.user.username else query.user.first_name if query.user else ''
        }
        txt.append(line_template.format(**line_data))

    return ''.join(txt)
