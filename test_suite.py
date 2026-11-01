import urllib.request
import urllib.parse
import json
import re

BASE_URL = "http://localhost:3000"

def log(msg, status="INFO"):
    icons = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌"}
    print(f"{icons.get(status, '•')} [{status}] {msg}")

def test_landing_page():
    log("Testando GET / (Landing Page)...")
    req = urllib.request.urlopen(f"{BASE_URL}/")
    assert req.getcode() == 200, f"Status code inválido: {req.getcode()}"
    html = req.read().decode("utf-8")
    
    # Validações estruturais
    assert "Estética Duda" in html, "Título da marca não encontrado"
    assert "Nova Mutum" in html, "Referência à cidade de Nova Mutum não encontrada"
    assert "Limpeza de Pele Profunda" in html, "Procedimento principal não listado"
    assert "form-agendamento" in html, "Formulário de agendamento não encontrado"
    assert 'name="celular"' in html, "Campo celular ausente no formulário"
    assert 'name="email"' in html, "Campo email ausente no formulário"
    assert 'name="nome_completo"' in html, "Campo nome_completo ausente no formulário"
    log("Landing page renderizada perfeitamente com todos os elementos de Nova Mutum!", "SUCCESS")

def test_agendamento_flow():
    log("Testando POST /agendar (Envio de formulário de reserva)...")
    
    # Criamos um opener que gerencia cookies e redirects
    import http.cookiejar
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    
    payload = {
        "nome_completo": "Larissa Oliveira",
        "email": "larissa.oliveira@gmail.com",
        "celular": "(66) 99712-3456",
        "servico": "Limpeza com Peeling de Diamante",
        "data_preferencial": "2026-11-15",
        "horario_preferencial": "Tarde (14h às 18h)",
        "observacoes": "Pele com sensibilidade leve, primeiro procedimento"
    }
    
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}/agendar", data=data, method="POST")
    resp = opener.open(req)
    
    assert resp.getcode() == 200, f"Falha na submissão do agendamento: {resp.getcode()}"
    final_url = resp.geturl()
    log(f"Redirecionado com sucesso para: {final_url}", "SUCCESS")
    assert "/agendamento-sucesso/" in final_url, "URL final não é a página de sucesso"
    
    sucesso_html = resp.read().decode("utf-8")
    assert "Larissa Oliveira" in sucesso_html, "Nome do cliente não exibido na página de sucesso"
    assert "Limpeza com Peeling de Diamante" in sucesso_html, "Serviço não exibido na página de sucesso"
    assert "wa.me" in sucesso_html, "Link direto para o WhatsApp não encontrado"
    
    # Extrai o ID da reserva
    match = re.search(r"/agendamento-sucesso/(\d+)", final_url)
    reserva_id = int(match.group(1)) if match else None
    assert reserva_id is not None, "ID do agendamento não identificado na URL"
    log(f"Agendamento criado no banco SQLite com ID #{reserva_id}!", "SUCCESS")
    return reserva_id, opener

def test_admin_auth_and_dashboard(reserva_id, opener):
    log("Testando bloqueio de rota protegida sem login...")
    # Novo opener sem sessão
    import http.cookiejar
    clean_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    resp = clean_opener.open(f"{BASE_URL}/admin/reservas")
    assert "/admin/login" in resp.geturl(), "Acesso não redirecionou para /admin/login"
    log("Bloqueio de rota sem login funcionando perfeitamente!", "SUCCESS")

    log("Testando login com senha incorreta...")
    login_err_data = urllib.parse.urlencode({"usuario": "eduardacamargo77@hotmail.com", "senha": "senha_errada"}).encode("utf-8")
    req_err = urllib.request.Request(f"{BASE_URL}/admin/login", data=login_err_data, method="POST")
    resp_err = clean_opener.open(req_err)
    html_err = resp_err.read().decode("utf-8")
    assert "E-mail ou senha inválidos" in html_err, "Mensagem de erro não exibida após senha errada"
    log("Rejeição de credenciais incorretas validada!", "SUCCESS")

    log("Testando login com credenciais oficiais (eduardacamargo77@hotmail.com / Duda777)...")
    login_data = urllib.parse.urlencode({"usuario": "eduardacamargo77@hotmail.com", "senha": "Duda777"}).encode("utf-8")
    req_login = urllib.request.Request(f"{BASE_URL}/admin/login", data=login_data, method="POST")
    resp_login = opener.open(req_login)
    assert resp_login.getcode() == 200
    assert "/admin/reservas" in resp_login.geturl(), "Não redirecionou para /admin/reservas após login correto"
    html_admin = resp_login.read().decode("utf-8")
    assert "Bem-vinda ao painel de gestão" in html_admin or "Painel de Gestão" in html_admin
    assert f"#{reserva_id}" in html_admin, f"Reserva #{reserva_id} não listada no painel administrativo"
    assert "Larissa Oliveira" in html_admin, "Nome do cliente não encontrado na tabela administrativa"
    log("Login realizado com sucesso e painel liberado!", "SUCCESS")

def test_atualizar_status(reserva_id, opener):
    log(f"Testando POST /admin/reservas/{reserva_id}/status (Alterar status para 'Confirmado')...")
    data = urllib.parse.urlencode({"status": "Confirmado"}).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}/admin/reservas/{reserva_id}/status", data=data, method="POST")
    resp = opener.open(req)
    assert resp.getcode() == 200
    
    # Confere se no HTML agora consta 'Confirmado'
    html = resp.read().decode("utf-8")
    assert "Confirmado" in html, "Status não atualizado para Confirmado"
    log(f"Status do agendamento #{reserva_id} alterado para 'Confirmado'!", "SUCCESS")

def test_api_json(reserva_id):
    log("Testando GET /api/reservas (API REST JSON)...")
    req = urllib.request.urlopen(f"{BASE_URL}/api/reservas")
    assert req.getcode() == 200
    data = json.loads(req.read().decode("utf-8"))
    
    assert "reservas" in data, "Chave 'reservas' não encontrada no JSON"
    assert data["total"] >= 1, "Total de reservas na API zerado"
    
    reserva = next((r for r in data["reservas"] if r["id"] == reserva_id), None)
    assert reserva is not None, f"Reserva #{reserva_id} não retornada pela API"
    assert reserva["nome_completo"] == "Larissa Oliveira"
    assert reserva["status"] == "Confirmado"
    assert reserva["servico"] == "Limpeza com Peeling de Diamante"
    log(f"API JSON validada com sucesso! Resposta contém {data['total']} registro(s).", "SUCCESS")

if __name__ == "__main__":
    print("\n" + "="*60)
    print(" 🧪 INICIANDO BATERIA DE TESTES END-TO-END (PORTA 3000)")
    print("="*60 + "\n")
    
    try:
        test_landing_page()
        reserva_id, opener = test_agendamento_flow()
        test_admin_auth_and_dashboard(reserva_id, opener)
        test_atualizar_status(reserva_id, opener)
        test_api_json(reserva_id)
        
        print("\n" + "="*60)
        print(" 🎉 TODOS OS TESTES PASSARAM COM 100% DE SUCESSO!")
        print("="*60 + "\n")
    except Exception as e:
        log(f"Erro no teste: {str(e)}", "ERROR")
        raise e
