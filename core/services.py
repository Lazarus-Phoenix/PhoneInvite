import random
import time
from django.core.cache import cache

def send_verification_code(phone):
    # Имитация отправки кода с задержкой
    code = str(random.randint(1000, 9999))
    cache.set(f'verification_code_{phone}', code, timeout=300)  # 5 минут
    time.sleep(random.uniform(1, 2))
    return code

def verify_code(phone, code):
    cached_code = cache.get(f'verification_code_{phone}')
    return cached_code == code
