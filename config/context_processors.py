def lang_from_cookie(request):
    lang = request.COOKIES.get('lang', 'ru')
    if lang not in ('en', 'ru', 'uz'):
        lang = 'ru'
    return {'current_lang': lang}
