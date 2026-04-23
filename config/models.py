from django.db import models


class Usuario(models.Model):
    usuario = models.CharField(
        max_length=30, blank=False, null=False, unique=True)
    contrasena = models.CharField(max_length=20, blank=False, null=False)
    categoria = models.CharField(max_length=30, blank=False, null=False)
    #nombre = models.CharField(max_length=30, blank=False, null=False)
    #apellido = models.CharField(max_length=30, blank=False, null=False)
    telefono = models.CharField(
        max_length=15, blank=False, null=False),
    #email = models.EmailField(unique=True)
    #direccion = models.CharField(max_length=30, null=False)
    ciudad = models.CharField(max_length=30, blank=False, null=False)
    codigo_postal = models.CharField(
        max_length=10, blank=False, null=False)
    #evaluar estado con choices
    #activo = models.BooleanField(default=True)
    verificado = models.BooleanField(default=False)
    ultimo_acceso = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Rol(models.Model):
    rol_name = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    nivel_acceso = models.IntegerField(default=1)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.rol_name


class Voluntario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    fecha_ingreso = models.DateField(blank=True, null=False)
    fecha_salida = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    disponibilidad = models.CharField(max_length=50, blank=True, null=True)
    especialidad = models.CharField(max_length=100, blank=True, null=True)
    horas_voluntariado = models.IntegerField(default=0)
    notas = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # usuario_id =
    # rol_id =

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Especie(models.Model):
    especie_id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Raza(models.Model):
    raza_id = models.BigAutoField(primary_key=True)
    especie_id = models.ForeignKey(
        Especie, on_delete=models.CASCADE,
        related_name='razas')
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Animal(models.Model):
    animal_id = models.BigAutoField(primary_key=True)
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    especie_id = models.ForeignKey(
        Especie, on_delete=models.PROTECT,
        related_name='animales')
    raza_id = models.ForeignKey(
        Raza, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='animales')
    #sexo = 
    fecha_nacimiento = models.DateField(blank=True, null=True)
    edad_aproximada = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    tamanio = models.CharField(max_length=20, blank=True, null=True)
    peso_kg = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)
    microchip = models.CharField(
        max_length=50, unique=True, blank=True, null=True)
    esterilizado = models.BooleanField(default=False)
    vacunado = models.BooleanField(default=False)
    desparasitado = models.BooleanField(default=False)
    estado_salud = models.CharField(max_length=50, default="bueno")
    enfermedades_cronicas = models.TextField(blank=True, null=True)
    alergias = models.TextField(blank=True, null=True)
    comportamiento = models.TextField(blank=True, null=True)
    historia = models.TextField(blank=True, null=True)
    necesidades_especiales = models.TextField(blank=True, null=True)
    fecha_ingreso = models.DateField()
    fecha_salida = models.DateField(blank=True, null=True)
    #estado =
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    foto_url = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class AnimalVoluntario(models.Model):
    animal_voluntario_id = models.BigAutoField(primary_key=True)
    animal_id = models.ForeignKey(
        Animal, on_delete=models.CASCADE,
        related_name='asignaciones_voluntario')
    voluntario_id = models.ForeignKey(
        Voluntario, on_delete=models.CASCADE,
        related_name='animales_asignados')
    tipo_asignacion = models.CharField(
        max_length=30, default="cuidador_principal")
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Adopcion(models.Model):
    adopcion_id = models.BigAutoField(primary_key=True)
    codigo_adopcion = models.CharField(max_length=50, unique=True)
    #usuario_id =
    #animal_id =
    #voluntario_id =
    fecha_solicitud = models.DateField()
    fecha_aprobacion = models.DateField(blank=True, null=True)
    fecha_adopcion = models.DateField(blank=True, null=True)
    #estado_solicitud =
    estado_adopcion = models.CharField(max_length=20, default="prueba")
    motivo_rechazo = models.TextField(blank=True, null=True)
    condiciones_especiales = models.TextField(blank=True, null=True)
    periodo_prueba_dias = models.IntegerField(default=30)
    costo_adopcion = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    pagado = models.BooleanField(default=False)
    contrato_firmado = models.BooleanField(default=False)
    seguimientos_realizados = models.IntegerField(default=0)
    notas = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.codigo_adopcion


class SeguimientoAdopcion(models.Model):
    seguimiento_id = models.BigAutoField(primary_key=True)
    #adopcion_id =
    #voluntario_id =
    fecha_seguimiento = models.DateField()
    tipo_seguimiento = models.CharField(max_length=20, default="llamada")
    estado_animal = models.CharField(max_length=100, blank=True, null=True)
    estado_adoptante = models.CharField(max_length=100, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    recomendaciones = models.TextField(blank=True, null=True)
    proxima_revision = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class TipoServicio(models.Model):
    tipo_servicio_id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    requiere_veterinario = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Incidencia(models.Model):
    incidencia_id = models.BigAutoField(primary_key=True)
    codigo_incidencia = models.CharField(max_length=50, unique=True)
    #animal_id =
    #voluntario_id =
    #tipo_servicio_id =
    servicio = models.CharField(max_length=50, blank=True, null=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    prioridad = models.CharField(max_length=10, default="media")
    estado = models.CharField(max_length=15, default="abierta")
    fecha_incidencia = models.DateField()
    fecha_resolucion = models.DateField(blank=True, null=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    veterinario_responsable = models.CharField(
        max_length=100, blank=True, null=True)
    tratamiento = models.TextField(blank=True, null=True)
    medicamentos = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CategoriaProducto(models.Model):
    categoria_id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    icono = models.CharField(max_length=50, blank=True, null=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Proveedor(models.Model):
    proveedor_id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    contacto = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Producto(models.Model):
    producto_id = models.BigAutoField(primary_key=True)
    codigo = models.CharField(max_length=50, unique=True)
    #categoria_id =

    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    unidad = models.CharField(max_length=50, default="unidad")
    stock_actual = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=10)
    stock_maximo = models.IntegerField(default=1000)
    precio_unitario = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    lote = models.CharField(max_length=50, blank=True, null=True)
    #proveedor_id =
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MovimientoInventario(models.Model):
    movimiento_id = models.BigAutoField(primary_key=True)
    #producto_id =
    tipo_movimiento = models.CharField(max_length=20)
    cantidad = models.IntegerField()
    stock_anterior = models.IntegerField()
    stock_nuevo = models.IntegerField()
    motivo = models.CharField(max_length=255, blank=True, null=True)
    referencia = models.CharField(max_length=100, blank=True, null=True)
    #voluntario_id =
    fecha_movimiento = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)


class SalidaDonacion(models.Model):
    salida_id = models.BigAutoField(primary_key=True)
    codigo_salida = models.CharField(max_length=50, unique=True)
    #voluntario_id =
    #producto_id =
    cantidad = models.IntegerField()
    destinatario = models.CharField(max_length=200, blank=True, null=True)
    motivo = models.TextField(blank=True, null=True)
    fecha_salida = models.DateField()
    aprobado = models.BooleanField(default=False)
    aprobado_por = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TipoDonacion(models.Model):
    tipo_donacion_id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Donacion(models.Model):
    donacion_id = models.BigAutoField(primary_key=True)
    codigo_donacion = models.CharField(max_length=50, unique=True)
    #usuario_id =
    ##voluntario_id =
    #tipo_donacion_id =
    tipo = models.CharField(max_length=20, default="productos")
    monto_monetario = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    descripcion = models.TextField(blank=True, null=True)
    fecha_donacion = models.DateField()
    comprobante = models.CharField(max_length=255, blank=True, null=True)
    deducible_impuestos = models.BooleanField(default=True)
    agradecimiento_enviado = models.BooleanField(default=False)
    notas = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.codigo_donacion


class DonacionProducto(models.Model):
    donacion_producto_id = models.BigAutoField(primary_key=True)
    #donacion_id =
    #producto_id =
    cantidad = models.IntegerField()
    valor_estimado = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    estado_producto = models.CharField(max_length=50, default="nuevo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ConfiguracionSistema(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre_organizacion = models.CharField(max_length=200, default="SafePaws")
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    sitio_web = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)
    dias_periodo_prueba_default = models.IntegerField(default=30)
    #costo_adopcion_default =
    dias_alerta_vencimiento = models.IntegerField(default=30)
    logo_url = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)


class Estadistica(models.Model):
    estadistica_id = models.BigAutoField(primary_key=True)
    tipo = models.CharField(max_length=50)
    valor = models.IntegerField()
    fecha = models.DateField()
    mes = models.IntegerField()
    anio = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class Notificacion(models.Model):
    notificacion_id = models.BigAutoField(primary_key=True)
    #usuario_id =
    tipo = models.CharField(max_length=20)
    titulo = models.CharField(max_length=200, blank=True, null=True)
    mensaje = models.TextField(blank=True, null=True)
    enlace = models.CharField(max_length=255, blank=True, null=True)
    leida = models.BooleanField(default=False)
    fecha_leida = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Reporte(models.Model):
    reporte_id = models.BigAutoField(primary_key=True)
    tipo_reporte = models.CharField(max_length=50)
    titulo = models.CharField(max_length=200, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    #generado_por =
    fecha_generacion = models.DateTimeField()
    formato = models.CharField(max_length=10, blank=True, null=True)
    archivo_url = models.CharField(max_length=255, blank=True, null=True)
    total_registros = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
