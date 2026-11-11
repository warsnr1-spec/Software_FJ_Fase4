# Guía de estudio del proyecto Software FJ

Este documento permite entender y exponer las decisiones importantes del código. Se recomienda leer el código de cada archivo mientras se sigue esta guía.

## 1. Modelo de clases

```text
              Entidad (ABC)
              /     |     \
         Cliente Servicio (ABC) Reserva
                  /   |   \
           ReservaSala  AlquilerEquipo  AsesoriaEspecializada

 GestorSoftwareFJ almacena listas de Cliente, Servicio y Reserva.
```

- `ABC` y `@abstractmethod`: impiden usar directamente una entidad genérica o un servicio genérico sin implementar los métodos exigidos.
- `Cliente`: usa `_nombre`, `_email` y `_celular`; las propiedades `@property` con setters impiden asignar valores inválidos.
- `Servicio`: define tarifa, disponibilidad y el contrato de tres operaciones para sus clases hijas.
- Las tres subclases de `Servicio`: implementan `validar_parametros`, `calcular_costo` y `describir`; esa sobrescritura permite el **polimorfismo**.
- `Reserva`: relaciona un `Cliente`, un `Servicio`, duración y estado; valida antes de modificar la reserva.
- `GestorSoftwareFJ`: utiliza tres listas (`_clientes`, `_servicios`, `_reservas`) como almacenamiento **solo en memoria**.

## 2. Cálculos de precios

En todas las variantes se calcula: `total = (subtotal × (1 - descuento/100)) × (1 + impuesto/100)`.

- **Sala**: subtotal = tarifa por hora × duración (máximo 8 horas).
- **Equipo**: subtotal = tarifa por hora × duración + $12.000 por preparación (máximo 72 horas).
- **Asesoría**: subtotal = tarifa por hora × duración (máximo 4 horas).

Se usa la clase `Decimal` para disminuir problemas de precisión con dinero. Se redondea a dos decimales mediante `ROUND_HALF_UP`.

La **sobrecarga** se representa con `@typing.overload` y variantes de argumentos opcionales de `calcular_costo`: una con solo duración y otra que admite descuento e impuesto. Importante: Python no implementa la sobrecarga de firmas a tiempo de ejecución como Java; los decoradores describen firmas para herramientas de análisis, mientras que los parámetros opcionales gestionan el comportamiento real.

## 3. Excepciones

- `ErrorSoftwareFJ`: padre de las excepciones de negocio.
- `DatoInvalidoError`: datos inválidos (duraciones, nombres, correos).
- `EntidadDuplicadaError`: cliente, servicio o reserva repetida.
- `EntidadNoEncontradaError`: búsqueda sin coincidencia.
- `ServicioNoDisponibleError`: servicio deshabilitado.
- `ReservaInvalidaError`: cliente o servicio de tipo inadecuado.
- `OperacionNoPermitidaError`: transición de estado inválida.
- `CalculoInvalidoError`: tarifa o porcentaje incorrecto.

**`try/except`** permite capturar una falla y continuar. **`try/except/else`** separa el resultado exitoso. **`try/except/finally`** registra el cierre de un intento independientemente de su resultado. **`raise ... from original`** explica de dónde surgió un error de transformación de datos.

## 4. Ejemplo: paso por paso de una reserva

1. El usuario registra un cliente y un servicio en `GestorSoftwareFJ`.
2. `crear_reserva` comprueba que el identificador no se encuentre duplicado.
3. Busca el cliente y el servicio en sus listas.
4. Construye el objeto `Reserva`, cuya duración pasa por validaciones.
5. Agrega la reserva a la lista solo si **todas** las validaciones fueron satisfactorias.
6. `confirmar_reserva` cambia su estado de PENDIENTE a CONFIRMADA.
7. `procesar_reserva` llama al método polimórfico `calcular_costo`.
8. En caso de éxito, guarda el total y cambia a PROCESADA.
9. Si ocurre una excepción, deja el estado sin cambios, escribe el evento en el log y devuelve el control al menú.

## 5. Qué demostrar al tutor

1. Ejecutar `py main.py --demo` y ver las 24 operaciones.
2. Señalar un registro inválido y mostrar que el siguiente sí se procesa.
3. Abrir `logs/software_fj.log` y enseñar los errores controlados.
4. Ejecutar `py -m unittest discover -s tests -v` y enseñar el total de pruebas.
5. Abrir `software_fj/servicios.py` y explicar herencia, métodos sobrescritos, polimorfismo y cálculo.
6. Abrir `software_fj/reserva.py` y localizar los bloques `try/except/else/finally`.
7. Abrir `software_fj/validaciones.py` para explicar `raise ... from original`.

## 6. Limitaciones del prototipo

Es un proyecto académico sin persistencia de datos comerciales, sin autenticación y sin manejo de fechas/horas de inicio para evitar conflictos de agenda. No se usa una base de datos; solamente el archivo de logs registra eventos de ejecución.

## 7. Participación colaborativa

La base está creada para que compañeros puedan revisar, corregir errores, añadir pruebas o mejorar la documentación. Las contribuciones deben quedar registradas con sus autores reales en el repositorio y, cuando se exija, en el foro académico.
