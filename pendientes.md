- Revisar colores fieldset donaciones_form y campo de formulario fuera de margen
- Revisar incidencias_form: campo de formulario fuera de margen
- 



- comandos basicos para trabajar rama develop
- te mueve  a la rama develop
        git checkout develop
- revisa y baja lo nuevo
        git pull origin develop
- crea una nueva rama para trabajar acorde a la funcionalidad
        git checkout -b feature/nueva-funcionalidad
- 
- 
- git status  usar  verificar que se agregara 
- Se agrega elementos editados
- git add .
- Realizar comit usar uno de estos formatos
- git commit -m "feat(auth): implementa login con validación"
    git commit -m "feat(incidencias): agrega formulario de creación"
    git commit -m "feat(users): añade perfil de usuario"
Enviar lo modificado en la rama creada a develop
    git push -u origin feature/nombre-funcionalidad
    hacer el Pull Request en github
    aprobar el PR en github

