# messages.py
import importlib

LANG_MAP = {
    'ko': {
        'label': '한국어',
        'module': 'messages_ko'
    },
    'en': {
        'label': 'English',
        'module': 'messages_en'
    },
}

def get_message(lang_code, key, *args):
    """지정된 언어 코드와 키에 해당하는 메시지를 반환합니다."""
    
    if lang_code in LANG_MAP:
        try:
            messages_module = importlib.import_module(LANG_MAP[lang_code]['module'])
            messages = messages_module.MESSAGES
            msg = messages.get(key, f"Translation missing for key: {key}")
            return msg.format(*args)
        except (ImportError, KeyError):
            return f"Error loading messages for language: {lang_code}"
    else:
        return f"Unsupported language code: {lang_code}"

def get_language_options():
    """지원하는 언어 옵션을 반환합니다."""
    return {code: data['label'] for code, data in LANG_MAP.items()}
    
