from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from functools import wraps
import database as db
import mailer
import urllib.parse

app = Flask(__name__)
app.secret_key = "estetica_duda_nova_mutum_secret_key"

# Inicializa o banco de dados na inicialização
db.init_db()

# WhatsApp oficial da Estética Duda (+55 65 9964-4755)
WHATSAPP_CLINICA = "556599644755"

# E-mail oficial de contato e notificações de reservas
EMAIL_CONTATO = "eduardacamargo77@hotmail.com"

# Credenciais de acesso administrativo
ADMIN_USUARIO = "eduardacamargo77@hotmail.com"
ADMIN_SENHA = "Duda777"

def login_required(f):
    """Decorator para exigir autenticação prévia nas rotas administrativas."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin_autenticado"):
            flash("Acesso restrito. Por favor, faça login com suas credenciais.", "warning")
            return redirect(url_for("admin_login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    """Rota principal: Landing page de alta conversão da clínica estética."""
    servicos = [
        {
            "id": "limpeza-profunda",
            "nome": "Limpeza de Pele Profunda",
            "duracao": "1h 30min",
            "descricao": "Higienização profunda, emoliência avançada, extração minuciosa com técnica indolor, máscara calmante e alta frequência para cicatrização.",
            "destaque": "Mais Procurado",
            "tag": "Renovação Total"
        },
        {
            "id": "peeling-diamante",
            "nome": "Limpeza com Peeling de Diamante",
            "duracao": "1h 45min",
            "descricao": "Associação da limpeza profunda à microdermoabrasão diamantada, promovendo esfoliação mecânica, clareamento suave e estímulo de colágeno.",
            "destaque": "Efeito Glow",
            "tag": "Textura Aveludada"
        },
        {
            "id": "protocolo-acne",
            "nome": "Protocolo Anti-Acne e Desintoxicante",
            "duracao": "1h 30min",
            "descricao": "Focado em peles oleosas e acneicas. Reduz a inflamação, controla a secreção sebácea e previne novas lesões com ativos bactericidas.",
            "destaque": "Cuidado Especial",
            "tag": "Controle Oleosidade"
        },
        {
            "id": "hidratacao-ouro",
            "nome": "Revitalização & Hidratação de Ouro",
            "duracao": "1h 15min",
            "descricao": "Tratamento nutritivo intenso com máscara enriquecida com oligoelementos e ácido hialurônico para devolver a luminosidade e viço natural da pele.",
            "destaque": "Nutrição Intensa",
            "tag": "Pele Iluminada"
        }
    ]
    return render_template(
        "index.html", 
        servicos=servicos, 
        whatsapp_clinica=WHATSAPP_CLINICA,
        email_contato=EMAIL_CONTATO
    )

@app.route("/agendar", methods=["POST"])
def agendar():
    """Recebe o formulário de reserva da landing page e salva no SQLite."""
    nome = request.form.get("nome_completo", "").strip()
    email = request.form.get("email", "").strip()
    celular = request.form.get("celular", "").strip()
    servico = request.form.get("servico", "Limpeza de Pele Profunda").strip()
    data = request.form.get("data_preferencial", "").strip()
    horario = request.form.get("horario_preferencial", "").strip()
    observacoes = request.form.get("observacoes", "").strip()

    # Validações básicas de preenchimento
    if not nome or not email or not celular:
        flash("Por favor, preencha todos os campos obrigatórios (Nome, E-mail e Celular).", "error")
        return redirect(url_for("index") + "#agendamento")

    # Inserção no banco SQLite
    try:
        agendamento_id = db.criar_agendamento(
            nome_completo=nome,
            email=email,
            celular=celular,
            servico=servico,
            data_preferencial=data,
            horario_preferencial=horario,
            observacoes=observacoes
        )

        # Dispara notificação por e-mail para a esteticista em background
        dados_notificacao = {
            "id": agendamento_id,
            "nome_completo": nome,
            "email": email,
            "celular": celular,
            "servico": servico,
            "data_preferencial": data,
            "horario_preferencial": horario,
            "observacoes": observacoes
        }
        mailer.disparar_notificacao_reserva(dados_notificacao)

        return redirect(url_for("agendamento_sucesso", agendamento_id=agendamento_id))
    except Exception as e:
        flash(f"Ocorreu um erro ao registrar sua reserva: {str(e)}", "error")
        return redirect(url_for("index") + "#agendamento")

@app.route("/agendamento-sucesso/<int:agendamento_id>")
def agendamento_sucesso(agendamento_id):
    """Página de confirmação com link inteligente para o WhatsApp."""
    reserva = db.obter_agendamento_por_id(agendamento_id)
    if not reserva:
        flash("Agendamento não encontrado.", "error")
        return redirect(url_for("index"))

    # Mensagem personalizada para disparo via WhatsApp
    texto_whatsapp = (
        f"Olá! Acabei de solicitar um agendamento na sua clínica em Nova Mutum.\n\n"
        f"👤 *Nome:* {reserva['nome_completo']}\n"
        f"✨ *Procedimento:* {reserva['servico']}\n"
        f"📅 *Data Preferencial:* {reserva['data_preferencial'] or 'A combinar'}\n"
        f"⏰ *Horário:* {reserva['horario_preferencial'] or 'A combinar'}\n\n"
        f"Gostaria de confirmar a disponibilidade. Obrigado!"
    )
    link_whatsapp = f"https://wa.me/{WHATSAPP_CLINICA}?text={urllib.parse.quote(texto_whatsapp)}"

    return render_template("sucesso.html", reserva=reserva, link_whatsapp=link_whatsapp)

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """Tela e processamento de login para acesso ao painel de reservas."""
    if session.get("admin_autenticado"):
        return redirect(url_for("admin_reservas"))

    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip().lower()
        senha = request.form.get("senha", "")
        next_url = request.form.get("next") or url_for("admin_reservas")

        if usuario == ADMIN_USUARIO.lower() and senha == ADMIN_SENHA:
            session["admin_autenticado"] = True
            session["admin_usuario"] = ADMIN_USUARIO
            flash(f"Bem-vinda ao painel de gestão, Eduarda!", "success")
            return redirect(next_url)
        else:
            flash("E-mail ou senha inválidos. Por favor, tente novamente.", "error")

    return render_template("login.html")

@app.route("/admin/logout")
def admin_logout():
    """Encerra a sessão administrativa."""
    session.pop("admin_autenticado", None)
    session.pop("admin_usuario", None)
    flash("Sessão finalizada com sucesso.", "info")
    return redirect(url_for("admin_login"))

@app.route("/admin/reservas")
@login_required
def admin_reservas():
    """Painel administrativo para visualizar e gerenciar reservas."""
    filtro_status = request.args.get("status", "Todos")
    busca = request.args.get("busca", "").strip()

    reservas = db.listar_agendamentos(status=filtro_status, busca=busca)
    stats = db.obter_estatisticas()

    return render_template(
        "admin_reservas.html",
        reservas=reservas,
        stats=stats,
        filtro_status=filtro_status,
        busca=busca,
        whatsapp_clinica=WHATSAPP_CLINICA
    )

@app.route("/admin/reservas/<int:agendamento_id>/status", methods=["POST"])
@login_required
def atualizar_status_reserva(agendamento_id):
    """Atualiza o status de um agendamento (Pendente, Confirmado, Concluído, Cancelado)."""
    novo_status = request.form.get("status")
    if novo_status in ["Pendente", "Confirmado", "Concluído", "Cancelado"]:
        db.atualizar_status(agendamento_id, novo_status)
        flash(f"Status do agendamento #{agendamento_id} atualizado para '{novo_status}'!", "success")
    else:
        flash("Status inválido informado.", "error")
    
    return redirect(request.referrer or url_for("admin_reservas"))

@app.route("/admin/reservas/<int:agendamento_id>/excluir", methods=["POST"])
@login_required
def excluir_reserva(agendamento_id):
    """Exclui um agendamento do banco de dados."""
    db.excluir_agendamento(agendamento_id)
    flash(f"Agendamento #{agendamento_id} removido com sucesso.", "info")
    return redirect(request.referrer or url_for("admin_reservas"))

@app.route("/api/reservas", methods=["GET"])
def api_reservas():
    """API JSON para consultar reservas (compatível com integrações e assistentes)."""
    filtro_status = request.args.get("status")
    busca = request.args.get("busca")
    
    registros = db.listar_agendamentos(status=filtro_status, busca=busca)
    
    lista = []
    for reg in registros:
        lista.append({
            "id": reg["id"],
            "nome_completo": reg["nome_completo"],
            "email": reg["email"],
            "celular": reg["celular"],
            "servico": reg["servico"],
            "data_preferencial": reg["data_preferencial"],
            "horario_preferencial": reg["horario_preferencial"],
            "observacoes": reg["observacoes"],
            "status": reg["status"],
            "criado_em": reg["criado_em"]
        })
    return jsonify({"total": len(lista), "reservas": lista})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 3000))
    print(f"Iniciando servidor da Clínica Estética em Nova Mutum na porta {port}...")
    app.run(host="0.0.0.0", port=port, debug=True)
