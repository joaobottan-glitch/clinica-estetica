import asyncio
from playwright.async_api import async_playwright

async def main():
    print("\n" + "="*60)
    print(" 🚀 INICIANDO DEMONSTRAÇÃO VISUAL AO VIVO NO NAVEGADOR")
    print("="*60 + "\n")

    async with async_playwright() as p:
        # headless=False abre a janela física do navegador na tela do usuário
        # slow_mo=1000 adiciona delay entre cada ação para visualização perfeita
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        
        # Cria contexto com janela ampla
        context = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await context.new_page()

        print("1. Abrindo a Landing Page da Estética Duda (http://localhost:3000)...")
        await page.goto("http://localhost:3000", wait_until="networkidle")
        await asyncio.sleep(2)

        print("2. Rolando pela página para você acompanhar o design...")
        await page.evaluate("window.scrollBy({ top: 500, behavior: 'smooth' });")
        await asyncio.sleep(2)

        print("3. Visualizando a seção de procedimentos...")
        await page.evaluate("window.scrollBy({ top: 600, behavior: 'smooth' });")
        await asyncio.sleep(2)

        print("4. Visualizando horários de funcionamento em Nova Mutum...")
        await page.evaluate("window.scrollBy({ top: 700, behavior: 'smooth' });")
        await asyncio.sleep(2)

        print("5. Indo até a seção do Formulário de Reserva...")
        await page.locator("#agendamento").scroll_into_view_if_needed()
        await asyncio.sleep(1.5)

        print("6. Preenchendo o Nome Completo...")
        await page.locator("#nome_completo").click()
        await page.locator("#nome_completo").type("JOÃO PEDRO MACHADO BOTTAN", delay=70)
        await asyncio.sleep(0.5)

        print("7. Preenchendo o Celular com DDD 65...")
        await page.locator("#celular").click()
        await page.locator("#celular").type("(65) 99269-1987", delay=80)
        await asyncio.sleep(0.5)

        print("8. Preenchendo o E-mail...")
        await page.locator("#email").click()
        await page.locator("#email").type("joaopedromachadobottan@gmail.com", delay=60)
        await asyncio.sleep(0.5)

        print("9. Selecionando o procedimento: Limpeza com Peeling de Diamante...")
        await page.locator("#servico").select_option(value="Limpeza com Peeling de Diamante")
        await asyncio.sleep(1)

        print("10. Escolhendo data preferencial...")
        await page.locator("#data_preferencial").fill("2026-11-18")
        await asyncio.sleep(1)

        print("11. Selecionando horário conforme o funcionamento da clínica...")
        await page.locator("#horario_preferencial").select_option(value="09:00 às 11:00 (Ter ou Qui)")
        await asyncio.sleep(1)

        print("12. Escrevendo observação sobre o atendimento...")
        await page.locator("#observacoes").click()
        await page.locator("#observacoes").type("Demonstração ao vivo realizada diretamente no navegador do usuário!", delay=40)
        await asyncio.sleep(1.5)

        print("13. Clicando no botão para enviar a reserva...")
        submit_btn = page.locator("button[type='submit']")
        await submit_btn.hover()
        await asyncio.sleep(1)
        await submit_btn.click()

        print("14. Aguardando a página de confirmação...")
        await page.wait_for_url("**/agendamento-sucesso/*")
        await asyncio.sleep(3)

        print("15. Navegando para o Painel Administrativo para acompanhar a chegada da reserva...")
        await page.goto("http://localhost:3000/admin/reservas", wait_until="networkidle")
        await asyncio.sleep(4)

        print("16. Demonstração concluída com sucesso! Fechando navegador em 3 segundos...")
        await asyncio.sleep(3)
        await browser.close()
        print("Finalizado!")

if __name__ == "__main__":
    asyncio.run(main())
