import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        print("Iniciando navegador Chromium...")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("Acessando http://localhost:3000...")
        await page.goto("http://localhost:3000", wait_until="networkidle")

        print("Rolando até o formulário de agendamento...")
        await page.locator("#agendamento").scroll_into_view_if_needed()

        print("Preenchendo os dados da reserva:")
        print(" - Nome: JOÃO PEDRO MACHADO BOTTAN")
        await page.fill("#nome_completo", "JOÃO PEDRO MACHADO BOTTAN")

        print(" - E-mail: joaopedromachadobottan@gmail.com")
        await page.fill("#email", "joaopedromachadobottan@gmail.com")

        print(" - Celular: (65) 99269-1987")
        # Preenche o celular (o script aciona a máscara)
        await page.click("#celular")
        await page.fill("#celular", "(65) 99269-1987")

        print(" - Procedimento: Limpeza com Peeling de Diamante")
        await page.select_option("#servico", value="Limpeza com Peeling de Diamante")

        print(" - Data: 2026-11-12")
        await page.fill("#data_preferencial", "2026-11-12")

        print(" - Horário: 12:30 às 16:00 (Seg, Qua ou Sex)")
        await page.select_option("#horario_preferencial", value="12:30 às 16:00 (Seg, Qua ou Sex)")

        print(" - Observações: Teste de agendamento automatizado para validação completa.")
        await page.fill("#observacoes", "Teste de agendamento automatizado para validação completa da clínica estética em Nova Mutum.")

        print("Enviando o formulário...")
        await page.click("button[type='submit']")

        # Aguarda redirecionamento para a página de sucesso
        await page.wait_for_url("**/agendamento-sucesso/*")
        url_sucesso = page.url
        print(f"✅ Redirecionado com sucesso para: {url_sucesso}")

        # Captura screenshot da confirmação
        screenshot_path = "d:/IAs/Projetos - IA/Duda/Clínica Estética/Site/screenshot_reserva_sucesso.png"
        await page.screenshot(path=screenshot_path, full_page=False)
        print(f"Screenshot da confirmação salvo em: {screenshot_path}")

        # Acessa o painel de reservas para verificar se o João Pedro já aparece
        print("Acessando o Painel Administrativo de Reservas...")
        await page.goto("http://localhost:3000/admin/reservas", wait_until="networkidle")
        screenshot_admin_path = "d:/IAs/Projetos - IA/Duda/Clínica Estética/Site/screenshot_admin_atualizado.png"
        await page.screenshot(path=screenshot_admin_path, full_page=False)
        print(f"Screenshot do Painel Administrativo salvo em: {screenshot_admin_path}")

        await browser.close()
        print("Fluxo de agendamento concluído com 100% de sucesso!")

if __name__ == "__main__":
    asyncio.run(main())
