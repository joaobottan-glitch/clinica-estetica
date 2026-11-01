import os
import threading
import resend

def carregar_env():
    """Carrega variáveis do arquivo .env caso existam."""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                linha = line.strip()
                if linha and not linha.startswith("#") and "=" in linha:
                    chave, valor = linha.split("=", 1)
                    chave = chave.strip()
                    valor = valor.strip()
                    if chave and chave not in os.environ:
                        os.environ[chave] = valor

carregar_env()

# Configurações do Resend
RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "").strip()
EMAIL_NOTIFICACAO_DESTINO = os.environ.get("EMAIL_NOTIFICACAO", "eduardacamargo77@hotmail.com").strip()
RESEND_FROM = os.environ.get("RESEND_FROM", "Estética Duda <onboarding@resend.dev>").strip()

def gerar_corpo_email_html(reserva):
    """Gera o template HTML elegante para a notificação de nova reserva."""
    num_limpo = reserva['celular'].replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
    if not num_limpo.startswith('55'):
        num_whatsapp = '55' + num_limpo
    else:
        num_whatsapp = num_limpo

    link_whatsapp = f"https://wa.me/{num_whatsapp}?text=Ol%C3%A1%20{reserva['nome_completo']}!%20Recebemos%20seu%20agendamento%20na%20Est%C3%A9tica%20Duda."

    return f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
      <meta charset="UTF-8">
      <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #FCFAF8; margin: 0; padding: 20px; color: #2D2825; }}
        .card {{ max-width: 600px; margin: 0 auto; background: #FFFFFF; border-radius: 12px; border: 1px solid #EADBCE; padding: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
        .header {{ border-bottom: 2px solid #F4EADA; padding-bottom: 15px; margin-bottom: 20px; }}
        .title {{ font-size: 22px; color: #A37F38; margin: 0; font-weight: bold; }}
        .subtitle {{ font-size: 13px; color: #8C8480; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 5px; }}
        .badge {{ display: inline-block; background: #FEF3C7; color: #B45309; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 12px; margin-bottom: 15px; }}
        .detail-row {{ margin-bottom: 12px; font-size: 14px; line-height: 1.5; }}
        .label {{ font-weight: bold; color: #5C524C; width: 140px; display: inline-block; }}
        .value {{ color: #2D2825; }}
        .obs-box {{ background: #FAF8F5; border-left: 3px solid #C5A059; padding: 12px; margin-top: 15px; border-radius: 6px; font-size: 13px; font-style: italic; }}
        .btn-whatsapp {{ display: inline-block; background: #25D366; color: #FFFFFF !important; text-decoration: none; padding: 12px 24px; border-radius: 25px; font-weight: bold; font-size: 14px; margin-top: 20px; text-align: center; }}
        .footer {{ margin-top: 25px; padding-top: 15px; border-top: 1px solid #EFEAE5; font-size: 12px; color: #9E9590; text-align: center; }}
      </style>
    </head>
    <body>
      <div class="card">
        <div class="header">
          <h2 class="title">✨ Nova Solicitação de Reserva</h2>
          <div class="subtitle">Estética Duda • Nova Mutum - MT</div>
        </div>

        <div class="badge">🔔 Status: Pendente de Confirmação</div>

        <div class="detail-row"><span class="label">👤 Cliente:</span> <span class="value"><strong>{reserva['nome_completo']}</strong></span></div>
        <div class="detail-row"><span class="label">📱 Celular/WhatsApp:</span> <span class="value">{reserva['celular']}</span></div>
        <div class="detail-row"><span class="label">✉️ E-mail:</span> <span class="value">{reserva['email']}</span></div>
        <div class="detail-row"><span class="label">💆 Procedimento:</span> <span class="value"><strong>{reserva['servico']}</strong></span></div>
        <div class="detail-row"><span class="label">📅 Data Preferencial:</span> <span class="value">{reserva.get('data_preferencial') or 'A combinar'}</span></div>
        <div class="detail-row"><span class="label">⏰ Horário/Turno:</span> <span class="value">{reserva.get('horario_preferencial') or 'A combinar'}</span></div>

        {f'<div class="obs-box"><strong>Observações do cliente:</strong><br>{reserva["observacoes"]}</div>' if reserva.get('observacoes') else ''}

        <div style="text-align: center;">
          <a href="{link_whatsapp}" class="btn-whatsapp">
            💬 Responder Cliente no WhatsApp
          </a>
        </div>

        <div class="footer">
          Esta notificação foi enviada automaticamente pelo sistema da <strong>Estética Duda</strong> via <strong>Resend.com</strong>.<br>
          Destinatário: {EMAIL_NOTIFICACAO_DESTINO}
        </div>
      </div>
    </body>
    </html>
    """

def _enviar_email_resend_worker(reserva):
    """Executa o envio do e-mail via Resend em background."""
    carregar_env()
    api_key = os.environ.get("RESEND_API_KEY", "").strip()
    destinatario = os.environ.get("EMAIL_NOTIFICACAO", EMAIL_NOTIFICACAO_DESTINO).strip()
    remetente = os.environ.get("RESEND_FROM", RESEND_FROM).strip()
    assunto = f"✨ Nova Reserva: {reserva['nome_completo']} - {reserva['servico']}"

    # Se a chave da API do Resend não estiver configurada no .env
    if not api_key:
        print(f"\n[RESEND.COM - AGUARDANDO API KEY]")
        print(f"Para enviar o e-mail real para: {destinatario}")
        print(f"Basta colar sua chave gratuita do Resend no arquivo Site/.env (ex: RESEND_API_KEY=re_12345678)")
        print(f"Dados da Reserva: {reserva['nome_completo']} | {reserva['servico']} | {reserva['celular']}\n")
        return False

    try:
        resend.api_key = api_key
        corpo_html = gerar_corpo_email_html(reserva)

        params: resend.Emails.SendParams = {
            "from": remetente,
            "to": [destinatario],
            "subject": assunto,
            "html": corpo_html,
        }

        resposta = resend.Emails.send(params)
        print(f"✅ [RESEND.COM] E-mail de notificação enviado com sucesso para {destinatario}! ID: {resposta}")
        return True
    except Exception as e:
        print(f"⚠️ [RESEND.COM] Erro ao enviar e-mail para {destinatario}: {str(e)}")
        return False

def disparar_notificacao_reserva(reserva):
    """Dispara a notificação de nova reserva de forma assíncrona (thread) usando o Resend."""
    thread = threading.Thread(target=_enviar_email_resend_worker, args=(reserva,), daemon=True)
    thread.start()
