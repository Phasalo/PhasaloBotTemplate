from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, CurrentPage, Row, StubScroll
from aiogram_dialog.widgets.text import Const, Format

from phrases import PHRASES_RU

SCROLL_ID = 'scroll_no_pager'


async def _noop(_callback, _button, _manager: DialogManager):
    pass


async def go_to_first(_callback, _button, manager: DialogManager):
    if scroll := manager.find(SCROLL_ID):
        await scroll.set_page(0)


async def go_to_prev(_callback, _button, manager: DialogManager):
    if scroll := manager.find(SCROLL_ID):
        await scroll.set_page(await scroll.get_page() - 1)


async def go_to_next(_callback, _button, manager: DialogManager):
    if scroll := manager.find(SCROLL_ID):
        await scroll.set_page(await scroll.get_page() + 1)


async def go_to_last(_callback, _button, manager: DialogManager):
    total_pages = manager.dialog_data.get('total_pages', 1)
    if scroll := manager.find(SCROLL_ID):
        await scroll.set_page(total_pages - 1)


async def current_page(dialog_manager: DialogManager) -> int:
    scroll = dialog_manager.find(SCROLL_ID)
    return (await scroll.get_page() + 1) if scroll else 1


def build_pagination_data(dialog_manager: DialogManager, total_pages: int, has_prev: bool, has_next: bool) -> dict:
    dialog_manager.dialog_data['total_pages'] = total_pages
    return {
        'pages_count': total_pages,
        'multipage': total_pages > 1,
        'is_first': not has_prev,
        'is_last': not has_next,
        'not_first': has_prev,
        'not_last': has_next,
    }


def pagination_scroll() -> StubScroll:
    return StubScroll(id=SCROLL_ID, pages='pages_count')


def pagination_row() -> Row:
    return Row(
        Button(Format(f'{PHRASES_RU.button.first_page} 1'), id='first', on_click=go_to_first, when='not_first'),
        Button(Const(' '), id='first_ph', on_click=_noop, when='is_first'),
        Button(Format(PHRASES_RU.button.prev_page), id='prev', on_click=go_to_prev, when='not_first'),
        Button(Const(' '), id='prev_ph', on_click=_noop, when='is_first'),
        CurrentPage(scroll=SCROLL_ID, text=Format('{current_page1}')),
        Button(Format(PHRASES_RU.button.next_page), id='next', on_click=go_to_next, when='not_last'),
        Button(Const(' '), id='next_ph', on_click=_noop, when='is_last'),
        Button(Format('{pages_count} ' + PHRASES_RU.button.last_page), id='last', on_click=go_to_last, when='not_last'),
        Button(Const(' '), id='last_ph', on_click=_noop, when='is_last'),
        when='multipage',
    )
