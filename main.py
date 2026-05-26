import asyncio
import sys
import random
import time
import uuid
from playwright.async_api import async_playwright

class RealisticBrowserSimulator:
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
        ]
        
    def get_random_cookie_id(self):
        return str(uuid.uuid4())

async def visit_target_site(page, target_url, referer_url, cookie_id):
    """Посещает целевой сайт с реальным выполнением JS"""
    print(f"\n{'='*60}")
    print(f"🎯 ЦЕЛЕВОЙ САЙТ: {target_url}")
    print(f"📎 ПЕРЕХОД С РЕФЕРА: {referer_url}")
    print(f"🍪 Cookie ID: {cookie_id[:8]}...")
    print(f"{'='*60}")
    
    # Устанавливаем заголовки и cookie
    await page.set_extra_http_headers({
        'Referer': referer_url,
        'Cookie': f'_ym_uid={cookie_id}; _ym_d={int(time.time())}'
    })
    
    try:
        # Переход на сайт (ожидаем полной загрузки)
        print(f"  🌐 Загрузка страницы...")
        await page.goto(target_url, wait_until='networkidle', timeout=30000)
        
        # Ждём загрузки Метрики
        print(f"  📊 Ожидание загрузки Яндекс Метрики...")
        await asyncio.sleep(random.uniform(2, 4))
        
        # Имитация прокруток и движений мыши
        view_duration = random.uniform(35, 70)
        scroll_count = random.randint(3, 6)
        scroll_interval = view_duration / scroll_count
        
        print(f"  👁️ Имитация поведения ({view_duration:.0f} сек):")
        
        for i in range(scroll_count):
            # Прокрутка на случайную величину
            scroll_y = random.randint(300, 800)
            await page.evaluate(f"window.scrollTo(0, {scroll_y})")
            print(f"    📜 Прокрутка {i+1}/{scroll_count}: {scroll_y}px")
            
            # Движение мыши по случайным элементам
            try:
                # Находим случайные элементы и наводим мышь
                elements = await page.query_selector_all('a, button, div, span')
                if elements and len(elements) > 10:
                    random_element = random.choice(elements[10:min(30, len(elements))])
                    await random_element.hover()
                    print(f"    🖱️ Наведение на элемент")
            except:
                pass
            
            # Ожидание между действиями
            await asyncio.sleep(scroll_interval)
        
        # Финальная прокрутка вверх
        await page.evaluate("window.scrollTo(0, 0)")
        await asyncio.sleep(random.uniform(1, 3))
        
        print(f"  ✅ Целевой сайт успешно просмотрен")
        return True
        
    except Exception as e:
        print(f"  ❌ Ошибка: {e}")
        return False

async def visit_referer_site(page, referer_url):
    """Посещает сайт-рефер"""
    print(f"\n{'='*60}")
    print(f"🔗 САЙТ-РЕФЕР: {referer_url}")
    print(f"{'='*60}")
    
    try:
        await page.goto(referer_url, wait_until='networkidle', timeout=30000)
        print(f"  ✅ Рефер загружен")
        
        # Небольшая имитация на рефере
        await page.evaluate("window.scrollTo(0, 500)")
        await asyncio.sleep(random.uniform(3, 7))
        await page.evaluate("window.scrollTo(0, 100)")
        await asyncio.sleep(random.uniform(2, 4))
        
        print(f"  ✅ Рефер просмотрен")
        return True
    except Exception as e:
        print(f"  ❌ Ошибка рефера: {e}")
        return False

def load_referers(filename='referers.txt'):
    referers = []
    import os
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if not line.startswith(('http://', 'https://')):
                        line = 'https://' + line
                    referers.append(line)
        print(f"📁 Загружено {len(referers)} реферов")
    return referers

async def main():
    # Проверка аргументов
    if len(sys.argv) < 3 or sys.argv[1] != "-u":
        print("\nИСПОЛЬЗОВАНИЕ: python main.py -u <ВАШ_САЙТ>")
        print("ПРИМЕР: python main.py -u https://example.com")
        print("\nФАЙЛ referers.txt: список сайтов-реферов")
        return
    
    target_url = sys.argv[2].rstrip('/')
    referers = load_referers('referers.txt')
    
    if not referers:
        print("❌ Создайте файл referers.txt со списком реферов")
        return
    
    cookie_id = str(uuid.uuid4())
    
    print(f"\n🤖 ЗАПУСК БРАУЗЕРНОГО БОТА")
    print(f"🎯 Цель: {target_url}")
    print(f"🍪 Cookie ID: {cookie_id[:8]}...")
    print(f"📁 Реферов: {len(referers)}")
    
    async with async_playwright() as p:
        # Запуск браузера в headless-режиме для сервера
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent=random.choice(RealisticBrowserSimulator().user_agents)
        )
        page = await context.new_page()
        
        successful = 0
        
        for i, referer in enumerate(referers, 1):
            print(f"\n{'🔄'*30}")
            print(f"📌 РЕФЕР #{i}: {referer}")
            
            # Посещение рефера
            if await visit_referer_site(page, referer):
                await asyncio.sleep(random.uniform(2, 4))
                
                # Переход на целевой сайт
                if await visit_target_site(page, target_url, referer, cookie_id):
                    successful += 1
            
            # Пауза между реферами
            if i < len(referers):
                pause = random.uniform(5, 10)
                print(f"\n⏸️ Пауза {pause:.0f} сек...")
                await asyncio.sleep(pause)
        
        await browser.close()
        
        print(f"\n✅ РАБОТА ЗАВЕРШЕНА")
        print(f"📊 Успешных переходов: {successful}/{len(referers)}")

if __name__ == "__main__":
    asyncio.run(main())