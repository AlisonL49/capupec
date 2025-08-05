import re
from django.shortcuts import redirect
from django.urls import resolve
from django.conf import settings

class RoleAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs públicas permitidas sin autenticación
        public_paths = [
            '/login/',
            '/logout/',
        ]
        
        if not request.user.is_authenticated and request.path not in public_paths:
            return redirect(f'{settings.LOGIN_URL}?next={request.path}')

        response = self.get_response(request)
        
        if request.user.is_authenticated:
            user_role = getattr(getattr(request.user, 'rol', None), 'rol_nombre', '').lower()

            resolved_url = resolve(request.path_info)
            
            # Definir permisos por rol
            role_permissions = {
                'administrador': ['/administracion/','/operativo/', '/contabilidad/','/socios/','/usuarios/'],
                'socio': ['/socios/']
            }

            ruta_actual = request.path

            # Verificar acceso
            if not any(ruta_actual.startswith(path) for path in role_permissions.get(user_role, [])):
                return redirect('acceso-denegado')

        return self.get_response(request)