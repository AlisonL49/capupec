document.addEventListener("DOMContentLoaded", function () {
    // Rotación de flechas en submenús 
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

    // Editar parametros
    document.querySelectorAll('.btn-action-edit-parm').forEach(btn => {
        btn.addEventListener('click', function () {
            document.getElementById('edit_id').value = this.dataset.id;
            document.getElementById('edit_abreviatura').value = this.dataset.abreviatura;
            document.getElementById('edit_descripcion').value = this.dataset.descripcion;
            document.getElementById('edit_valor').value = this.dataset.valor;
            document.getElementById('edit_estado').checked = this.dataset.estado === "True" || this.dataset.estado === "1";
            var modal = new bootstrap.Modal(document.getElementById('modalEditarParametro'));
            modal.show();
        });
    });

    // Eliminar parametros
    document.querySelectorAll('.btn-action-delete-parm').forEach(btn => {
        btn.addEventListener('click', function () {
            const id = this.dataset.id;
            if (confirm('¿Está seguro de eliminar este parámetro?')) {
                fetch(`/administracion/parametros/eliminar/${id}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCSRFToken()
                    }
                }).then(response => {
                    if (response.ok) {
                        location.reload();
                    } else {
                        response.json().then(data => {
                            alert(data.error || 'Error al eliminar el parámetro.');
                        });
                    }
                }).catch(() => {
                    alert('Error de red. Intente nuevamente.');
                });
            }
        });
    });

    // Enviar formulario de edición por AJAX
    const formEditar = document.getElementById('formEditarParametro');
    if (formEditar) {
        formEditar.addEventListener('submit', function (e) {
            e.preventDefault();
            const id = document.getElementById('edit_id').value;
            const formData = new FormData(this);
            fetch(`/administracion/parametros/editar/${id}/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCSRFToken()
                }
            }).then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    response.json().then(data => {
                        alert(data.error || 'Error al editar el parámetro.');
                    });
                }
            }).catch(() => {
                alert('Error de red. Intente nuevamente.');
            });
        });
    }

    // Editar Forma de Pago
    document.querySelectorAll('.btn-action-edit-fpago').forEach(btn => {
        btn.addEventListener('click', function () {
            document.getElementById('edit_fpago_id').value = this.dataset.id;
            document.getElementById('edit_fpago_codigo').value = this.dataset.codigo;
            document.getElementById('edit_fpago_descripcion').value = this.dataset.descripcion;
            document.getElementById('edit_fpago_estado').checked = this.dataset.estado === "True" || this.dataset.estado === "1";
            var modal = new bootstrap.Modal(document.getElementById('modalEditarFormaPago'));
            modal.show();
        });
    });

    // Eliminar Forma de Pago
    document.querySelectorAll('.btn-action-delete-fpago').forEach(btn => {
        btn.addEventListener('click', function () {
            const id = this.dataset.id;
            if (confirm('¿Está seguro de eliminar esta forma de pago?')) {
                fetch(`/administracion/formas-pago/eliminar/${id}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCSRFToken()
                    }
                }).then(response => {
                    if (response.ok) {
                        location.reload();
                    } else {
                        alert('Error al eliminar la forma de pago.');
                    }
                }).catch(() => {
                    alert('Error de red. Intente nuevamente.');
                });
            }
        });
    });

    // Enviar formulario de edición por AJAX
    const formEditarFpago = document.getElementById('formEditarFormaPago');
    if (formEditarFpago) {
        formEditarFpago.addEventListener('submit', function (e) {
            e.preventDefault();
            const id = document.getElementById('edit_fpago_id').value;
            const formData = new FormData(this);
            fetch(`/administracion/formas-pago/editar/${id}/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCSRFToken()
                }
            }).then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    alert('Error al editar la forma de pago.');
                }
            }).catch(() => {
                alert('Error de red. Intente nuevamente.');
            });
        });
    }

    // Editar Tipo de Ahorro
    document.querySelectorAll('.btn-action-edit-tahorro').forEach(btn => {
        btn.addEventListener('click', function () {
            document.getElementById('edit_tahorro_id').value = this.dataset.id;
            document.getElementById('edit_tahorro_abreviatura').value = this.dataset.abreviatura;
            document.getElementById('edit_tahorro_tipo').value = this.dataset.tipo;
            document.getElementById('edit_tahorro_dia_aporte').value = this.dataset.dia_aporte;
            document.getElementById('edit_tahorro_meses_minimo').value = this.dataset.meses_minimo;
            document.getElementById('edit_tahorro_porcent_aporte').value = this.dataset.porcent_aporte;
            document.getElementById('edit_tahorro_capitalizacion').value = this.dataset.capitalizacion;
            document.getElementById('edit_tahorro_estado').checked = this.dataset.estado === "True" || this.dataset.estado === "1";
            var modal = new bootstrap.Modal(document.getElementById('modalEditarTipoAhorro'));
            modal.show();
        });
    });

    // Eliminar Tipo de Ahorro
    document.querySelectorAll('.btn-action-delete-tahorro').forEach(btn => {
        btn.addEventListener('click', function () {
            const id = this.dataset.id;
            if (confirm('¿Eliminar este tipo de ahorro?')) {
                fetch(`/administracion/tipos-ahorros/eliminar/${id}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCSRFToken()
                    }
                }).then(response => {
                    if (response.ok) {
                        location.reload();
                    } else {
                        alert('Error al eliminar el tipo de ahorro.');
                    }
                }).catch(() => {
                    alert('Error de red. Intente nuevamente.');
                });
            }
        });
    });

    // Enviar formulario de edición por AJAX
    const formEditarTAhorro = document.getElementById('formEditarTipoAhorro');
    if (formEditarTAhorro) {
        formEditarTAhorro.addEventListener('submit', function (e) {
            e.preventDefault();
            const id = document.getElementById('edit_tahorro_id').value;
            const formData = new FormData(this);
            fetch(`/administracion/tipos-ahorros/editar/${id}/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCSRFToken()
                }
            }).then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    alert('Error al editar el tipo de ahorro.');
                }
            }).catch(() => {
                alert('Error de red. Intente nuevamente.');
            });
        });
    }

    // Editar Tipo de Crédito
    document.querySelectorAll('.btn-action-edit-tcredito').forEach(btn => {
        btn.addEventListener('click', function () {
            document.getElementById('edit_tcredito_id').value = this.dataset.id;
            document.getElementById('edit_tcredito_tipo').value = this.dataset.tipo;
            document.getElementById('edit_tcredito_abreviatura').value = this.dataset.abreviatura;
            document.getElementById('edit_tcredito_monto_maximo').value = this.dataset.monto_maximo;
            document.getElementById('edit_tcredito_num_cuotas').value = this.dataset.num_cuotas;
            document.getElementById('edit_tcredito_tasa_interes').value = this.dataset.tasa_interes;
            document.getElementById('edit_tcredito_aporte_minimo').value = this.dataset.aporte_minimo;
            document.getElementById('edit_tcredito_porcentaje_encaje').value = this.dataset.porcentaje_encaje;
            document.getElementById('edit_tcredito_gracia').value = this.dataset.gracia;
            document.getElementById('edit_tcredito_porcentaje_mora').value = this.dataset.porcentaje_mora;
            document.getElementById('edit_tcredito_estado').checked = this.dataset.estado === "True" || this.dataset.estado === "1";
            var modal = new bootstrap.Modal(document.getElementById('modalEditarTipoCredito'));
            modal.show();
        });
    });

    // Eliminar Tipo de Crédito
    document.querySelectorAll('.btn-action-delete-tcredito').forEach(btn => {
        btn.addEventListener('click', function () {
            const id = this.dataset.id;
            if (confirm('¿Está seguro de eliminar este tipo de crédito?')) {
                fetch(`/administracion/tipos-credito/eliminar/${id}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCSRFToken()
                    }
                }).then(response => {
                    if (response.ok) {
                        location.reload();
                    } else {
                        alert('Error al eliminar el tipo de crédito.');
                    }
                }).catch(() => {
                    alert('Error de red. Intente nuevamente.');
                });
            }
        });
    });

    // Enviar formulario de edición por AJAX
    const formEditarTCredito = document.getElementById('formEditarTipoCredito');
    if (formEditarTCredito) {
        formEditarTCredito.addEventListener('submit', function (e) {
            e.preventDefault();
            const id = document.getElementById('edit_tcredito_id').value;
            const formData = new FormData(this);
            fetch(`/administracion/tipos-credito/editar/${id}/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCSRFToken()
                }
            }).then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    alert('Error al editar el tipo de crédito.');
                }
            }).catch(() => {
                alert('Error de red. Intente nuevamente.');
            });
        });
    }

    // Editar Tipo de Ahorro Futuro
    document.querySelectorAll('.btn-action-edit-tafuturo').forEach(btn => {
        btn.addEventListener('click', function () {
            document.getElementById('edit_tafuturo_id').value = this.dataset.id;
            document.getElementById('edit_tafuturo_abreviatura').value = this.dataset.abreviatura;
            document.getElementById('edit_tafuturo_tipo').value = this.dataset.tipo;
            document.getElementById('edit_tafuturo_v_inicial').value = this.dataset.v_inicial;
            document.getElementById('edit_tafuturo_v_periodico').value = this.dataset.v_periodico;
            document.getElementById('edit_tafuturo_plazo').value = this.dataset.plazo;
            document.getElementById('edit_tafuturo_penalizacion').value = this.dataset.penalizacion;
            document.getElementById('edit_tafuturo_estado').checked = this.dataset.estado === "True" || this.dataset.estado === "1";
            var modal = new bootstrap.Modal(document.getElementById('modalEditarTiposAFuturo'));
            modal.show();
        });
    });

    // Eliminar Tipo de Ahorro Futuro
    document.querySelectorAll('.btn-action-delete-tafuturo').forEach(btn => {
        btn.addEventListener('click', function () {
            const id = this.dataset.id;
            if (confirm('¿Está seguro de eliminar este registro?')) {
                fetch(`/administracion/tipos-ahorrofuturo/eliminar/${id}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCSRFToken()
                    }
                }).then(response => {
                    if (response.ok) {
                        location.reload();
                    } else {
                        alert('Error al eliminar el tipo de ahorro futuro.');
                    }
                }).catch(() => {
                    alert('Error de red. Intente nuevamente.');
                });
            }
        });
    });

    // Enviar formulario de edición por AJAX
    const formEditarTAFuturo = document.getElementById('formEditarTiposAFuturo');
    if (formEditarTAFuturo) {
        formEditarTAFuturo.addEventListener('submit', function (e) {
            e.preventDefault();
            const id = document.getElementById('edit_tafuturo_id').value;
            const formData = new FormData(this);
            fetch(`/administracion/tipos-ahorrofuturo/editar/${id}/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCSRFToken()
                }
            }).then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    alert('Error al editar el tipo de ahorro futuro.');
                }
            }).catch(() => {
                alert('Error de red. Intente nuevamente.');
            });
        });
    }

    // Editar Plazo Fijo
    document.querySelectorAll('.btn-action-edit-plazofijo').forEach(btn => {
        btn.addEventListener('click', function () {
            document.getElementById('edit_pf_id').value = this.dataset.id;
            document.getElementById('edit_pf_descripcion').value = this.dataset.descripcion;
            document.getElementById('edit_pf_monto').value = this.dataset.monto;
            document.getElementById('edit_pf_plazo').value = this.dataset.plazo;
            document.getElementById('edit_pf_tasa_interes').value = this.dataset.tasa_interes;
            document.getElementById('edit_pf_fecha_vencimiento').value = this.dataset.fecha_vencimiento;
            document.getElementById('edit_pf_estado').checked = this.dataset.estado === "True" || this.dataset.estado === "1";
            var modal = new bootstrap.Modal(document.getElementById('modalEditarPlazoFijo'));
            modal.show();
        });
    });

    // Eliminar PLazo Fijo
    document.querySelectorAll('.btn-action-delete-plazofijo').forEach(btn => {
        btn.addEventListener('click', function () {
            const id = this.dataset.id;
            if (confirm('¿Está seguro de eliminar este registro?')) {
                fetch(`/administracion/plazo-fijo/eliminar/${id}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCSRFToken()
                    }
                }).then(response => {
                    if (response.ok) {
                        location.reload();
                    } else {
                        response.json().then(data => {
                            alert(data.error || 'Error al eliminar el registro.');
                        });
                    }
                }).catch(() => {
                    alert('Error de red. Intente nuevamente.');
                });
            }
        });
    });

    // Enviar formulario de edición por AJAX
    const formEditarPFijo = document.getElementById('formEditarPlazoFijo');
    if (formEditarPFijo) {
        formEditarPFijo.addEventListener('submit', function (e) {
            e.preventDefault();
            const id = document.getElementById('edit_pf_id').value;
            const formData = new FormData(this);
            fetch(`/administracion/plazo-fijo/editar/${id}/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCSRFToken()
                }
            }).then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    response.json().then(data => {
                        alert(data.error || 'Error al editar el registro.');
                    });
                }
            }).catch(() => {
                alert('Error de red. Intente nuevamente.');
            });
        });
    }

    // Editar Interes en Ahorros
    document.querySelectorAll('.btn-action-edit-iahorro').forEach(btn => {
        btn.addEventListener('click', function () {
            document.getElementById('edit_iahorro_id').value = this.dataset.id;
            document.getElementById('edit_iahorro_tipo').value = this.dataset.tipo;
            document.getElementById('edit_iahorro_v_minimo').value = this.dataset.v_minimo;
            document.getElementById('edit_iahorro_v_maximo').value = this.dataset.v_maximo;
            document.getElementById('edit_iahorro_rendimiento').value = this.dataset.rendimiento;
            document.getElementById('edit_iahorro_estado').checked = this.dataset.estado === "True" || this.dataset.estado === "1";
            var modal = new bootstrap.Modal(document.getElementById('modalEditarInteresAhorro'));
            modal.show();
        });
    });

    // Eliminar Interes en Ahorros
    document.querySelectorAll('.btn-action-delete-iahorro').forEach(btn => {
        btn.addEventListener('click', function () {
            const id = this.dataset.id;
            if (confirm('¿Está seguro de eliminar este registro?')) {
                fetch(`/administracion/interes-ahorros/eliminar/${id}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCSRFToken()
                    }
                }).then(response => {
                    if (response.ok) {
                        location.reload();
                    } else {
                        alert('Error al eliminar registro.');
                    }
                }).catch(() => {
                    alert('Error de red. Intente nuevamente.');
                });
            }
        });
    });

    // Enviar formulario de edición por AJAX 
    const formEditarInteresAhorro = document.getElementById('formEditarInteresAhorro');
    if (formEditarInteresAhorro) {
        formEditarInteresAhorro.addEventListener('submit', function (e) {
            e.preventDefault();
            const id = document.getElementById('edit_iahorro_id').value;
            const formData = new FormData(this);
            fetch(`/administracion/interes-ahorros/editar/${id}/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCSRFToken()
                }
            }).then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    alert('Error al editar el interés en ahorros.');
                }
            }).catch(() => {
                alert('Error de red. Intente nuevamente.');
            });
        });
    }

    //Editar Interes a Futuro
    document.querySelectorAll('.btn-action-edit-iafuturo').forEach(btn => {
        btn.addEventListener('click', function () {
            document.getElementById('edit_iafuturo_id').value = this.dataset.id;
            document.getElementById('edit_iafuturo_tipo').value = this.dataset.tipo;
            document.getElementById('edit_iafuturo_rendimiento').value = this.dataset.rendimiento;
            document.getElementById('edit_iafuturo_v_minimo').value = this.dataset.v_minimo;
            document.getElementById('edit_iafuturo_v_maximo').value = this.dataset.v_maximo;
            document.getElementById('edit_iafuturo_estado').checked = this.dataset.estado === "True" || this.dataset.estado === "1";
            var modal = new bootstrap.Modal(document.getElementById('modalEditarInteresAFuturo'));
            modal.show();
        });
    });

    // Eliminar Interes a Futuro
    document.querySelectorAll('.btn-action-delete-iafuturo').forEach(btn => {
        btn.addEventListener('click', function () {
            const id = this.dataset.id;
            if (confirm('¿Está seguro de eliminar este registro?')) {
                fetch(`/administracion/interes-ahorrofuturo/eliminar/${id}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCSRFToken()
                    }
                }).then(response => {
                    if (response.ok) {
                        location.reload();
                    } else {
                        alert('Error al eliminar el interés a futuro.');
                    }
                }).catch(() => {
                    alert('Error de red. Intente nuevamente.');
                });
            }
        });
    });

    // Enviar formulario de edición por AJAX
    const formEditarInteresAFuturo = document.getElementById('formEditarInteresAFuturo');
    if (formEditarInteresAFuturo) {
        formEditarInteresAFuturo.addEventListener('submit', function (e) {
            e.preventDefault();
            const id = document.getElementById('edit_iafuturo_id').value;
            const formData = new FormData(this);
            fetch(`/administracion/interes-ahorrofuturo/editar/${id}/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCSRFToken()
                }
            }).then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    alert('Error al editar el interés a futuro.');
                }
            }).catch(() => {
                alert('Error de red. Intente nuevamente.');
            });
        });
    }


    // Validación de formulario de crédito 
    const creditoForm = document.getElementById("creditoForm");
    if (creditoForm) {
        creditoForm.addEventListener("submit", function (event) {
            let nombre = document.getElementById("id_nombre").value.trim();
            let tipoCredito = document.getElementById("id_tipo_credito").value;
            let monto = document.getElementById("id_monto").value;
            let meses = document.getElementById("id_meses").value;
            let valido = true;

            if (nombre === "") {
                document.getElementById("errorNombre").classList.remove("d-none");
                valido = false;
            } else {
                document.getElementById("errorNombre").classList.add("d-none");
            }

            if (tipoCredito === "") {
                document.getElementById("errorTipoCredito").classList.remove("d-none");
                valido = false;
            } else {
                document.getElementById("errorTipoCredito").classList.add("d-none");
            }

            if (monto <= 0 || isNaN(monto)) {
                document.getElementById("errorMonto").classList.remove("d-none");
                valido = false;
            } else {
                document.getElementById("errorMonto").classList.add("d-none");
            }

            if (meses < 1 || isNaN(meses)) {
                document.getElementById("errorMeses").classList.remove("d-none");
                valido = false;
            } else {
                document.getElementById("errorMeses").classList.add("d-none");
            }

            if (!valido) {
                event.preventDefault(); // Evita el envío si hay errores
            }
        });
    }
});

// CSRF universal
function getCSRFToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute('content') : '';
}

// Funciones simulación 
function guardarSimulacion() {
    alert("Simulación guardada correctamente.");
}

function enviarSimulacion() {
    alert("Simulación enviada.");
}

function descargarSimulacion() {
    alert("Simulación descargada como PDF.");
}

/*-----------------------------------------------------------------------------------
                            OPERATIVO
-----------------------------------------------------------------------------------*/

// EDITAR SOCIO
    document.querySelectorAll('.btn-action-edit-socio').forEach(button => {
        button.addEventListener('click', function () {
            const data = this.dataset;

            document.getElementById('edit-socio_id').value = data.id;
            document.getElementById('edit-last_name').value = data.apellidos;
            document.getElementById('edit-first_name').value = data.nombres;
            document.getElementById('edit-estado_civil').value = data.estado_civil;
            document.getElementById('edit-fecha_nacimiento').value = data.fecha_nacimiento;
            document.getElementById('edit-cedula').value = data.cedula;
            document.getElementById('edit-fecha_caducidad').value = data.fecha_caducidad;
            document.getElementById('edit-telefono').value = data.telefono;
            document.getElementById('edit-email').value = data.email;
            document.getElementById('edit-rol').value = data.rol;
            document.getElementById('edit-trabajo').value = data.trabajo;
            document.getElementById('edit-fecha_ingreso').value = data.fecha_ingreso;
            document.getElementById('edit-ciudad').value = data.ciudad;
            document.getElementById('edit-direccion').value = data.direccion;
            document.getElementById('edit-masculino').checked = false;
            document.getElementById('edit-femenino').checked = false;
            if (data.genero === 'M') {
                document.getElementById('edit-masculino').checked = true;
            } else if (data.genero === 'F') {
                document.getElementById('edit-femenino').checked = true;
            }

            if (data.nombramiento === 'Titular') {
                document.getElementById('edit-titular').checked = true;
            } else if (data.nombramiento === 'Contrato') {
                document.getElementById('edit-acontrato').checked = true;
            }
            document.getElementById('edit-estado').checked = data.estado === 'true';

            new bootstrap.Modal(document.getElementById('editSocioModal')).show();
        });
    });

    // ELIMIAR SOCIO
    document.querySelectorAll('.btn-action-delete-socio').forEach(button => {
        button.addEventListener('click', function () {
            const socioId = this.dataset.id;
            const socioName = this.dataset.nombre;

            document.getElementById('delete-socio-id').value = socioId;
            document.getElementById('delete-socio-name').textContent = socioName;

            new bootstrap.Modal(document.getElementById('deleteSocioModal')).show();
        });
    });


