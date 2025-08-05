function inicializarAutocomplete(selector, url) {
    const input = document.querySelector(selector);

    // Crear lista de sugerencias si no existe
    let lista = document.createElement('ul');
    lista.classList.add('list-group');
    lista.style.position = 'absolute';
    lista.style.zIndex = '1000';
    lista.style.width = input.offsetWidth + 'px';
    lista.style.maxHeight = '200px';
    lista.style.overflowY = 'auto';
    lista.style.cursor = 'pointer';
    input.parentNode.appendChild(lista);
    lista.style.display = 'none';

    input.addEventListener('input', function () {
        const query = input.value;
        if (query.length < 2) {
            lista.innerHTML = '';
            lista.style.display = 'none';
            return;
        }

        fetch(`${url}?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                lista.innerHTML = '';
                if (data.length === 0) {
                    lista.style.display = 'none';
                    return;
                }
                data.forEach(usuario => {
                    const item = document.createElement('li');
                    item.classList.add('list-group-item', 'list-group-item-action');
                    item.textContent = usuario.nombre;
                    item.addEventListener('click', () => {
                        input.value = usuario.nombre;
                        lista.innerHTML = '';
                        lista.style.display = 'none';
                    });
                    lista.appendChild(item);
                });
                lista.style.display = 'block';
            })
            .catch(err => {
                console.error('Error en el autocompletado:', err);
            });
    });

    // Ocultar sugerencias cuando se hace clic fuera
    document.addEventListener('click', function (e) {
        if (!lista.contains(e.target) && e.target !== input) {
            lista.style.display = 'none';
        }
    });
}


function inicializarAutocompleteConId(inputSelector, urlBusqueda, hiddenInputSelector) {
    const input = document.querySelector(inputSelector);
    const hiddenInput = document.querySelector(hiddenInputSelector);

    let lista = document.createElement('ul');
    lista.classList.add('list-group');
    lista.style.position = 'absolute';
    lista.style.zIndex = '1000';
    lista.style.width = input.offsetWidth + 'px';
    lista.style.maxHeight = '200px';
    lista.style.overflowY = 'auto';
    lista.style.cursor = 'pointer';
    input.parentNode.appendChild(lista);
    lista.style.display = 'none';

    input.addEventListener('input', function () {
        const query = input.value;
        hiddenInput.value = '';  

        if (query.length < 2) {
            lista.innerHTML = '';
            lista.style.display = 'none';
            return;
        }

        fetch(`${urlBusqueda}?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                lista.innerHTML = '';
                if (data.length === 0) {
                    lista.style.display = 'none';
                    return;
                }
                data.forEach(usuario => {
                    const item = document.createElement('li');
                    item.classList.add('list-group-item', 'list-group-item-action');
                    item.textContent = usuario.nombre;
                    item.addEventListener('click', () => {
                        input.value = usuario.nombre;
                        hiddenInput.value = usuario.id;  
                        lista.innerHTML = '';
                        lista.style.display = 'none';
                    });
                    lista.appendChild(item);
                });
                lista.style.display = 'block';
            })
            .catch(err => {
                console.error('Error en autocompletado con ID:', err);
            });
    });

    document.addEventListener('click', function (e) {
        if (!lista.contains(e.target) && e.target !== input) {
            lista.style.display = 'none';
        }
    });
}


function inicializarAutocompleteAhorros(selector, url, campos) {
    const input = document.querySelector(selector);
    let lista = document.createElement('ul');
    lista.classList.add('list-group');
    lista.style.position = 'absolute';
    lista.style.zIndex = '1000';
    lista.style.width = input.offsetWidth + 'px';
    lista.style.maxHeight = '200px';
    lista.style.overflowY = 'auto';
    lista.style.cursor = 'pointer';
    input.parentNode.appendChild(lista);
    lista.style.display = 'none';

    input.addEventListener('input', function () {
        const query = input.value.trim();
        if (query.length < 2) {
            lista.innerHTML = '';
            lista.style.display = 'none';
            return;
        }

        fetch(`${url}?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                lista.innerHTML = '';
                if (data.length === 0) {
                    lista.style.display = 'none';
                    return;
                }
                data.forEach(usuario => {
                    const item = document.createElement('li');
                    item.classList.add('list-group-item', 'list-group-item-action');
                    item.textContent = `${usuario.nombre}`;
                    item.addEventListener('click', () => {
                        input.value = usuario.nombre;
                        lista.innerHTML = '';
                        lista.style.display = 'none';

                        // Llenar los campos del formulario
                        document.querySelector(campos.noSocio).value = usuario.id;
                        document.querySelector(campos.noSocioHidden).value = usuario.id;
                        document.querySelector(campos.identificacion).value = usuario.cedula;
                        document.querySelector(campos.nombres).value = usuario.nombre;
                        document.querySelector(campos.nombramiento).value = usuario.nombramiento;
                        document.querySelector(campos.lugarTrabajo).value = usuario.lugarTrabajo;
                        document.querySelector(campos.fechaApertura).value = usuario.fechaApertura;
                        document.querySelector(campos.saldo).value = usuario.saldo;
                    });
                    lista.appendChild(item);
                });
                lista.style.display = 'block';
            })
            .catch(err => {
                console.error('Error en el autocompletado:', err);
            });
    });

    document.addEventListener('click', function (e) {
        if (!lista.contains(e.target) && e.target !== input) {
            lista.style.display = 'none';
        }
    });
}

