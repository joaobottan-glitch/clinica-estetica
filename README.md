# Estética Duda - Nova Mutum (MT)
## Landing Page & Sistema de Agendamentos em Python + SQLite

Aplicação desenvolvida para esteticista especializada em limpeza de pele e tratamentos faciais na cidade de **Nova Mutum - MT**.

---

### 🚀 Como Executar

1. **Instalar dependências** (caso ainda não tenha instalado):
   ```bash
   pip install -r requirements.txt
   ```

2. **Iniciar o servidor**:
   ```bash
   python app.py
   ```

3. **Acessar no navegador**:
   - **Landing Page Pública**: [http://127.0.0.1:3000/](http://127.0.0.1:3000/)
   - **Painel de Reservas (Admin Protegido)**: [http://127.0.0.1:3000/admin/reservas](http://127.0.0.1:3000/admin/reservas)
   - **Tela de Login Administrativo**: [http://127.0.0.1:3000/admin/login](http://127.0.0.1:3000/admin/login)
   - **API JSON de Reservas**: [http://127.0.0.1:3000/api/reservas](http://127.0.0.1:3000/api/reservas)

---

### 🔐 Credenciais de Acesso ao Painel
- **Usuário:** `eduardacamargo77@hotmail.com`
- **Senha:** `Duda777`
*(Qualquer tentativa de acesso direto às rotas administrativas sem autenticação é automaticamente redirecionada para a tela de login).*

---

### 📧 E-mail Oficial de Notificações
- **Destinatário das Reservas:** `eduardacamargo77@hotmail.com`
- Sempre que um cliente preenche o formulário da landing page, o sistema salva no banco SQLite e dispara uma notificação automática assíncrona por e-mail com todos os dados da reserva (Nome, E-mail, Celular, Procedimento, Data/Horário e link direto para WhatsApp).
- **Variáveis de Ambiente Opcionais para SMTP Real:**
  - `SMTP_SERVER` (padrão: `smtp.office365.com` ou `smtp.gmail.com`)
  - `SMTP_PORT` (padrão: `587`)
  - `SMTP_USER` (ex: seu e-mail de envio)
  - `SMTP_PASS` (senha de aplicativo)
  *(Caso as variáveis não sejam informadas, o sistema registra a notificação estruturada em log com segurança sem interromper o fluxo).*

---

### 🧭 Estrutura de Rotas

| Rota | Método | Função |
| :--- | :--- | :--- |
| `/` | `GET` | Landing Page de alta conversão para clientes de Nova Mutum |
| `/agendar` | `POST` | Processa o formulário e salva no banco de dados SQLite (`clinica.db`) |
| `/agendamento-sucesso/<id>` | `GET` | Tela de agradecimento com botão de confirmação direta via WhatsApp |
| `/admin/reservas` | `GET` | Painel gerencial da esteticista com métricas, filtros por status e busca |
| `/admin/reservas/<id>/status` | `POST` | Atualiza o status do agendamento (Pendente, Confirmado, Concluído, Cancelado) |
| `/admin/reservas/<id>/excluir` | `POST` | Exclui um agendamento do sistema |
| `/api/reservas` | `GET` | Retorna lista de agendamentos em JSON para integrações (ex: chatbots) |

---

### 💾 Estrutura do Banco SQLite (`clinica.db`)

Tabela: `agendamentos`
- `id` (INTEGER PRIMARY KEY)
- `nome_completo` (TEXT)
- `email` (TEXT)
- `celular` (TEXT com máscara `(66) 9XXXX-XXXX`)
- `servico` (TEXT)
- `data_preferencial` (TEXT)
- `horario_preferencial` (TEXT)
- `observacoes` (TEXT)
- `status` (TEXT: 'Pendente', 'Confirmado', 'Concluído', 'Cancelado')
- `criado_em` (TIMESTAMP)
