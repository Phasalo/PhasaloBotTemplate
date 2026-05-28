from aiogram import Router, types

router = Router()


@router.inline_query()
async def inline_get_photo(query: types.InlineQuery):
    # text = query.query
    # какая-то бизнес-логика, генерирующая result

    #   <-| ----------------- -<phasalo>- ------------------ |->
    #                                                          |
    #   какая-то бизнес-логика, генерирующая result            | <=| PHASALO<|||
    #                                                          |
    #   <-| ----------------- -<phasalo>- ------------------ |->

    # await query.answer(result, cache_time=1, is_personal=True)
    pass
