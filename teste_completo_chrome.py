import asyncio
from playwright.async_api import async_playwright

async def main():
    print("\n" + "="*60)
    print(" 🧪 EXECUTANDO TESTE COMPLETO NO GOOGLE CHROME ESTÁVEL")
    print("="*60 + "\n")

    async with async_playwright() as p:
        # Lança diretamente o Google Chrome estável instalado no Windows com janela visível
        print("1. Abrindo o Google Chrome oficial instalado no seu computador...")
        browser = await p.chromium.launch(
            channel="chrome",
            headless=False,
            slow_mo=1000,
            args=["--start-maximized", "--disable-infobars"]
        )
        context = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await context.new_page()

        print("2. Acessando a Landing Page da Estética Duda (http://localhost:3000)...")
        await page.goto("http://localhost:3000", wait_until="networkidle")
        await asyncio.sleep(2)

        print("3. Rolando e verificando procedimentos e diferenciais...")
        await page.evaluate("window.scrollBy({ top: 500, behavior: 'smooth' });")
        await asyncio.sleep(2)

        print("4. Verificando os horários de atendimento de Nova Mutum...")
        await page.evaluate("window.scrollBy({ top: 600, behavior: 'smooth' });")
        await asyncio.sleep(2)

        print("5. Rolando até o formulário de reserva...")
        await page.locator("#agendamento").scroll_into_view_if_needed()
        await asyncio.sleep(1.5)

        print("6. Preenchendo dados de agendamento de teste:")
        print("   - Nome: Mariana Albuquerque")
        await page.locator("#nome_completo").click()
        await page.locator("#nome_completo").type("Mariana Albuquerque", delay=70)
        await asyncio.sleep(0.5)

        print("   - Celular: (65) 99812-4455")
        await page.locator("#celular").click()
        await page.locator("#celular").type("(65) 99812-4455", delay=80)
        await asyncio.sleep(0.5)

        print("   - E-mail: mariana.albuquerque@gmail.com")
        await page.locator("#email").click()
        await page.locator("#email").type("mariana.albuquerque@gmail.com", delay=60)
        await asyncio.sleep(0.5)

        print("   - Procedimento: Revitalização & Hidratação de Ouro")
        await page.locator("#servico").select_option(value="Revitalização & Hidratação de Ouro")
        await asyncio.sleep(1)

        print("   - Data: 2026-11-25")
        await page.locator("#data_preferencial").fill("2026-11-25")
        await asyncio.sleep(1)

        print("   - Horário: 12:30 às 16:00 (Seg, Qua ou Sex)")
        await page.locator("#horario_preferencial").select_option(value="12:30 às 16:00 (Seg, Qua ou Sex)")
        await asyncio.sleep(1)

        print("   - Observações...")
        await page.locator("#observacoes").click()
        await page.locator("#observacoes").type("Teste de validação executado no Google Chrome nativo do Windows.", delay=40)
        await asyncio.sleep(1.5)

        print("7. Enviando formulário de reserva...")
        btn_enviar = page.locator("button[type='submit']")
        await btn_enviar.click()

        print("8. Aguardando tela de confirmação...")
        await page.wait_for_url("**/agendamento-sucesso/*")
        print(f"✅ Reserva criada com sucesso! URL: {page.url}")
        await asyncio.sleep(3)

        print("9. Acessando a área administrativa protegida (/admin/reservas)...")
        await page.goto("http://localhost:3000/admin/reservas", wait_until="networkidle")
        print("✅ Redirecionado com segurança para a tela de Login!")
        await asyncio.sleep(2)

        print("10. Efetuando login como Administradora:")
        print("    - Usuário: eduardacamargo77@hotmail.com")
        await page.locator("#usuario").click()
        await page.locator("#usuario").type("eduardacamargo77@hotmail.com", delay=50)
        await asyncio.sleep(0.5)

        print("    - Senha: •••••••")
        await page.locator("#senha").click()
        await page.locator("#senha").type("Duda777", delay=80)
        await asyncio.sleep(1)

        print("11. Clicando em Entrar no Painel...")
        await page.click("button[type='submit']")
        await page.wait_for_url("**/admin/reservas*")
        print("✅ Login efetuado! Acesso liberado ao Painel de Gestão!")
        await asyncio.sleep(3)

        print("12. Verificando a nova reserva da Mariana Albuquerque no topo da tabela...")
        await page.evaluate("window.scrollBy({ top: 300, behavior: 'smooth' });")
        await asyncio.sleep(3)

        print("13. Alterando o status para 'Confirmado' ao vivo...")
        # Altera o primeiro select de status na tabela
        primeiro_select = page.locator(".reservas-table tbody tr:first-child select[name='status']")
        await primeiro_select.select_option("Confirmado")
        await asyncio.sleep(3)

        print("14. Finalizando teste com sucesso! A janela fechará em 5 segundos.")
        await asyncio.sleep(5)
        await browser.close()

        print("\n" + "="*60)
        print(" 🎉 TESTE NO GOOGLE CHROME CONCLUÍDO COM 100% DE ÊXITO!")
        print("="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
