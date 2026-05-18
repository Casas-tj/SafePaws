from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils import timezone
from datetime import timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = "Seed completo de datos para todas las apps"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("==> Iniciando seed de datos..."))
        
        self.seed_users()
        self.seed_owners()
        self.seed_animals()
        self.seed_donaciones()
        self.seed_inventario()
        self.seed_health()
        self.seed_adopciones()
        
        self.stdout.write(self.style.SUCCESS("==> Seed completado!"))

    def seed_users(self):
        self.stdout.write("  [USUARIOS]")
        
        grupos = ['Administrador', 'Veterinario', 'Cuidador de Animales', 'Atención al Cliente']
        for g in grupos:
            Group.objects.get_or_create(name=g)
        
        roles = list(Group.objects.all())
        
        usuarios = [
            ('admin', 'Zuriñe', 'Casas', 'admin@safepaws.es', True),
            ('vet1', 'Dr. Mario', 'García', 'vet1@safepaws.es', False),
            ('vet2', 'Dra. Laura', 'López', 'vet2@safepaws.es', False),
            ('vol1', 'Carlos', 'Martín', 'vol1@safepaws.es', True),
            ('vol2', 'Ana', 'Rodríguez', 'vol2@safepaws.es', True),
            ('vol3', 'Pedro', 'Sánchez', 'vol3@safepaws.es', True),
            ('vol4', 'María', 'Fernández', 'vol4@safepaws.es', True),
            ('vol5', 'Juan', 'Gómez', 'vol5@safepaws.es', True),
            ('cuidador1', 'Lucía', 'Torres', 'cuidador1@safepaws.es', False),
            ('cuidador2', 'Jorge', 'Ruiz', 'cuidador2@safepaws.es', False),
            ('user1', 'Sofia', 'Benito', 'user1@test.com', False),
            ('user2', 'Miguel', 'Castro', 'user2@test.com', True),
            ('user3', 'Elena', 'Mora', 'user3@test.com', True),
            ('user4', 'David', 'Herrera', 'user4@test.com', False),
            ('user5', 'Carmen', 'Vega', 'user5@test.com', True),
            ('user6', 'Alejandro', 'Navarro', 'user6@test.com', False),
            ('user7', 'Patricia', 'Suárez', 'user7@test.com', True),
            ('user8', 'Fernando', 'Reyes', 'user8@test.com', True),
            ('user9', 'Isabel', 'Mendez', 'user9@test.com', False),
            ('user10', 'Roberto', 'Campos', 'user10@test.com', True),
        ]
        
        for username, first, last, email, is_vol in usuarios:
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password('123456')
                user.first_name = first
                user.last_name = last
                user.email = email
                user.is_volunteer = is_vol
                user.is_active = True
                user.save()
                if username == 'admin':
                    admin_group = Group.objects.get(name='Administrador')
                    user.groups.add(admin_group)
                else:
                    user.groups.add(random.choice(roles))
                self.stdout.write(f"    + {username}")

    def seed_owners(self):
        self.stdout.write("  [OWNERS]")
        
        owners = [
            ('Juan', 'Pérez García', 'juan.perez@email.com', '+34611111111', True, 'Calle Mayor 12, Madrid'),
            ('María', 'López Martínez', 'maria.lopez@email.com', '+34622222222', True, 'Avda. de la Paz 45, Barcelona'),
            ('Carlos', 'Rodríguez Sánchez', 'carlos.r@email.com', '+34633333333', False, 'Calle Sol 8, Valencia'),
            ('Ana', 'Fernández Torres', 'ana.f@email.com', '+34644444444', True, 'Plaza España 3, Sevilla'),
            ('Pedro', 'Gómez Ruiz', 'pedro.g@email.com', '+34655555555', True, 'Calle Luna 22, Bilbao'),
            ('Laura', 'Martín Castro', 'laura.m@email.com', '+34666666666', False, 'Avda. del Mar 67, Málaga'),
            ('Miguel', 'López Hidalgo', 'miguel.l@email.com', '+34677777777', True, 'Calle Sierra 15, Zaragoza'),
            ('Sofía', 'Ramírez Ortega', 'sofia.r@email.com', '+34688888888', True, 'Gran Vía 90, Murcia'),
            ('Javier', 'Morales Serrano', 'javier.m@email.com', '+34699999999', False, 'Calle Olmo 5, Palma'),
            ('Elena', 'Castillo Vega', 'elena.c@email.com', '+34700000000', True, 'Avda. Constitución 34, Alicante'),
            ('David', 'Navarro Gutiérrez', 'david.n@email.com', '+34711111111', True, 'Calle Real 11, La Coruña'),
            ('Carmen', 'Jiménez Flores', 'carmen.j@email.com', '+34722222222', False, 'Calle del Prado 78, Granada'),
            ('Alejandro', 'Muñoz Romero', 'alex.m@email.com', '+34733333333', True, 'Avda. América 50, Valladolid'),
            ('Patricia', 'Serrano Delgano', 'patricia.s@email.com', '+34744444444', True, 'Calle Jardín 9, Santander'),
            ('Fernando', 'Hernández Morales', 'fernando.h@email.com', '+34755555555', False, 'Plaza Mayor 2, Toledo'),
            ('Isabel', 'Garrido Ruiz', 'isabel.g@email.com', '+34766666666', True, 'Calle San Juan 14, Pamplona'),
            ('Roberto', 'Aguilar Torres', 'roberto.a@email.com', '+34777777777', True, 'Avda. de la Vega 28, Huelva'),
            ('Cristina', 'Vargas López', 'cristina.v@email.com', '+34788888888', False, 'Calle Norte 6, León'),
            ('Antonio', 'Cabrera Sánchez', 'antonio.c@email.com', '+34799999999', True, 'Calle del Sol 33, Cádiz'),
            ('María José', 'Peña Gutiérrez', 'mariaj.p@email.com', '+34800000000', True, 'Avda. Andalucía 55, Almería'),
        ]
        
        for name, last, email, phone, is_vol, address in owners:
            from apps.owners.models import Owner
            owner, created = Owner.objects.get_or_create(
                name=name, last_name=last,
                defaults={
                    'email': email,
                    'phone': phone,
                    'address': address,
                    'is_volunteer': is_vol,
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f"    + {name} {last}")

    def seed_animals(self):
        self.stdout.write("  [ANIMALES]")
        
        from apps.owners.models import Owner
        owners = list(Owner.objects.all()[:10])
        
        animales = [
            ('Luna', 'Gato', 'Atigrado', 2, 3, 'Hembra', True, True, 'Disponible',
             'Llegó al refugio tras ser encontrada en la calle por una vecina que la alimentaba desde hacía semanas. '
             'Vivía en la vía pública, sin hogar ni cuidados veterinarios. Es una gata muy sociable y cariñosa '
             'que busca un hogar donde la cuiden. Se lleva bien con otros gatos y con niños.'),
            ('Max', 'Perro', 'Golden Retriever', 3, 0, 'Macho', True, True, 'Sano',
             'Entregado por su familia debido a un cambio de residencia al extranjero donde no podían llevarlo. '
             'Vivía en una casa con jardín y estaba bien cuidado. Es un perro tranquilo, obediente y excelente '
             'con niños. Necesita un hogar con espacio para correr y actividad moderada diaria.'),
            ('Coco', 'Pajaro', 'Canario', 1, 6, 'Macho', False, False, 'Disponible',
             'Encontrado en un parque público por un paseante que lo vio en el suelo sin poder volar. '
             'Posiblemente escapó de una jaula o fue abandonado. Es un canario cantor de color amarillo '
             'intenso, sano y activo. Se adapta bien a cualquier ambiente tranquilo.'),
            ('Rocky', 'Perro', 'Beagle', 5, 0, 'Macho', True, True, 'En Tratamiento',
             'Rescatado de un criadero ilegal que fue desmantelado por las autoridades. Vivía hacinado '
             'con otros perros en condiciones insalubres, sin alimentación adecuada ni atención veterinaria. '
             'Llegó al refugio con desnutrición severa y sarna. Está en tratamiento veterinario y responde '
             'bien. Es un perro cariñoso pero asustadizo, necesita paciencia y un hogar tranquilo.'),
            ('Bella', 'Gato', 'Persa', 4, 0, 'Hembra', True, False, 'Sano',
             'Abandonada durante una mudanza. Los vecinos avisaron al refugio cuando vieron que la habían '
             'dejado atrás en el piso vacío. Estuvo varios días sola hasta que fue rescatada. Es una gata '
             'persa de pelo largo, tranquila y acostumbrada a vivir en interiores. Buena con niños y otras '
             'mascotas. Necesita cepillado regular por su tipo de pelo.'),
            ('Thor', 'Perro', 'Pastor Alemán', 2, 0, 'Macho', True, True, 'Disponible',
             'Entregado por sus dueños porque no podían cubrir sus necesidades de ejercicio y espacio en un piso. '
             'Provenía de un hogar donde lo tenían en un apartamento pequeño sin salidas suficientes. '
             'Es un perro joven muy activo, inteligente y leal. Necesita un hogar con jardín o patio, '
             'y dueños con experiencia en la raza que le proporcionen ejercicio diario y estimulación mental.'),
            ('Mía', 'Gato', 'Siamés', 1, 2, 'Hembra', True, True, 'Sano',
             'Encontrada por unos obreros en una obra en construcción, donde llevaba días refugiada entre '
             'los escombros. Estaba asustada y desorientada cuando llegó al refugio. Es una gata siamesa '
             'joven, muy dulce y juguetona. Ideal para familias con niños. Se adapta bien a pisos y '
             'le encanta estar en compañía de personas.'),
            ('Simba', 'Perro', 'Labrador', 4, 0, 'Macho', False, True, 'Critico',
             'Rescatado de una situación de abandono severo. Fue encontrado atado en un terreno baldío '
             'sin acceso a agua ni comida durante días. Llegó al refugio en estado crítico con displasia '
             'de cadera avanzada y signos de desnutrición. Actualmente recibe tratamiento veterinario '
             'intensivo y fisioterapia. Es un perro dócil y agradecido que necesita cuidados especiales '
             'y un hogar dispuesto a asumir su condición médica.'),
            ('Nala', 'Gato', 'European', 3, 0, 'Hembra', True, True, 'Disponible',
             'Rescatada de una colonia urbana controlada por el ayuntamiento. Vivía en la calle con otros '
             'gatos, expuesta a enfermedades y condiciones climáticas adversas. Fue desparasitada y '
             'vacunada al llegar al refugio. Es una gata europea de carácter independiente pero cariñosa '
             'cuando coge confianza. Busca un hogar con experiencia en gatos rescatados.'),
            ('Duke', 'Perro', 'Boxer', 6, 0, 'Macho', True, False, 'En Tratamiento',
             'Entregado por una familia mayor que ya no podía cuidarlo por problemas de salud. Provenía '
             'de un hogar donde estaba bien cuidado pero con movilidad reducida. Es un boxer senior con '
             'problemas articulares que requiere medicación diaria y visitas periódicas al veterinario. '
             'Es un perro tranquilo y muy leal, ideal para un hogar sin niños pequeños y con espacio '
             'adecuado para sus necesidades de movilidad.'),
            ('Pipo', 'Conejo', 'Holandés', 1, 0, 'Macho', False, True, 'Disponible',
             'Entregado por una familia que lo adquirió sin informarse adecuadamente sobre sus cuidados '
             'y decidió darlo en adopción. Vivía en una jaula pequeña sin espacio para ejercitarse. '
             'Es un conejo holandés blanco y negro, muy manso y acostumbrado al manejo. Necesita un '
             'hogar con espacio para correr y una dieta adecuada de heno y verduras frescas.'),
            ('Oreo', 'Conejo', 'Enano', 0, 8, 'Hembra', True, True, 'Disponible',
             'Rescatada de un particular que no podía hacerse cargo de ella por problemas económicos. '
             'La tenían en condiciones básicas pero sin los cuidados óptimos para un conejo enano. '
             'Es una coneja pequeña y activa, muy curiosa y sociable. Se recomienda adoptarla con '
             'compañía o dedicarle tiempo diario de ejercicio y estimulación.'),
            ('Chispas', 'Hamster', 'Sirio', 0, 4, 'Macho', False, False, 'Disponible',
             'Entregado por una familia cuyo hijo perdió el interés en la mascota. Llegó con su jaula '
             'y accesorios básicos. Es un hámster sirio joven y activo, en buen estado de salud. '
             'Necesita un hogar responsable que entienda las necesidades de los roedores: una jaula '
             'espaciosa con rueda de ejercicio y una dieta equilibrada.'),
            ('Kiko', 'Pajaro', 'Loro', 2, 0, 'Macho', False, True, 'Disponible',
             'Entregado voluntariamente por su dueño, quien por motivos de salud ya no podía atenderlo '
             'adecuadamente. El dueño anterior lo cuidó durante dos años y le enseñó algunas palabras. '
             'Es un loro hablador, sociable y acostumbrado a la interacción humana. Necesita un hogar '
             'con experiencia en aves, espacio para volar y estimulación mental diaria.'),
            ('Shadow', 'Gato', 'Negro', 5, 0, 'Macho', True, True, 'Sano',
             'Llegó al refugio después de que su dueño falleciera y la familia no pudiera quedarse con él. '
             'Vivía en un hogar estable desde cachorro, con todos los cuidados veterinarios al día. '
             'Es un gato negro de tamaño grande, extremadamente tranquilo y hogareño. Se adapta bien '
             'a entornos tranquilos. Ideal para personas mayores o familias sin niños muy pequeños.'),
            ('Lucky', 'Perro', 'Chihuahua', 3, 0, 'Hembra', True, True, 'Disponible',
             'Encontrada en el arcén de una autopista por un conductor que avisó a la policía local. '
             'Llegó al refugio asustada y deshidratada, pero se recuperó por completo. Es una chihuahua '
             'de tamaño pequeño, muy valiente y cariñosa una vez que confía. Ideal para pisos y familias '
             'sin niños pequeños. Necesita un hogar donde no pase largas horas sola.'),
            ('Pelusa', 'Gato', 'Carey', 2, 6, 'Hembra', True, False, 'Sano',
             'Abandonada en una caja cerrada en la puerta del refugio durante la noche. Apareció junto '
             'con una nota pidiendo que la cuidaran. Es una gata carey de pelo largo, muy independiente '
             'y elegante. No es especialmente cariñosa pero disfruta de la compañía tranquila. Necesita '
             'un hogar sin otros gatos y con gente que respete su espacio.'),
            ('Toby', 'Perro', 'Podenco', 4, 0, 'Macho', True, True, 'En Tratamiento',
             'Rescatado de un cazador que lo mantenía atado y en condiciones precarias. Fue incautado '
             'por las autoridades junto con otros perros en una operación contra el maltrato animal. '
             'Llegó con una pata fracturada que está en proceso de recuperación. Es un perro desconfiado '
             'al principio pero muy leal una vez que establece vínculo. Necesita un hogar con paciencia, '
             'sin niños pequeños y con espacio para correr.'),
            ('Frida', 'Gato', 'Azul Ruso', 1, 0, 'Hembra', True, True, 'Disponible',
             'Rescatada de una perrera municipal donde estaba en la lista de eutanasia por saturación. '
             'Una voluntaria del refugio la vio y la trasladó a SafePaws. Es una gata azul ruso joven, '
             'de carácter tranquilo y elegante. Ideal para familias, se adapta bien a pisos y se lleva '
             'bien con niños respetuosos. Busca un hogar definitivo donde la valoren.'),
            ('Rex', 'Perro', 'Dóberman', 5, 0, 'Macho', True, True, 'Sano',
             'Entregado por su dueño tras un cambio de residencia forzoso por motivos laborales. '
             'Vivía en una casa con jardín, bien cuidado y con todas las vacunas al día. Es un dóberman '
             'de carácter equilibrado, bien socializado y obediente. Necesita un hogar con experiencia '
             'en la raza, espacio suficiente y dueños activos que le proporcionen ejercicio diario.'),
        ]
        
        base_date = timezone.now().date()
        
        for i, (name, species, breed, age_y, age_m, sex, vacc, ster, status, description) in enumerate(animales):
            from apps.animales.models import Animal
            owner = random.choice(owners) if owners else None
            days_back = random.randint(1, 90)
            
            obj, created = Animal.objects.update_or_create(
                name=name, species=species,
                defaults={
                    'breed': breed,
                    'age_years': age_y,
                    'age_months': age_m,
                    'sex': sex,
                    'admission_date': base_date - timedelta(days=days_back),
                    'status': status,
                    'vaccinated': vacc,
                    'sterilized': ster,
                    'description': description,
                    'owner': owner,
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f"    + {name} ({species})")
            else:
                self.stdout.write(f"    ~ {name} ({species}) actualizado")

    def seed_donaciones(self):
        self.stdout.write("  [DONACIONES]")
        
        donors = [
            ('Fundación Amigos de los Animales', 'fundacion@amigos.es', '+34600000100', 'Monetaria', 5000, 'Transferencia', 'Donativo corporativo anual'),
            ('María Gómez Sánchez', 'maria.g@email.com', '+34600000101', 'Monetaria', 250, 'Tarjeta', 'Donativo mensual recurrente'),
            ('Pet Store Co.', 'contacto@petstore.es', '+34600000102', 'Monetaria', 1200, 'Transferencia', 'Patrocinio de eventos del refugio'),
            ('Anónimo', '', '', 'Monetaria', 500, 'Efectivo', 'Donativo anónimo en hucha del refugio'),
            ('Juan Rodríguez', 'juan.r@email.com', '+34600000103', 'Monetaria', 100, 'PayPal', 'Donativo online campaña Navidad'),
            ('ONG Protectora Animal', 'ong@protectora.es', '+34600000104', 'Monetaria', 2500, 'Transferencia', 'Subvención trimestral'),
            ('Carmen Vega', 'carmen.v@email.com', '+34600000105', 'Monetaria', 75, 'Tarjeta', 'Donativo cumpleaños solidario'),
            ('Empresas Nat SA', 'rrhh@empresasnat.es', '+34600000106', 'Monetaria', 3000, 'Transferencia', 'Aportación RSC empresa'),
            ('Luis Martínez', 'luis.m@email.com', '+34600000107', 'Monetaria', 150, 'Efectivo', 'Donativo en evento benéfico'),
            ('Ana Belén Torres', 'ana.t@email.com', '+34600000108', 'Monetaria', 200, 'Tarjeta', 'Donativo por adopción completada'),
            ('Distribuidora Pet', 'compras@distripet.es', '+34600000109', 'Material', 0, '', 'Lote de 50 kg de pienso y 30 latas de comida húmeda'),
            ('Veterinaria PetCare', 'vet@petcare.es', '+34600000110', 'Material', 0, '', 'Material sanitario: vendas, jeringuillas y antisépticos'),
            ('Coordinadora Animal', 'info@coordanimal.es', '+34600000111', 'Monetaria', 800, 'Transferencia', 'Donativo campaña de esterilización'),
            ('Beatriz Sánchez', 'beatriz.s@email.com', '+34600000112', 'Monetaria', 50, 'Tarjeta', 'Donativo puntual semana solidaria'),
            ('Club de Mascotas', 'club@mascotas.es', '+34600000113', 'Monetaria', 450, 'Transferencia', 'Recaudación evento socios'),
            ('Raúl Fernández', 'raul.f@email.com', '+34600000114', 'Monetaria', 100, 'PayPal', 'Donativo online'),
            ('Tienda Animalandia', 'tienda@animalandia.es', '+34600000115', 'Material', 0, '', 'Juguetes, camas y accesorios para perros y gatos'),
            ('Silvia Crespo', 'silvia.c@email.com', '+34600000116', 'Monetaria', 300, 'Tarjeta', 'Donativo por apadrinamiento de animal'),
            ('Alberto Velasco', 'alberto.v@email.com', '+34600000117', 'Monetaria', 175, 'Efectivo', 'Donativo recogida en empresa'),
            ('Fundación Huellas', 'fundacion@huellas.es', '+34600000118', 'Monetaria', 1500, 'Transferencia', 'Convenio de colaboración anual'),
        ]
        
        base_date = timezone.now().date()
        estados = ['Pendiente', 'Recibida', 'Procesada', 'Procesada', 'Procesada']
        
        from apps.donaciones.models import Donacion
        Donacion.objects.all().delete()
        
        for donante, email, phone, tipo, amount, metodo, desc in donors:
            days_back = random.randint(1, 180)
            estado = random.choice(estados) if tipo == 'Monetaria' else 'Recibida'
            
            Donacion.objects.create(
                donante=donante,
                donante_email=email,
                donante_phone=phone,
                date=base_date - timedelta(days=days_back),
                donation_type=tipo,
                status=estado,
                amount=amount if amount else None,
                payment_method=metodo if metodo else '',
                description=desc,
                is_active=True
            )
            self.stdout.write(f"    + {donante[:30]}")

    def seed_inventario(self):
        self.stdout.write("  [INVENTARIO]")
        
        productos = [
            ('Comida para perros', 50, 'kg'),
            ('Comida para gatos', 45, 'kg'),
            ('Comida para conejos', 20, 'kg'),
            ('Comida para pájaros', 15, 'kg'),
            ('Arena para gatos', 30, 'bolsa'),
            ('Pienso cachorro', 25, 'kg'),
            ('Pienso adulto', 40, 'kg'),
            ('Snacks para perros', 3, 'caja'),
            ('Snacks para gatos', 4, 'caja'),
            ('Juguetes masticables', 8, 'ud'),
            ('Correas perros', 15, 'ud'),
            ('Collares', 20, 'ud'),
            ('Camas para perros', 6, 'ud'),
            ('Camas para gatos', 5, 'ud'),
            ('Bolsas de plástico', 100, 'bolsa'),
            ('Guantes desechables', 50, 'caja'),
            ('Desinfectante', 10, 'L'),
            ('Champú neutro', 8, 'L'),
            ('Medicamentos básicos', 2, 'caja'),
            ('Vitaminas', 5, 'caja'),
            ('Almohadillas absorbentes', 20, 'bolsa'),
            ('Bebederos automáticos', 4, 'ud'),
            ('Comederos', 12, 'ud'),
            ('Transportines', 3, 'ud'),
            ('Ropa de cama', 15, 'bolsa'),
        ]
        
        for name, qty, unit in productos:
            from apps.inventario.models import Product
            Product.objects.get_or_create(
                name=name,
                defaults={
                    'quantity': qty,
                    'unit': unit,
                    'description': f'Producto de inventario: {name}',
                    'is_active': True
                }
            )
            self.stdout.write(f"    + {name}")
        
        self.seed_movements()
        
        stock_bajo = [
            ('Antibióticos', 2, 'caja'),
            ('Sueros', 4, 'ud'),
        ]
        
        for name, qty, unit in stock_bajo:
            from apps.inventario.models import Product
            Product.objects.get_or_create(
                name=name,
                defaults={
                    'quantity': qty,
                    'unit': unit,
                    'description': f'Medicamento: {name}',
                    'is_active': True
                }
            )
            self.stdout.write(f"    + {name} (stock bajo)")

    def seed_movements(self):
        self.stdout.write("  [MOVIMIENTOS]")
        
        from apps.inventario.models import Product, Movement
        
        productos = Product.objects.all()[:15]
        
        if not productos:
            self.stdout.write(self.style.WARNING("    ! No hay productos para crear movimientos"))
            return
        
        movimientos = [
            (productos[0], 'Entrada', 20, 'Donación de empresa pet friendly'),
            (productos[0], 'Salida', 5, 'Consumo diario gatos'),
            (productos[1], 'Entrada', 15, 'Compra mensual'),
            (productos[1], 'Salida', 8, 'Consumo diario perros'),
            (productos[2], 'Entrada', 10, 'Donación particular'),
            (productos[2], 'Salida', 3, 'Consumo conejos'),
            (productos[3], 'Entrada', 5, 'Reposición'),
            (productos[4], 'Entrada', 25, 'Pedido proveedores'),
            (productos[4], 'Salida', 10, 'Uso limpieza'),
            (productos[5], 'Entrada', 30, 'Compra granel'),
            (productos[5], 'Salida', 12, 'Cachorros alimentación'),
            (productos[6], 'Entrada', 20, 'Reposición almacen'),
            (productos[6], 'Salida', 15, 'Adultos alimentación'),
            (productos[7], 'Entrada', 10, 'Donación tienda'),
            (productos[8], 'Entrada', 8, 'Proveedor'),
            (productos[9], 'Entrada', 5, 'Donación'),
            (productos[9], 'Salida', 2, 'Juego libre'),
            (productos[10], 'Entrada', 12, 'Pedido'),
            (productos[10], 'Salida', 4, 'Paseos diarios'),
            (productos[11], 'Entrada', 15, 'Reposición'),
        ]
        
        base_date = timezone.now().date()
        
        for i, (product, tipo, cantidad, motivo) in enumerate(movimientos):
            days_back = random.randint(1, 60)
            Movement.objects.create(
                product=product,
                movement_date=base_date - timedelta(days=days_back),
                quantity=cantidad,
                type=tipo,
                reason=motivo,
                is_active=True
            )
            self.stdout.write(f"    + {tipo}: {product.name} ({cantidad})")

    def seed_health(self):
        self.stdout.write("  [EVENTOS MÉDICOS]")
        
        from apps.animales.models import Animal
        animales = Animal.objects.all()[:15]
        
        eventos = [
            ('Emergencia', 'Golpe en la cabeza por caída', 'Alta', 'Resolved'),
            ('Consulta', 'Revision anual de salud', 'Baja', 'Resolved'),
            ('Control', 'Control post-operatorio', 'Media', 'Resolved'),
            ('Procedimiento', 'Castración', 'Media', 'Resolved'),
            ('Consulta', 'Problemas digestivos', 'Media', 'Resolved'),
            ('Emergencia', 'Intoxicación alimentaria', 'Alta', 'Resolved'),
            ('Control', 'Vacunación', 'Baja', 'Resolved'),
            ('Procedimiento', 'Limpieza dental', 'Baja', 'Resolved'),
            ('Consulta', 'Problemas de piel', 'Media', 'En Proceso'),
            ('Emergencia', 'Herida en pata', 'Alta', 'Abierto'),
            ('Control', 'Desparasitación', 'Baja', 'Resolved'),
            ('Procedimiento', 'Esterilización', 'Media', 'Resolved'),
            ('Consulta', 'Revision ocular', 'Baja', 'Resolved'),
            ('Emergencia', 'Alergia severa', 'Alta', 'En Proceso'),
            ('Control', 'Análisis de sangre', 'Baja', 'Resolved'),
            ('Procedimiento', 'Corte de uñas', 'Baja', 'Resolved'),
            ('Consulta', 'Problemas dentales', 'Media', 'En Proceso'),
            ('Emergencia', 'Golpe de calor', 'Alta', 'Abierto'),
            ('Control', 'Chequeo cardiovascular', 'Baja', 'Resolved'),
            ('Procedimiento', 'Extracción de tumor benigno', 'Alta', 'Resolved'),
            ('Consulta', 'Otitis Infection', 'Media', 'Resolved'),
            ('Control', 'Vacunación antirrábica', 'Baja', 'Resolved'),
            ('Procedimiento', 'Limpieza de orejas', 'Baja', 'Resolved'),
            ('Consulta', 'Cojera persistente', 'Media', 'Resolved'),
            ('Emergencia', 'Atragantamiento', 'Alta', 'Resolved'),
            ('Control', 'Revisión de peso', 'Baja', 'Resolved'),
            ('Procedimiento', 'Tratamiento antiparasitario', 'Baja', 'Resolved'),
            ('Consulta', 'Infección urinaria', 'Media', 'Resolved'),
            ('Emergencia', 'Reacción аллергическая', 'Alta', 'Abierto'),
            ('Control', 'Radiografía torácica', 'Media', 'Resolved'),
        ]
        
        base_date = timezone.now().date()
        
        # Asignar varios eventos a cada animal (3-4 por animal)
        evento_idx = 0
        for animal in animales:
            for _ in range(3):
                if evento_idx < len(eventos):
                    from apps.health.models import MedicalEvent
                    tipo, desc, sev, estado = eventos[evento_idx]
                    days_back = random.randint(1, 120)
                    
                    resolved_date = None
                    if estado == 'Resolved':
                        days_resolved = random.randint(1, days_back - 1) if days_back > 1 else 0
                        resolved_date = base_date - timedelta(days=days_resolved)
                    
                    MedicalEvent.objects.create(
                        animal=animal,
                        event_type=tipo,
                        description=desc,
                        incident_date=base_date - timedelta(days=days_back),
                        severity=sev,
                        status=estado,
                        resolved_date=resolved_date,
                        is_active=True
                    )
                    self.stdout.write(f"    + {tipo}: {animal.name}")
                    evento_idx += 1

    def seed_adopciones(self):
        self.stdout.write("  [ADOPCIONES]")
        
        from apps.animales.models import Animal
        from apps.owners.models import Owner
        animales = list(Animal.objects.all()[:20])
        owners = list(Owner.objects.all()[:20])
        
        if not animales or not owners:
            self.stdout.write(self.style.WARNING("    ! No hay animales o owners suficientes"))
            return
        
        adopciones_data = [
            (animales[0], owners[0]),
            (animales[1], owners[1]),
            (animales[2], owners[2]),
            (animales[3], owners[3]),
            (animales[4], owners[4]),
            (animales[5], owners[5]),
            (animales[6], owners[6]),
            (animales[7], owners[7]),
            (animales[8], owners[8]),
            (animales[9], owners[9]),
            (animales[10], owners[10]),
            (animales[11], owners[11]),
            (animales[12], owners[12]),
            (animales[13], owners[13]),
            (animales[14], owners[14]),
            (animales[15], owners[15]),
            (animales[16], owners[16]),
            (animales[17], owners[17]),
            (animales[18], owners[18]),
            (animales[19], owners[19]),
        ]
        
        base_date = timezone.now().date()
        estados = ['Pendiente', 'Aprobada', 'Completada', 'Completada', 'Completada']
        
        for i, (animal, owner) in enumerate(adopciones_data):
            from apps.adopciones.models import Adopcion
            days_back = random.randint(10, 180)
            estado = random.choice(estados)
            fecha_adop = base_date - timedelta(days=days_back)
            
            Adopcion.objects.create(
                animal=animal,
                owner=owner,
                adoption_date=fecha_adop,
                status=estado,
                is_active=True
            )
            self.stdout.write(f"    + {animal.name} -> {owner.name}")