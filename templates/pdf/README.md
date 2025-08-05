# Estructura Modular para Reportes PDF

Esta estructura permite crear reportes PDF reutilizando componentes comunes como encabezado, footer y firmas.

## Archivos de la estructura:

### 1. Archivos base:
- `base_reporte.html` - Template base que incluye todos los componentes
- `partials/styles.html` - Estilos CSS para todos los reportes
- `partials/header.html` - Encabezado reutilizable
- `partials/footer.html` - Footer reutilizable  
- `partials/firmas.html` - Sección de firmas reutilizable

### 2. Archivos específicos:
- `reporte_socios.html` - Reporte específico de socios
- `ejemplo_reporte.html` - Ejemplo de cómo crear nuevos reportes

## Cómo crear un nuevo reporte:

### 1. Crear el template del reporte:
```html
{% extends 'pdf/base_reporte.html' %}

{% block contenido_reporte %}
    <!-- Tu contenido específico aquí -->
    <div class="table-container">
        <div class="table-title">TÍTULO DE TU REPORTE</div>
        
        <table>
            <thead>
                <tr>
                    <th>COLUMNA 1</th>
                    <th>COLUMNA 2</th>
                </tr>
            </thead>
            <tbody>
                {% for item in datos %}
                <tr>
                    <td>{{ item.campo1 }}</td>
                    <td>{{ item.campo2 }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
{% endblock %}
```

### 2. En la vista de Django:
```python
def mi_reporte_pdf(request):
    # Obtener datos
    datos = MiModelo.objects.all()
    
    # Cargar logo (opcional)
    logo_base64 = cargar_logo()
    
    # Renderizar template
    html_string = render_to_string('pdf/mi_reporte.html', {
        'datos': datos,
        'representantes': Representantes.objects.first(),
        'fecha_generacion': datetime.now().strftime('%d/%m/%Y %H:%M'),
        'logo_base64': logo_base64,
        'titulo_reporte': 'MI REPORTE PERSONALIZADO',
        'titulo_documento': 'Mi Reporte - CAPUPEC',
        'info_adicional': f'Total de registros: {datos.count()}',
    })
    
    # Generar PDF
    pdf_file = HTML(string=html_string).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="mi_reporte.pdf"'
    return response
```

## Variables disponibles en todos los templates:

### Variables requeridas:
- `fecha_generacion` - Fecha y hora de generación
- `titulo_reporte` - Título que aparece en el encabezado
- `titulo_documento` - Título del documento HTML

### Variables opcionales:
- `logo_base64` - Logo en base64 para el encabezado
- `representantes` - Objeto con datos de representantes para firmas
- `info_adicional` - Información adicional para el footer

## Estilos CSS disponibles:

### Clases para tablas:
- `table-container` - Contenedor de tabla
- `table-title` - Título de la tabla
- `estado-activo` - Texto verde para estados activos
- `estado-inactivo` - Texto rojo para estados inactivos

### Clases para información:
- `info-section` - Sección de estadísticas
- `info-item` - Item individual de estadística
- `total`, `activos`, `inactivos` - Colores específicos

### Clases para contenido:
- `no-data` - Mensaje cuando no hay datos
- `page-break` - Forzar salto de página

## Personalización de estilos:

Los estilos están en `partials/styles.html` y pueden modificarse para cambiar:
- Colores corporativos
- Tipografías
- Espaciados
- Bordes de tabla
- Tamaños de página

## Ejemplo de tabla con estilo actual:
- Solo líneas horizontales de separación
- Bordes izquierdo y derecho externos únicamente
- Encabezado gris (#6c757d)
- Filas alternadas en gris claro
- Sin bordes verticales internos