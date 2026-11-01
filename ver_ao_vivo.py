import asyncio
import ctypes
from playwright.async_api import async_playwright

async def main():
    print("Iniciando navegador com foco na tela...")
    async with async_playwright() as p:
        # Abre diretamente o Google Chrome estável do Windows
        browser = await p.chromium.launch(
            channel="chrome",
            headless=False,
            slow_mo=1200,
            args=["--start-maximized", "--disable-infobars"]
        )
        context = await browser.new_context(no_viewport=True)
        page = await context.new_page()

        print("Navegando para http://localhost:3000...")
        await page.goto("http://localhost:3000", wait_until="networkidle")

        # Tenta trazer a janela do navegador para a frente de todas as outras janelas no Windows
        try:
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            ctypes.windll.user32.ShowWindow(hwnd, 3) # SW_MAXIMIZE
        except Exception:
            pass

        await asyncio.sleep(2)

        print("Movendo e rolando a página ao vivo...")
        for i in range(1, 5):
            await page.evaluate(f"window.scrollBy({{ top: 400, behavior: 'smooth' }});")
            await asyncio.sleep(2)

        print("Indo até a seção de agendamento...")
        await page.locator("#agendamento").scroll_into_view_if_needed()
        await asyncio.sleep(2)

        print("Clicando no campo de nome e digitando...")
        await page.locator("#nome_completo").click()
        await page.locator("#nome_completo").type("JOÃO PEDRO (AO VIVO NA SUA TELA)", delay=100)
        await asyncio.sleep(1)

        print("Digitando telefone...")
        await page.locator("#celular").click()
        await page.locator("#celular").type("(65) 99269-1987", delay=100)
        await asyncio.sleep(1)

        print("Digitando e-mail...")
        await page.locator("#email").click()
        await page.locator("#email").type("joaopedromachadobottan@gmail.com", delay=80)
        await asyncio.sleep(2)

        print("Navegando para o Login do Painel...")
        await page.goto("http://localhost:3000/admin/login", wait_until="networkidle")
        await asyncio.sleep(2)

        print("Preenchendo e-mail de login...")
        await page.locator("#usuario").fill("eduardacamargo77@hotmail.com")
        await asyncio.sleep(1)

        print("Preenchendo senha de login...")
        await page.locator("#senha").fill("Duda777")
        await asyncio.sleep(1.5)

        print("Clicando em Entrar...")
        await page.click("button[type='submit']")
        await page.wait_for_url("**/admin/reservas*")
        await asyncio.sleep(5)

        print("Concluído! A janela permanecerá aberta por 10 segundos para você ver.")
        await asyncio.sleep(10)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
