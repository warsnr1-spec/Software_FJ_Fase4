# Software FJ - Fase 4, Programación (UNAD, 213023)

Proyecto educativo: **Sistema Integral de Gestión de Clientes, Servicios y Reservas**, siguiendo el *Anexo 3 - Problema a desarrollar Fase 4*.

## 1. ¿Qué ofrece?

- Clientes con propiedades encapsuladas y validación de nombre, email y teléfono.
- Clase abstracta `Entidad` y clase abstracta `Servicio`.
- Tres servicios polimórficos: `ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada`.
- Reservas con estados PENDIENTE, CONFIRMADA, PROCESADA y CANCELADA.
- Métodos de cálculo con variantes de firma (`@overload`) y argumentos opcionales para descuento e impuesto.
- Excepciones personalizadas, `try/except`, `try/except/else`, `try/except/finally` y encadenamiento con `raise ... from`.
- Registros de errores y eventos en `logs/software_fj.log`.
- **Sin base de datos.** Los clientes, servicios y reservas se mantienen en listas durante la ejecución.
- Menú interactivo, **24 operaciones** de demostración y pruebas unitarias.

## 2. Requisitos

Python 3.10 o superior. Únicamente biblioteca estándar; no requiere instalar paquetes.

## 3. Cómo ejecutarlo

Abra una terminal en la carpeta donde se encuentra `main.py`.

**Windows (PowerShell):**

```powershell
py main.py --demo
py main.py --menu
py -m unittest discover -s tests -v
```

**Linux y macOS:**

```bash
python3 main.py --demo
python3 main.py --menu
python3 -m unittest discover -s tests -v
```

Al ejecutar `--demo`, el programa verifica 24 operaciones con resultados esperados, incluidas fallas controladas. `--menu` permite crear clientes, servicios y reservas propios. Las pruebas unitarias verifican cada comportamiento importante. Los archivos de log se generan en `logs/`.

## 4. Arquitectura y responsabilidades

| Archivo | Contenido |
| --- | --- |
| `main.py` | Entrada a la aplicación, menú y ejecución de demostración |
| `software_fj/entidades.py` | Clase abstracta base `Entidad` |
| `software_fj/cliente.py` | Clase `Cliente` y encapsulación |
| `software_fj/servicios.py` | Clase abstracta `Servicio` y 3 clases derivadas |
| `software_fj/reserva.py` | Estados, confirmación, cancelación y procesamiento |
| `software_fj/gestor.py` | Control de listas y coordinación de operaciones |
| `software_fj/validaciones.py` | Validaciones de entrada y valores decimales |
| `software_fj/excepciones.py` | Jerarquía de excepciones propias |
| `software_fj/registro.py` | Registro de eventos/errores mediante `logging` |
| `software_fj/demo.py` | Simulación de 24 operaciones |
| `tests/test_sistema.py` | Pruebas automáticas con `unittest` |
| `evidencias/resultado_demo.txt` | Salida real de la simulación |
| `evidencias/resultado_pruebas.txt` | Salida real de las pruebas unitarias |
| `informe/Informe_Fase4_Software_FJ.pdf` | Documento para entregar (faltan datos individuales y URL de GitHub) |

## 5. Reglas de negocio que adoptamos para la simulación

Estas decisiones son **propuestas de implementación**, no cifras impuestas por el Anexo 3:

- Sala: máximo 8 horas; su precio es tarifa/hora × horas.
- Equipo: máximo 72 horas; cargo de preparación fijo de $12.000 COP por alquiler.
- Asesoría: máximo 4 horas; su precio es tarifa/hora × horas.
- En cálculo: primero se aplica el descuento y después el impuesto; ambos de 0 a 100%.
- Las reservas se confirman antes de procesarse. Una procesada no se puede cancelar.
- La disponibilidad es un atributo booleano del servicio. El prototipo **no agenda franjas de calendario ni detecta solapamientos temporales** porque el ejercicio no exige fecha/hora ni almacenamiento duradero.
- Las listas se reinician al cerrar el programa; solo permanece la bitácora de eventos.

## 6. Cómo subirlo a GitHub

1. Entre a [github.com/new](https://github.com/new) con su cuenta y cree el repositorio `Software_FJ_Fase4` (público o privado según las indicaciones del curso).
2. Desde una terminal en esta carpeta, ejecute:

```bash
git init
git add .
git commit -m "Fase 4: sistema orientado a objetos y manejo de excepciones"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/Software_FJ_Fase4.git
git push -u origin main
```

3. **Reemplace `TU_USUARIO`** por su usuario verdadero. Si creó el repositorio con un README inicial, deberá integrar antes el historial remoto para evitar conflictos, o crear el repositorio vacío.
4. Invite a sus compañeros como colaboradores y solicite que registren aportes en sus propias confirmaciones de Git. El historial debe reflejar contribuciones reales; no se deben atribuir aportes a compañeros que no participaron.
5. Pegue la URL REAL del repositorio en la sección correspondiente del PDF, junto con nombres, docente, grupo y fecha. No se ha publicado ni creado automáticamente el repositorio.

## 7. Comprobación final

- [ ] `py main.py --demo` ejecuta 24 operaciones sin interrupciones.
- [ ] `py -m unittest discover -s tests -v` supera todas las pruebas.
- [ ] El archivo `logs/software_fj.log` registra los errores.
- [ ] Se creó el repositorio real en GitHub y se subieron los archivos.
- [ ] El PDF contiene nombres, grupo, tutor, fecha y enlace verdadero.
- [ ] Se han publicado los aportes en el foro y las contribuciones reales en el repositorio.

**Alcance:** solución académica, no un sistema empresarial de producción. La validación de correo es básica; no implementa autenticación ni calendarios.
