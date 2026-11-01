import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome", headless=True)
        page = await browser.new_page()
        print("Navegando para http://localhost:3000...")
        await page.goto("http://localhost:3000", wait_until="networkidle")
        
        # Título da página
        title = await page.title()
        print(f"Título da Página: {title}")
        
        # Captura screenshot da Landing Page
        await page.screenshot(path="d:/IAs/Projetos - IA/Duda/Clínica Estética/Site/screenshot_landing.png", full_page=False)
        print("Screenshot da Landing Page salvo em screenshot_landing.png!")
        
        # Testando navegação até o painel de reservas
        await page.goto("http://localhost:3000/admin/reservas", wait_until="networkidle")
        admin_title = await page.title()
        print(f"Título do Painel Admin: {admin_title}")
        await page.screenshot(path="d:/IAs/Projetos - IA/Duda/Clínica Estética/Site/screenshot_admin.png", full_page=False)
        print("Screenshot do Painel de Reservas salvo em screenshot_admin.png!")
        
        await browser.close()
        print("Teste de automação com Playwright concluído com sucesso!")

if __name__ == "__main__":
    asyncio.run(main())
