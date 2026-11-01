document.addEventListener("DOMContentLoaded", () => {
  // 1. Máscara de Telefone/Celular (66) 9XXXX-XXXX
  const phoneInput = document.getElementById("celular");
  if (phoneInput) {
    phoneInput.addEventListener("input", (e) => {
      let value = e.target.value.replace(/\D/g, "");
      if (value.length > 11) value = value.slice(0, 11);

      if (value.length > 10) {
        // (XX) 9XXXX-XXXX
        value = value.replace(/^(\d{2})(\d{5})(\d{4})$/, "($1) $2-$3");
      } else if (value.length > 6) {
        // (XX) XXXX-XXXX
        value = value.replace(/^(\d{2})(\d{4})(\d{0,4})$/, "($1) $2-$3");
      } else if (value.length > 2) {
        // (XX) XXXX
        value = value.replace(/^(\d{2})(\d{0,5})$/, "($1) $2");
      } else if (value.length > 0) {
        value = value.replace(/^(\d{0,2})$/, "($1");
      }
      e.target.value = value;
    });

    // Se o campo estiver vazio ao focar, pré-preenche com o DDD 66 (Nova Mutum - MT)
    phoneInput.addEventListener("focus", () => {
      if (!phoneInput.value) {
        phoneInput.value = "(66) ";
      }
    });
  }

  // 2. Preenchimento automático do procedimento selecionado nos cards
  const selectServiceButtons = document.querySelectorAll(".btn-select-service");
  const serviceSelect = document.getElementById("servico");

  selectServiceButtons.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const serviceName = btn.getAttribute("data-service-name");
      if (serviceSelect && serviceName) {
        // Procura opção correspondente
        for (let i = 0; i < serviceSelect.options.length; i++) {
          if (serviceSelect.options[i].text.includes(serviceName) || serviceSelect.options[i].value === serviceName) {
            serviceSelect.selectedIndex = i;
            break;
          }
        }
      }
    });
  });

  // 3. Data mínima no campo de agendamento (hoje)
  const dateInput = document.getElementById("data_preferencial");
  if (dateInput) {
    const today = new Date().toISOString().split("T")[0];
    dateInput.setAttribute("min", today);
  }
});
