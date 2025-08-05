document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('formAhorros');
    const btnGuardar = document.getElementById('btnGuardar');
    const btnCrearCuenta = document.getElementById('btnCrearCuenta');

    if (form && btnCrearCuenta) {
        btnCrearCuenta.addEventListener('click', function (e) {
            e.preventDefault();
            document.getElementById('accion').value = 'crear_cuenta';
            form.submit();
        });
    }

    if (form && btnGuardar) {
        btnGuardar.addEventListener('click', function (e) {
            e.preventDefault();

            const socioId = document.getElementById('noSocio').value;
            const valor = parseFloat(document.getElementById('valorAporte').value).toFixed(2);
            const tieneCuenta = document.getElementById('noSocioHidden').value;
            const nombres = document.getElementById('nombres').value;

            if (!socioId ) {
                alert('Por favor, seleccione un socio');
                return;
            }
            if (isNaN(valor) || valor <= 0) {
                alert('Por favor, seleccione un valor válido.');
                return;
            }
            

            if (!tieneCuenta || saldo === '') {
                alert('El socio no tiene una cuenta de ahorros. Cree una antes de registrar aportes');
                return;
            }


            if (!confirm(`¿Desea registrar un aporte de $${valor}? para el socio ${nombres}`)) {
                return;
            }

            const formData = new FormData(form);

            fetch('registrar-aporte/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const iframe = document.getElementById('reciboIframe');
                    iframe.src = `recibo-pdf/${data.usuario_id}/${data.aporte}/`;
                    const modal = new bootstrap.Modal(document.getElementById('reciboModal'));
                    modal.show();
                    // Opcional: limpiar formulario
                    form.reset();
                } else {
                    alert('Error al guardar: ' + data.error);
                }
            })
            .catch(err => {
                alert('Error en la solicitud: ' + err);
            });
        });
    }
});
