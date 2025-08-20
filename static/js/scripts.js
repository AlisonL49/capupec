document.addEventListener("DOMContentLoaded", function () {

    // ==========================
    // ROTACIÓN DE ICONOS SUBMENÚ
    // ==========================
    document.querySelectorAll(".collapse").forEach(submenu => {
        submenu.addEventListener("show.bs.collapse", function () {
            const arrow = this.previousElementSibling.querySelector(".chevron-dropdown");
            if (arrow) arrow.style.transform = "rotate(90deg)";
        });
        submenu.addEventListener("hide.bs.collapse", function () {
            const arrow = this.previousElementSibling.querySelector(".chevron-dropdown");
            if (arrow) arrow.style.transform = "rotate(0deg)";
        });
    });

    // ==========================
    // OBTENER CSRF TOKEN
    // ==========================
    function getCSRFToken() {
        const meta = document.querySelector('meta[name="csrf-token"]');
        if (meta) return meta.getAttribute('content');
        const name = 'csrftoken';
        for (let cookie of document.cookie.split(';')) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                return decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
        return '';
    }

    // ==========================
    // FUNCIONES GENÉRICAS
    // ==========================
    function openEditModal(button, modalId, fieldsMap) {
        const data = button.dataset;
        for (let fieldId in fieldsMap) {
            const field = document.getElementById(fieldId);
            if (field) {
                if (field.type === "checkbox") {
                    field.checked = ['true', '1', 'True'].includes(data[fieldsMap[fieldId]]);
                } else {
                    field.value = data[fieldsMap[fieldId]] || '';
                }
            }
        }
        new bootstrap.Modal(document.getElementById(modalId)).show();
    }

    function bindEditButtons(selector, modalId, fieldsMap) {
        document.querySelectorAll(selector).forEach(btn => {
            btn.addEventListener('click', function () {
                openEditModal(this, modalId, fieldsMap);
            });
        });
    }

    function bindDeleteButtons(selector, urlBase, confirmMsg) {
        document.querySelectorAll(selector).forEach(btn => {
            btn.addEventListener('click', function () {
                if (!confirm(confirmMsg)) return;
                fetch(`${urlBase}${this.dataset.id}/`, {
                    method: 'POST',
                    headers: { 'X-CSRFToken': getCSRFToken() }
                })
                    .then(response => {
                        if (response.ok) {
                            location.reload();
                        } else {
                            response.json().then(data => alert(data.error || 'Error al eliminar.'));
                        }
                    })
                    .catch(() => alert('Error de red.'));
            });
        });
    }

    function bindEditForm(formId, urlBase) {
        const form = document.getElementById(formId);
        if (form) {
            form.addEventListener('submit', function (e) {
                e.preventDefault();
                const id = form.querySelector('[name="id"]').value;
                const formData = new FormData(this);
                fetch(`${urlBase}${id}/`, {
                    method: 'POST',
                    body: formData,
                    headers: { 'X-CSRFToken': getCSRFToken() }
                })
                    .then(response => {
                        if (response.ok) {
                            location.reload();
                        } else {
                            response.json().then(data => alert(data.error || 'Error al guardar.'));
                        }
                    })
                    .catch(() => alert('Error de red.'));
            });
        }
    }

    // ==========================
    // MÓDULOS ADMINISTRATIVOS
    // ==========================

    // 1️⃣ Parámetros
    bindEditButtons('.btn-action-edit-parm', 'modalEditarParametro', {
        'edit_id': 'id',
        'edit_abreviatura': 'abreviatura',
        'edit_descripcion': 'descripcion',
        'edit_valor': 'valor',
        'edit_estado': 'estado'
    });
    bindDeleteButtons('.btn-action-delete-parm', '/administracion/parametros/eliminar/', '¿Eliminar este parámetro?');
    bindEditForm('formEditarParametro', '/administracion/parametros/editar/');

    // 2️⃣ Formas de Pago
    bindEditButtons('.btn-action-edit-fpago', 'modalEditarFormaPago', {
        'edit_fpago_id': 'id',
        'edit_fpago_descripcion': 'descripcion',
        'edit_fpago_estado': 'estado'
    });
    bindDeleteButtons('.btn-action-delete-fpago', '/administracion/formas-pago/eliminar/', '¿Eliminar esta forma de pago?');
    bindEditForm('formEditarFormaPago', '/administracion/formas-pago/editar/');

    // 3️⃣ Tipos de Crédito
    bindEditButtons('.btn-action-edit-tcredito', 'modalEditarTipoCredito', {
        'edit_tcredito_id': 'id',
        'edit_tcredito_tipo': 'tipo',
        'edit_tcredito_abreviatura': 'abreviatura',
        'edit_tcredito_monto_maximo': 'monto_maximo',
        'edit_tcredito_num_cuotas': 'num_cuotas',
        'edit_tcredito_tasa_interes': 'tasa_interes',
        'edit_tcredito_aporte_minimo': 'aporte_minimo',
        'edit_tcredito_porcentaje_encaje': 'porcentaje_encaje',
        'edit_tcredito_gracia': 'gracia',
        'edit_tcredito_porcentaje_mora': 'porcentaje_mora',
        'edit_tcredito_estado': 'estado'
    });
    bindDeleteButtons('.btn-action-delete-tcredito', '/administracion/tipos-credito/eliminar/', '¿Eliminar este tipo de crédito?');
    bindEditForm('formEditarTipoCredito', '/administracion/tipos-credito/editar/');

    // 4️⃣ Tipos de Ahorro
    bindEditButtons('.btn-action-edit-tahorro', 'modalEditarTipoAhorro', {
        'edit_tahorro_id': 'id',
        'edit_tahorro_nombre': 'nombre',
        'edit_tahorro_descripcion': 'descripcion',
        'edit_tahorro_estado': 'estado'
    });
    bindDeleteButtons('.btn-action-delete-tahorro', '/administracion/tipos-ahorro/eliminar/', '¿Eliminar este tipo de ahorro?');
    bindEditForm('formEditarTipoAhorro', '/administracion/tipos-ahorro/editar/');

    // 5️⃣ Plazos Fijos
    bindEditButtons('.btn-action-edit-pfijo', 'modalEditarPlazoFijo', {
        'edit_pfijo_id': 'id',
        'edit_pfijo_nombre': 'nombre',
        'edit_pfijo_tasa': 'tasa',
        'edit_pfijo_plazo': 'plazo',
        'edit_pfijo_estado': 'estado'
    });
    bindDeleteButtons('.btn-action-delete-pfijo', '/administracion/plazos-fijos/eliminar/', '¿Eliminar este plazo fijo?');
    bindEditForm('formEditarPlazoFijo', '/administracion/plazos-fijos/editar/');


});

// ---------------- SOLICITUD DE CRÉDITO ----------------
document.addEventListener("DOMContentLoaded", function () {
    const solicitudForm = document.querySelector("form#form-solicitud-credito");
    const accionInput = document.getElementById("accion");
    const btnCalcular = document.querySelector("#btn-calcular");
    const btnImprimir = document.querySelector("#btn-imprimir");

    if (solicitudForm) {
        // Botón Calcular
        if (btnCalcular) {
            btnCalcular.addEventListener("click", function (e) {
                e.preventDefault();
                accionInput.value = "calcular";
                solicitudForm.submit();
            });
        }

        // Botón Imprimir
        if (btnImprimir) {
            btnImprimir.addEventListener("click", function (e) {
                e.preventDefault();
                const socioId = this.getAttribute("data-socio-id");
                if (socioId) {
                    window.open(`/solicitud-credito/imprimir/${socioId}/`, "_blank");
                } else {
                    alert("Debe seleccionar un socio antes de imprimir.");
                }
            });
        }
    }

    // ---------------- SOLICITUD DE CRÉDITO: ACTUALIZAR DETALLES ----------------
    const tipoCreditoSelect = document.getElementById("tipo_credito");
    const tasaInteresField = document.getElementById("interes");
    const graciaField = document.getElementById("gracia");
    const minAporteField = document.getElementById("min_aporte");

    if (tipoCreditoSelect && tasaInteresField && graciaField) {
        tipoCreditoSelect.addEventListener("change", function () {
            const tipoCreditoId = this.value;
            if (tipoCreditoId) {
                fetch(`/operativo/get_credit_details?tipo_credito_id=${tipoCreditoId}`)
                    .then(response => response.json())
                    .then(data => {
                        tasaInteresField.value = data.interes;
                        graciaField.value = data.gracia;
                        minAporteField.value = data.min_aporte;
                    })
                    .catch(error => console.error("Error fetching credit details:", error));
            }
        });
    }
});

