import os
from django.core.management.base import BaseCommand

OUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ebook_files'
)

AUTOESTIMA_DATA = [
    {
        'id': 'complaciente',
        'bloqueo': 'El Complaciente Desdibujado',
        'subtitulo': 'Fuga de límites y autoabandono por aprobación',
        'frase': 'Crees que para recibir afecto tienes que ser útil. Tu mayor miedo no es decir «no», sino la culpa de pensar que van a dejar de quererte.',
        'origen': (
            'En la infancia aprendiste que el afecto era condicional al buen comportamiento, a no dar problemas '
            'o a cuidar a adultos desbordados. Tu sistema concluyó: «Si me hago indispensable y complazco, me aseguro un lugar». '
            'No es cobardía ni falta de carácter: fue tu forma infantil de garantizar pertenencia y seguridad.'
        ),
        'adultez': [
            'Te cuesta decir que no sin dar una justificación de tres párrafos o inventar una excusa médica.',
            'Sientes culpa inmediata si descansas mientras alguien a tu alrededor está trabajando o molesto.',
            'Atraes a vínculos demandantes que se acostumbran a que tú resuelvas todo sin quejarte.',
            'Llamas "generosidad" a lo que en el fondo es terror visceral al rechazo.',
            'Cuando alguien te pregunta qué quieres comer o hacer, tu respuesta refleja es «lo que tú prefieras».'
        ],
        'cuerpo': (
            'Tensión crónica en la garganta y hombros cargados, como si llevaras la responsabilidad de sostener a todo el mundo '
            'sin poder pedir nada para ti. Es la coraza que aprendió a tragar el deseo propio antes de que salga.'
        ),
        'practica': (
            'El cultivo de la autoestima aquí no es "amarte más", es entrenar el músculo del límite. '
            'Cada «no» que sostienes hacia afuera con firmeza es un «sí» sagrado que rescata tu autoconcepto.'
        ),
        'ejercicio': (
            '1. La pausa de 5 segundos: cuando alguien te pida un favor, no respondas de inmediato. Respira y di: '
            '«Déjame revisar mi tiempo y te confirmo en un rato».\n'
            '2. Registro del cuerpo: nota si al aceptar se cierra tu estómago o pecho. Tu cuerpo sabe antes que tu mente.\n'
            '3. Un «no» sin justificar por semana: di «esta vez no puedo, gracias por pensar en mí» y cierra la boca. '
            'Sostén la culpa sin escapar de ella: es el precio de tu libertad.'
        )
    },
    {
        'id': 'critico',
        'bloqueo': 'El Crítico Implacable',
        'subtitulo': 'Ausencia del observador neutro y perfeccionismo defensivo',
        'frase': 'Crees que si dejas de exigirte te vas a desmoronar. Pero la autoexigencia no es excelencia: es el pánico a que descubran que eres defectuoso.',
        'origen': (
            'Creciste en un ambiente donde solo se premiaba el rendimiento impecable o donde el error era castigado '
            'con burla, silencio o decepción. Tu niño interior inventó un fiscal adentro para castigarse antes de que lo hicieran afuera.'
        ),
        'adultez': [
            'Incapacidad crónica de disfrutar tus victorias: apenas alcanzas una meta ya estás estresado por la que sigue.',
            'Procrastinación defensiva: si sientes que el resultado no va a ser perfecto, postergas el inicio.',
            'Hipersensibilidad a la crítica ajena, porque confirma exactamente lo que tu juez interno ya te venía gritando.',
            'Confundes la autocompasión con debilidad, flojera o mediocridad.',
            'Tu mente es un tribunal permanente donde siempre estás en el banquillo de los acusados.'
        ],
        'cuerpo': (
            'Mandíbula apretada, respiración alta y contenida, estómago tenso en estado de alerta permanente por el juicio '
            'que tú mismo vas a emitir.'
        ),
        'practica': (
            'Encender el Punto de Vista del Observador (Endonáutica). El observador no juzga, solo registra. '
            'Cuando la voz crítica aparezca, no pelees con ella: obsérvala con distancia neutral como quien mira llover.'
        ),
        'ejercicio': (
            '1. Nombrar la voz: cuando notes la autocrítica voraz, di internamente: «Ahí está mi juez de nuevo intentando protegerme».\n'
            '2. Desidentificación: tú no eres esa voz; eres quien la escucha.\n'
            '3. La regla del 80%: entrega intencionalmente una tarea al 80% de tu estándar. Experimenta que el mundo no se acaba '
            'y que sigues teniendo exactamente el mismo valor.'
        )
    },
    {
        'id': 'prisionero',
        'bloqueo': 'El Prisionero de su Identidad',
        'subtitulo': 'Lealtad a una historia vieja y autoconcepto cristalizado',
        'frase': 'Te apegaste a una narrativa donde tú eres «el tímido», «el torpe» o «el roto». Cambiar te aterra porque no sabes quién eres si sueltas tu dolor.',
        'origen': (
            'En tu infancia recibiste etiquetas tempranas («es el problemático», «la calladita», «el que no entiende») '
            'o sufriste una herida de rechazo. Adoptaste esa etiqueta como armadura y hoy sigues siendo fiel a un personaje que ya no te sirve.'
        ),
        'adultez': [
            'Uso repetido de absolutos limitantes: «yo nunca he servido para eso», «a mí siempre me toca perder».',
            'Rechazo involuntario ante halagos sinceros: sientes que quien te elogia se equivocó o te tiene lástima.',
            'Miedo a prosperar porque sientes que si te transformas, traicionas el clan o la historia de tu familia.',
            'Sensación de que todos recibieron un manual para vivir que a ti se les olvidó entregarte.',
            'Te proteges tras la timidez o la soledad para no exponerte a ser juzgado de verdad.'
        ],
        'cuerpo': (
            'Hombros encogidos hacia adelante, pecho hundido, mirada baja; un cuerpo configurado físicamente para ocupar '
            'el menor espacio posible.'
        ),
        'practica': (
            'Reconocer que el autoconcepto es plástico y modificable (Endonáutica L701). No eres esa etiqueta vieja que te pusieron '
            'a los 7 años; eres la conciencia que hoy tiene el poder de decidir quién quiere ser.'
        ),
        'ejercicio': (
            '1. Auditoría de etiquetas: escribe en un papel todas las frases que empiezan con «Yo siempre he sido...» o «Yo nunca...».\n'
            '2. Pregunta de quiebre: ¿quién te dijo eso por primera vez?, ¿a quién le estás siendo leal sosteniendo esa limitación?\n'
            '3. Postura de presencia: 2 minutos al día con hombros atrás, pecho abierto y respiración profunda. El cuerpo enseña a la mente.'
        )
    },
    {
        'id': 'espectador',
        'bloqueo': 'El Espectador Resignado',
        'subtitulo': 'Locus de control externo y parálisis por validación',
        'frase': 'Pusiste el termostato de tu valor en el bolsillo de los demás. Si te aprueban existes; si te ignoran sientes que te desvaneces.',
        'origen': (
            'En la infancia tus opiniones e iniciativas fueron invalidadas, minimizadas o sancionadas como rebeldía. '
            'Aprendiste que decidir por ti mismo era peligroso y que era más seguro esperar órdenes.'
        ),
        'adultez': [
            'Pides tres opiniones diferentes antes de tomar una decisión cotidiana o profesional.',
            'Un solo comentario tibio o desaprobatorio en tu entorno arruina tu estado de ánimo por días.',
            'Sensación recurrente de estar en la "sala de espera" de tu propia vida, esperando que algo mágico ocurra.',
            'Resentimiento soterrado hacia las personas decididas, justificando tu inacción en la mala suerte.',
            'Fuga de responsabilidad personal: es más cómodo culpar a las circunstancias que asumir las consecuencias.'
        ],
        'cuerpo': (
            'Sensación de pesadez en brazos y piernas, falta de tonicidad, respiración superficial; postura de quien espera '
            'pasivamente que otros actúen.'
        ),
        'practica': (
            'Migrar del Locus de Control Externo al Interno (Endonáutica L733). Tu valor no se somete a plebiscito ajeno. '
            'Empieza por tomar una pequeña decisión al día sin consultar a nadie y asumiendo su resultado.'
        ),
        'ejercicio': (
            '1. Ayuno de validación: toma una decisión hoy (un menú, una ropa, una compra pequeña) sin preguntarle a nadie.\n'
            '2. Asumir la causa: sustituye la frase «esto me pasó por culpa de X» por «¿qué parte de esta situación permití o cocreé yo?».\n'
            '3. Celebración privada: reconoce tu propio logro en silencio antes de publicarlo o contarlo.'
        )
    },
    {
        'id': 'saboteador',
        'bloqueo': 'El Saboteador del Merecimiento',
        'subtitulo': 'Intolerancia al bienestar y miedo a la expansión',
        'frase': 'Soportas el malestar porque ya te lo conoces, pero cuando las cosas empiezan a ir bien tu sistema nervioso entra en pánico y busca cómo arruinarlo.',
        'origen': (
            'Creciste en un entorno caótico donde después de una risa o celebración venía inevitablemente una crisis, '
            'un grito o una decepción. Tu sistema grabó: «Estar bien es peligroso, la caída duele el doble».'
        ),
        'adultez': [
            'Sensación permanente de que "algo malo está a punto de pasar" en cuanto la vida se vuelve tranquila.',
            'Decisiones económicas o laborales erráticas justo en los momentos en que estabas consolidando estabilidad.',
            'Dificultad profunda para recibir regalos, favores o ayuda sin sentir una deuda angustiante.',
            'Te aburres en ambientes sanos y pacíficos porque tu sistema aprendió a confundir adrenalina y drama con vitalidad.',
            'Te bajas de oportunidades grandes a último minuto con excusas aparentemente lógicas.'
        ],
        'cuerpo': (
            'Espasmos en el plexo solar, taquicardia o inquietud motora justo después de recibir una buena noticia o experimentar paz.'
        ),
        'practica': (
            'Entrenar la autorregulación somática y la tolerancia al bienestar (Endonáutica L711). Cuando sientas el impulso de '
            'sabotear la paz, quédate quieto, respira en el cuerpo y permite que el merecimiento se asiente.'
        ),
        'ejercicio': (
            '1. Ampliar el contenedor: cuando te ocurra algo bueno, detén todo por 60 segundos. Cierra los ojos, pon las manos en tu pecho '
            'y siente el bienestar sin anticipar el futuro.\n'
            '2. Detectar el impulso de huida: antes de pelear, gastar de más o cancelar un compromiso importante, pregúntate: '
            '«¿Estoy reaccionando a un peligro real o mi sistema está asustado de la calma?».\n'
            '3. Recibir sin compensar: cuando te hagan un regalo o favor, di simplemente: «Muchas gracias, lo recibo con alegría».'
        )
    }
]


class Command(BaseCommand):
    help = 'Genera los 5 PDFs de "Mapa de Autoestima y Autoconcepto" para entrega de leads.'

    def handle(self, *args, **options):
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'AutoestimaTitle', parent=styles['Title'], fontSize=20, leading=24, spaceAfter=4,
            textColor=colors.HexColor('#1a1a1a'),
        )
        mask_style = ParagraphStyle(
            'AutoestimaMask', parent=styles['Normal'], fontSize=13,
            textColor=colors.HexColor('#7ECCCD'), spaceAfter=12,
        )
        frase_style = ParagraphStyle(
            'Frase', parent=styles['Normal'], fontSize=11, leading=16,
            textColor=colors.HexColor('#2a2a2a'), spaceAfter=14, spaceBefore=4,
            fontName='Helvetica-Oblique',
        )
        h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=13, spaceBefore=14, spaceAfter=6, textColor=colors.HexColor('#1a1a1a'))
        body = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, leading=15, spaceAfter=7, textColor=colors.HexColor('#333333'))
        bullet = ParagraphStyle('Bullet', parent=body, leftIndent=12, bulletIndent=0, spaceAfter=4)

        for b in AUTOESTIMA_DATA:
            out_path = os.path.join(OUT_DIR, f"mapa-autoestima-{b['id']}.pdf")
            doc = SimpleDocTemplate(
                out_path, pagesize=A4,
                topMargin=2.2*cm, bottomMargin=2.0*cm, leftMargin=2.4*cm, rightMargin=2.4*cm,
            )
            story = []
            story.append(Paragraph(f"Mapa de Autoestima: {b['bloqueo']}", title_style))
            story.append(Paragraph(b['subtitulo'], mask_style))
            story.append(HRFlowable(width='100%', thickness=0.6, color=colors.HexColor('#DDDDDD')))
            story.append(Paragraph(f'«{b["frase"]}»', frase_style))

            story.append(Paragraph('1. De dónde viene (El origen en tu infancia)', h2))
            story.append(Paragraph(b['origen'], body))

            story.append(Paragraph('2. Cómo opera hoy en tu adultez', h2))
            for t in b['adultez']:
                story.append(Paragraph(f'• {t}', bullet))

            story.append(Paragraph('3. La coraza en el cuerpo', h2))
            story.append(Paragraph(b['cuerpo'], body))

            story.append(Paragraph('4. El antídoto endonáutico', h2))
            story.append(Paragraph(b['practica'], body))

            story.append(Paragraph('5. Ejercicios prácticos para transformar este autoconcepto', h2))
            for linea in b['ejercicio'].split('\n'):
                if linea.strip():
                    story.append(Paragraph(linea.strip(), bullet))

            story.append(Spacer(1, 0.6*cm))
            story.append(HRFlowable(width='100%', thickness=0.6, color=colors.HexColor('#DDDDDD')))
            story.append(Spacer(1, 0.3*cm))
            story.append(Paragraph(
                'Fragmento práctico de <b>La Endonáutica</b>, por Franco Jeria Castro (Terapeuta en Salud Integrativa).<br/>'
                'Descubre el mapa completo del viaje interior y el Círculo Endonauta en: <b>endonautas.cl</b>',
                ParagraphStyle('Foot', parent=body, fontSize=8.5, leading=12, textColor=colors.HexColor('#777777')),
            ))

            doc.build(story)
            self.stdout.write(self.style.SUCCESS(f"OK: {out_path}"))
