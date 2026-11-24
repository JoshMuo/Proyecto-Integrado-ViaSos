import io, secrets, re
from urllib.parse import quote
import qrcode
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Perfil, Contacto, CodigoQR, Notificacion, Soporte, Configuracion, Pregunta

# Devuelve el usuario autenticado o None si no existe una sesión válida.
def me(request): return request.user if request.user.is_authenticated and request.user.is_active else None

# Todas las pantallas de ViaSOS se renderizan desde un único archivo HTML.
def page(request, section, context=None):
 data = {'section': section}
 if context:
  data.update(context)
 return render(request, 'viasos.html', data)

# INICIO: entrega la sección de bienvenida del HTML único.
# INICIO: entrega la sección de bienvenida del HTML único.
# INICIO: entrega la sección de bienvenida del HTML único.
def home(request): return page(request, 'home')
# REGISTRO: valida los campos, crea el usuario Django y su perfil ViaSOS.
# REGISTRO: valida los campos, crea el usuario Django y su perfil ViaSOS.
# REGISTRO: valida los campos, crea el usuario Django y su perfil ViaSOS.
def register(request):
 if request.method=='POST':
  n=request.POST.get('name','').strip(); s=request.POST.get('surname','').strip(); e=request.POST.get('email','').strip().lower(); p=request.POST.get('password','')
  if not all([n, s, e, p]) or p != request.POST.get('confirm'):
   messages.error(request, 'Completa los campos y verifica la contraseña.')
  elif len(p) < 10:
   messages.error(request, 'La contraseña debe tener al menos 10 caracteres.')
  elif User.objects.filter(username=e).exists():
   messages.error(request, 'Ese correo ya está registrado.')
  else:
   u=User.objects.create_user(username=e,email=e,password=p,first_name=n,last_name=s); Perfil.objects.create(user=u); login(request,u); return redirect('dashboard')
 return page(request, 'register')
# AUTENTICACIÓN: verifica correo/contraseña con el backend de autenticación Django.
# AUTENTICACIÓN: verifica correo/contraseña con el backend de autenticación Django.
# AUTENTICACIÓN: verifica correo y contraseña con Django.
def login_view(request):
 if request.method=='POST':
  e=request.POST.get('email','').strip().lower(); u=authenticate(request,username=e,password=request.POST.get('password',''))
  if u: login(request,u); return redirect('admin_dashboard' if u.viasos.role=='admin' else 'dashboard')
  messages.error(request,'Correo o contraseña incorrectos.')
 return page(request, 'login')
# CIERRE DE SESIÓN: elimina la sesión autenticada y vuelve al inicio.
# CIERRE DE SESIÓN: elimina la sesión autenticada y vuelve al inicio.
# CIERRE DE SESIÓN: elimina la sesión autenticada.
def logout_view(request): logout(request); return redirect('home')
# PANEL: carga exclusivamente los datos pertenecientes al usuario conectado.
# PANEL: carga exclusivamente los datos pertenecientes al usuario conectado.
# PANEL: carga los registros que pertenecen al usuario conectado.
def dashboard(request):
 u=me(request)
 if not u:return redirect('login')
 if u.viasos.role=='admin':return redirect('admin_dashboard')
 return page(request, 'dashboard', {'profile':u.viasos,'contacts':Contacto.objects.filter(user=u).order_by('position'),'qrs':CodigoQR.objects.filter(user=u).order_by('-created_at'),'notifications':Notificacion.objects.filter(user=u).order_by('-created_at')[:10],'tickets':Soporte.objects.filter(user=u).order_by('-created_at')[:5]})
@require_POST
# PERFIL: guarda los datos médicos/personales y sus permisos de publicación.
# PERFIL: guarda los datos personales y sus permisos de publicación.
# PERFIL: guarda datos personales y permisos para mostrarlos en la ficha QR.
def save_profile(request):
 u=me(request)
 if not u:return redirect('login')
 p=u.viasos
 for f in ['phone','address','birth_date','allergies','conditions','medications','blood_type','other']: setattr(p,f,request.POST.get(f,'').strip())
 for f in ['phone','address','birth_date','allergies','conditions','medications','blood_type','other']: setattr(p,'public_'+f,request.POST.get('public_'+f)=='on')
 p.save(); messages.success(request,'Información guardada.'); return redirect('/panel/#informacion')
@require_POST
# CONTACTOS: agrega un contacto privado respetando el máximo de tres.
# CONTACTOS: agrega un contacto privado respetando el máximo de tres.
# CONTACTOS: agrega un contacto privado con límite de tres.
def add_contact(request):
 u=me(request)
 if not u:return redirect('login')
 if Contacto.objects.filter(user=u).count()>=3: messages.error(request,'Máximo 3 contactos.')
 else: Contacto.objects.create(user=u,name=request.POST.get('name',''),phone=request.POST.get('phone',''),relationship=request.POST.get('relationship','Otro familiar'),position=Contacto.objects.filter(user=u).count()+1)
 return redirect('/panel/#contactos')
@require_POST
# CONTACTOS: elimina un contacto del propietario y reordena posiciones.
# CONTACTOS: elimina un contacto del propietario y reordena posiciones.
# CONTACTOS: elimina un contacto y vuelve a ordenar los restantes.
def delete_contact(request,pk):
 u=me(request); c=get_object_or_404(Contacto,pk=pk,user=u); c.delete()
 for i,x in enumerate(Contacto.objects.filter(user=u).order_by('id'),1): x.position=i; x.save()
 return redirect('/panel/#contactos')
@require_POST
# QR: genera un token aleatorio y crea un código para el usuario conectado.
# QR: genera un token aleatorio y crea un código para el usuario conectado.
# QR: genera un token aleatorio y crea el código del usuario.
def create_qr(request):
 u=me(request)
 if not u:return redirect('login')
 if CodigoQR.objects.filter(user=u).count()>=3: messages.error(request,'Máximo 3 códigos QR.')
 else: CodigoQR.objects.create(user=u,token=secrets.token_urlsafe(18),name=request.POST.get('name') or 'Mi QR',description=request.POST.get('description',''))
 return redirect('/panel/#qrs')
@require_POST
# QR: alterna el estado activo/suspendido del código del propietario.
# QR: alterna el estado activo/suspendido del código del propietario.
# QR: cambia entre activo y suspendido.
def toggle_qr(request,token):
 u=me(request); q=get_object_or_404(CodigoQR,user=u,token=token); q.active=not q.active; q.save(); return redirect('/panel/#qrs')
@require_POST
# QR: elimina el código QR que pertenece al usuario conectado.
# QR: elimina el código QR que pertenece al usuario conectado.
# QR: elimina el código perteneciente al usuario conectado.
def delete_qr(request,token):
 u=me(request); get_object_or_404(CodigoQR,user=u,token=token).delete(); return redirect('/panel/#qrs')
# QR: construye la dirección pública que se codifica dentro de la imagen.
# QR: construye la dirección pública que se codifica dentro de la imagen.
# QR: construye la dirección pública que se guarda dentro de la imagen.
def qr_target(request,token): return request.build_absolute_uri(f'/qr/{token}/')
# QR: genera la imagen PNG descargable a partir de la dirección pública.
# QR: genera la imagen PNG descargable a partir de la dirección pública.
# QR: genera y devuelve el archivo PNG del código.
def qr_image(request,token):
 u=me(request); q=get_object_or_404(CodigoQR,user=u,token=token); img=qrcode.make(qr_target(request,token)); b=io.BytesIO(); img.save(b,format='PNG'); r=HttpResponse(b.getvalue(),content_type='image/png'); r['Content-Disposition']=f'attachment; filename="viasos_{token}.png"'; return r
# FICHA PÚBLICA: muestra solo campos autorizados y QR activo.
# FICHA PÚBLICA: muestra solo campos autorizados y QR activo.
# FICHA PÚBLICA: muestra solo campos autorizados y códigos activos.
def public_profile(request,token):
 q=get_object_or_404(CodigoQR,token=token,active=True,user__is_active=True); u=q.user; p=u.viasos
 return page(request, 'public_profile', {'owner':u,'p':p})
# SOPORTE: registra una solicitud y genera una notificación para el usuario.
# SOPORTE: registra una solicitud y genera una notificación para el usuario.
# SOPORTE: crea la solicitud y una notificación para el usuario.
def create_ticket(request):
 u=me(request)
 if not u:return redirect('login')
 if request.method=='POST': Soporte.objects.create(user=u,subject=request.POST.get('subject',''),body=request.POST.get('body','')); Notificacion.objects.create(user=u,text='Tu solicitud de soporte fue recibida.')
 return redirect('/panel/#soporte')
# SEGURIDAD: comprueba que la sesión corresponda al rol administrador de ViaSOS.
# SEGURIDAD: comprueba que la sesión corresponda al rol administrador de ViaSOS.
# SEGURIDAD: comprueba el rol de administrador propio de ViaSOS.
def admin_required(request):
 u = me(request)
 return bool(u and hasattr(u, 'viasos') and u.viasos.role == 'admin')
# ADMIN VIA SOS: presenta usuarios y solicitudes de soporte.
# ADMIN VIA SOS: presenta usuarios y solicitudes de soporte.
# ADMIN VIA SOS: presenta usuarios y solicitudes recibidas.
def admin_dashboard(request):
 if not admin_required(request):return redirect('login')
 return page(request, 'admin', {'users':User.objects.filter(viasos__role='user'),'tickets':Soporte.objects.select_related('user').order_by('-created_at')})
# ADMIN USUARIOS: reutiliza el resumen administrativo de usuarios.
# ADMIN USUARIOS: reutiliza el resumen administrativo de usuarios.
# ADMIN USUARIOS: utiliza el resumen administrativo.
def admin_users(request): return admin_dashboard(request)
@require_POST
# ADMIN USUARIOS: activa/suspende una cuenta y sus códigos QR.
# ADMIN USUARIOS: activa/suspende una cuenta y sus códigos QR.
# ADMIN USUARIOS: suspende/reactiva una cuenta y sus códigos QR.
def admin_toggle_user(request,pk):
 if not admin_required(request):return redirect('login')
 u=get_object_or_404(User,pk=pk); u.is_active=not u.is_active; u.save(); CodigoQR.objects.filter(user=u).update(active=u.is_active); return redirect('admin_dashboard')
# ADMIN CONFIGURACIÓN: consulta y guarda el modo de demostración de WhatsApp.
# ADMIN CONFIGURACIÓN: consulta y guarda el modo de demostración de WhatsApp.
# ADMIN CONFIGURACIÓN: lee y guarda el modo de contacto configurado.
def admin_settings(request):
 if not admin_required(request): return redirect('login')
 setting, _ = Configuracion.objects.get_or_create(key='whatsapp_mode', defaults={'value':'simulation'})
 if request.method == 'POST':
  setting.value = request.POST.get('whatsapp_mode', 'simulation')
  setting.save()
  messages.success(request, 'Configuración guardada.')
 return page(request, 'settings', {'mode': setting.value})
# ADMIN SOPORTE: lista solicitudes para su revisión.
# ADMIN SOPORTE: lista solicitudes para su revisión.
# ADMIN SOPORTE: lista solicitudes para revisión.
def admin_support(request):
 if not admin_required(request): return redirect('login')
 return page(request, 'support', {'tickets': Soporte.objects.select_related('user').order_by('-created_at')})
@require_POST
# ADMIN SOPORTE: guarda estado/respuesta y notifica al usuario.
# ADMIN SOPORTE: guarda estado/respuesta y notifica al usuario.
# ADMIN SOPORTE: actualiza el ticket y notifica al usuario si hay respuesta.
def admin_update_ticket(request,pk):
 if not admin_required(request):return redirect('login')
 t=get_object_or_404(Soporte,pk=pk); t.status=request.POST.get('status','pending'); t.reply=request.POST.get('reply',''); t.save(); Notificacion.objects.create(user=t.user,text='Respuesta de soporte: '+t.reply) if t.reply else None; return redirect('admin_dashboard')
# DETALLE QR: muestra la imagen del código al propietario autenticado.
# DETALLE QR: muestra la imagen del código al propietario autenticado.
# DETALLE QR: muestra al propietario el QR seleccionado.
def qr_detail(request,token):
 u=me(request)
 if not u:return redirect('login')
 q=get_object_or_404(CodigoQR,user=u,token=token); return page(request, 'qr_detail', {'qr':q})
