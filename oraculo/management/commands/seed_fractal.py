"""
Seed command for the 33 Fractal Oracle cards.
Based on the oracle created by Alanis Mika Yuda (UNESP, 2023).
22 Major Arcana (imperative verbs) + 11 Sephiroth (Kabbalah).
"""

from django.core.management.base import BaseCommand
from oraculo.models import CartaFractal


CARTAS = [
    # ── 22 ARCANOS MAYORES (0–21) ──────────────────────────────────────
    {
        "numero": 0,
        "nombre_arcano": "El Loco",
        "verbo": "PREPARA",
        "tipo": "arcano",
        "descripcion_breve": "Todo viaje comienza en el vacío. El necio sagrado es el primero y el último: no tiene nada que proteger. Antes del primer paso, hay un silencio que lo contiene todo.",
        "descripcion_larga": "El Loco representa el potencial puro, el alma antes de la forma. Su imperativo es PREPARA: no la preparación ansiosa que anticipa el fracaso, sino el acto de vaciarse para poder recibir. Jungianamente, es la psique antes de la individuación, la apertura radical al proceso. En el fractal de la existencia, es el punto inicial desde el cual emerge todo patrón.",
    },
    {
        "numero": 1,
        "nombre_arcano": "El Mago",
        "verbo": "MANIFIESTA",
        "tipo": "arcano",
        "descripcion_breve": "La voluntad consciente se convierte en herramienta. Aquello que observas con intención ya ha comenzado a cambiar. La alquimia no está en los objetos, sino en quien los sostiene.",
        "descripcion_larga": "El Mago es el arquetipo de la agencia consciente. MANIFIESTA implica que ya tienes los elementos: el trabajo es enfocar. En términos junguianos, es la función del ego cuando está alineada con el Self. El fractal aquí es la iteración intencional: cada acción repite el patrón que crea la realidad visible.",
    },
    {
        "numero": 2,
        "nombre_arcano": "La Sacerdotisa",
        "verbo": "SUPRIME",
        "tipo": "arcano",
        "descripcion_breve": "El conocimiento que no se comparte guarda su fuerza. El silencio es una forma de soberanía. Hay sabiduría en contener, en no revelar, en dejar que el misterio permanezca intacto.",
        "descripcion_larga": "La Sacerdotisa custodia el umbral entre lo visible y lo invisible. SUPRIME no es represión: es discernimiento sobre qué revelar y qué guardar. Jung llamaría a esto la función de la anima en su aspecto sabio. En el fractal, es la parte del conjunto que no se expande hacia afuera pero organiza la estructura interna.",
    },
    {
        "numero": 3,
        "nombre_arcano": "La Emperatriz",
        "verbo": "APRECIA",
        "tipo": "arcano",
        "descripcion_breve": "La abundancia no llega a quien la persigue, sino a quien la percibe donde ya existe. La tierra da frutos a quien puede ver el fruto antes de que madure. Aprecia: el primer acto de la creación.",
        "descripcion_larga": "La Emperatriz es el principio de la fertilidad y la presencia sensorial plena. APRECIA invoca la capacidad de recibir lo que ya está dado. Jungianamente, conecta con la función sentimiento cuando es consciente y discriminante. En el fractal, es el momento de reconocer el patrón que ya existe en el caos.",
    },
    {
        "numero": 4,
        "nombre_arcano": "El Emperador",
        "verbo": "ESTABLECE",
        "tipo": "arcano",
        "descripcion_breve": "Antes de construir, traza los límites de lo que será. El poder sin estructura se dispersa. El caos necesita un recipiente para convertirse en forma útil.",
        "descripcion_larga": "El Emperador es el principio ordenador. ESTABLECE los límites no como prisión sino como forma que da dirección a la energía. En la individuación jungiana, es la función que crea el marco dentro del cual el Self puede operar. El fractal necesita sus condiciones de borde para generar la complejidad.",
    },
    {
        "numero": 5,
        "nombre_arcano": "El Hierofante",
        "verbo": "TOLERA",
        "tipo": "arcano",
        "descripcion_breve": "Las tradiciones no son prisiones sino mapas escritos por quienes caminaron antes. Tolerar no es resignarse: es reconocer que lo ajeno también contiene verdad.",
        "descripcion_larga": "El Hierofante guarda la sabiduría transmitida. TOLERA pide apertura a lo establecido sin rendición acrítica. Jungianamente, trabaja con la sombra colectiva: lo que la cultura ha codificado como sagrado, aunque no siempre comprendamos por qué. En el fractal, es el principio de semejanza entre escalas: lo que fue verdad en el pasado tiene ecos en el presente.",
    },
    {
        "numero": 6,
        "nombre_arcano": "Los Amantes",
        "verbo": "DIVIDE",
        "tipo": "arcano",
        "descripcion_breve": "Elegir es renunciar. Cada bifurcación en el fractal de tu vida requiere que abandones una rama para poder habitar otra. La división no es pérdida: es definición.",
        "descripcion_larga": "Los Amantes representan la bifurcación fundamental. DIVIDE no es separar por rechazo sino elegir conscientemente. La alquimia psicológica requiere separatio: distinguir lo propio de lo ajeno, lo auténtico de lo adaptativo. En el fractal, cada iteración que bifurca el conjunto crea estructura a partir de la elección.",
    },
    {
        "numero": 7,
        "nombre_arcano": "El Carro",
        "verbo": "CONTINÚA",
        "tipo": "arcano",
        "descripcion_breve": "El movimiento no requiere claridad total sobre el destino. La inercia del alma en dirección correcta es suficiente para hoy. Continúa, aunque el camino sea neblinoso.",
        "descripcion_larga": "El Carro es la voluntad en movimiento. CONTINÚA reconoce que el impulso sostenido supera a la claridad estática. Jungianamente, es la coniunctio en proceso: el yo y el inconsciente avanzando juntos sin necesitar resolución prematura. En el fractal, es la propiedad de la iteración: el patrón emerge del movimiento sostenido.",
    },
    {
        "numero": 8,
        "nombre_arcano": "La Fuerza",
        "verbo": "LIMITA",
        "tipo": "arcano",
        "descripcion_breve": "La fuerza real no se expresa en la explosión sino en la contención. Limitar no es debilidad: es la presión que transforma el carbono en diamante.",
        "descripcion_larga": "La Fuerza no es dominio sino integración. LIMITA la energía desbordada para convertirla en potencia útil. Jung describió esto como la domesticación de los instintos sin reprimirlos: transformar la bestia en aliada. En el fractal, el límite del conjunto es lo que genera la frontera infinitamente compleja.",
    },
    {
        "numero": 9,
        "nombre_arcano": "El Ermitaño",
        "verbo": "REFLEXIONA",
        "tipo": "arcano",
        "descripcion_breve": "La respuesta que buscas no está en el ruido externo. El ermitaño se retira no para escapar del mundo, sino para encontrar en sí mismo el mundo completo.",
        "descripcion_larga": "El Ermitaño encarna el trabajo de introspección necesario para el camino de individuación. REFLEXIONA es la instrucción de volverse hacia adentro antes de actuar. En términos junguianos, es el encuentro con el Viejo Sabio interior, la función de la intuición cuando apunta hacia la profundidad propia.",
    },
    {
        "numero": 10,
        "nombre_arcano": "La Rueda de la Fortuna",
        "verbo": "CIRCULA",
        "tipo": "arcano",
        "descripcion_breve": "Nada permanece en el nadir ni en el cenit. Lo que ahora pesa pasará; lo que ahora brilla cambiará de forma. El ciclo no es una trampa: es la naturaleza de lo vivo.",
        "descripcion_larga": "La Rueda de la Fortuna es el ciclo cósmico. CIRCULA reconoce que la posición actual es transitoria y que el movimiento es inherente a la existencia. Jungianamente, conecta con la enantiodromia: la tendencia de todo lo extremo a convertirse en su opuesto. En el fractal, es la naturaleza cíclica de las iteraciones.",
    },
    {
        "numero": 11,
        "nombre_arcano": "La Justicia",
        "verbo": "RELATIVIZA",
        "tipo": "arcano",
        "descripcion_breve": "La balanza no busca el absoluto sino el equilibrio contextual. Lo que parece injusto desde un ángulo puede ser necesario desde otro. Relativiza antes de sentenciar.",
        "descripcion_larga": "La Justicia trabaja con la función discriminativa de la psique. RELATIVIZA no significa renunciar a valores, sino expandir la perspectiva para ver el campo completo. En Jung, esto conecta con la trascendencia de los opuestos: ni blanco ni negro, sino el gris que los contiene. En el fractal, cada punto pertenece a un conjunto que no se puede juzgar desde un solo ángulo.",
    },
    {
        "numero": 12,
        "nombre_arcano": "El Colgado",
        "verbo": "PERCIBE",
        "tipo": "arcano",
        "descripcion_breve": "Ver el mundo desde la posición invertida revela lo que la postura habitual oculta. El colgado no sufre: observa. La inmovilidad voluntaria es una forma de percepción activa.",
        "descripcion_larga": "El Colgado es la suspensión voluntaria. PERCIBE desde una posición no habitual. Jungianamente, es la etapa de disolución necesaria para la transformación: el ego debe soltarse para que el Self pueda reorganizar. En el fractal, es el momento en que la iteración parece detenida pero en realidad está acumulando complejidad.",
    },
    {
        "numero": 13,
        "nombre_arcano": "La Muerte",
        "verbo": "TRANSFORMA",
        "tipo": "arcano",
        "descripcion_breve": "Lo que termina hace espacio para lo que viene. La muerte no es el opuesto de la vida: es su condición. Transforma, que es la única forma de continuar siendo.",
        "descripcion_larga": "La Muerte en el tarot es metamorfosis, no aniquilación. TRANSFORMA es el imperativo del proceso de individuación completo: cada etapa de crecimiento requiere que algo muera. Jung lo llamó opus contra naturam: el trabajo que va en contra del instinto de preservar la identidad vieja. En el fractal, es la condición de borde que permite que emerja una forma nueva.",
    },
    {
        "numero": 14,
        "nombre_arcano": "La Templanza",
        "verbo": "MODERA",
        "tipo": "arcano",
        "descripcion_breve": "El exceso en cualquier dirección consume su propia fuente. La maestría no está en la intensidad sino en la proporción justa. Modera: no por miedo, sino por sabiduría.",
        "descripcion_larga": "La Templanza es el arte de la mezcla alquímica. MODERA es la habilidad de combinar opuestos en la proporción que genera vida. Jungianamente, es la función transcendente activa: el símbolo que emerge de la tensión entre consciente e inconsciente. En el fractal, es el parámetro justo que genera complejidad sin caos destructivo.",
    },
    {
        "numero": 15,
        "nombre_arcano": "El Diablo",
        "verbo": "INVIERTE",
        "tipo": "arcano",
        "descripcion_breve": "Lo que te encadena te encadena con tu propio consentimiento. La sombra tiene forma porque la luz la proyecta. Invierte tu perspectiva sobre lo que consideras una prisión.",
        "descripcion_larga": "El Diablo es la sombra personificada. INVIERTE la perspectiva sobre lo que parece limitante. En Jung, esto es el trabajo central de la individuación: integrar la sombra no como demonio sino como energía que ha estado negada. En el fractal, los puntos que se alejan infinitamente revelan la forma del conjunto por contraste.",
    },
    {
        "numero": 16,
        "nombre_arcano": "La Torre",
        "verbo": "ROMPE",
        "tipo": "arcano",
        "descripcion_breve": "Algunas estructuras deben caer para que algo genuino pueda sostenerse. El rayo no destruye sin razón: apunta a lo que era frágil desde adentro. Rompe lo que ya no sustenta.",
        "descripcion_larga": "La Torre es la ruptura necesaria. ROMPE las estructuras que se construyeron sobre bases falsas. Jungianamente, es la erupción del inconsciente cuando el ego ha construido una persona demasiado rígida. En el fractal, es el momento de discontinuidad que reorganiza el sistema hacia un atractor más estable.",
    },
    {
        "numero": 17,
        "nombre_arcano": "La Estrella",
        "verbo": "INSPÍRATE",
        "tipo": "arcano",
        "descripcion_breve": "Después del derrumbe, la estrella aparece. La esperanza no es ingenuidad: es el reconocimiento de que el ciclo continúa y algo nuevo es siempre posible.",
        "descripcion_larga": "La Estrella es la renovación después de la crisis. INSPÍRATE invoca la conexión con algo más grande que el yo. Jungianamente, es el momento en que el Self comienza a mostrar su guía después de que el ego se ha humillado suficientemente. En el fractal, es el punto desde el cual emerge un nuevo patrón de orden.",
    },
    {
        "numero": 18,
        "nombre_arcano": "La Luna",
        "verbo": "SUMÉRGETE",
        "tipo": "arcano",
        "descripcion_breve": "Las mareas internas no se controlan: se navegan. El inconsciente tiene su propia lógica que la mente diurna no comprende. Sumérgete sin resistir.",
        "descripcion_larga": "La Luna representa el reino del inconsciente profundo. SUMÉRGETE en las corrientes psíquicas sin resistencia. Jungianamente, es la confrontación con el inconsciente colectivo: sus imágenes, sus miedos, sus poderes no resueltos. En el fractal, es la región de borde infinitamente compleja donde el orden y el caos coexisten.",
    },
    {
        "numero": 19,
        "nombre_arcano": "El Sol",
        "verbo": "INTENSIFICA",
        "tipo": "arcano",
        "descripcion_breve": "Hay momentos en que la vida pide que te expandas completamente. No hay modestia en eclipsar tu propio brillo cuando el momento lo convoca. Intensifica tu presencia.",
        "descripcion_larga": "El Sol es la conciencia plena, la individuación en su expresión luminosa. INTENSIFICA la presencia, la vitalidad, la claridad. Jungianamente, es el momento en que el Self y el ego se alinean sin fricción. En el fractal, es la región de máxima estabilidad donde el conjunto se despliega con toda su energía.",
    },
    {
        "numero": 20,
        "nombre_arcano": "El Juicio",
        "verbo": "CONSIDERA",
        "tipo": "arcano",
        "descripcion_breve": "Antes del veredicto, hay una pregunta que aún no has hecho. La campana llama a despertar, no a juzgar. Considera todo, incluso lo que preferirías ignorar.",
        "descripcion_larga": "El Juicio es el llamado al despertar. CONSIDERA antes de cerrar el libro. Jungianamente, es la integración final donde todo lo que fue sombra es llamado de vuelta al campo de la conciencia. En el fractal, es el momento en que el sistema tiene en cuenta todas sus condiciones iniciales antes de generar el patrón final.",
    },
    {
        "numero": 21,
        "nombre_arcano": "El Mundo",
        "verbo": "SÉ",
        "tipo": "arcano",
        "descripcion_breve": "Es difícil encontrar un verbo que defina la totalidad. Aquí las lágrimas, las sonrisas, las pasiones son las primeras y las últimas veces de tu estancia en el mundo. Sé.",
        "descripcion_larga": "El Mundo es la individuación completada, la totalidad expresada. SÉ: el imperativo más simple y más profundo. Jung lo llamaría la realización del Self. En el fractal, es el conjunto completo contemplado desde afuera: toda la complejidad, toda la belleza, toda la estructura emergente de iteraciones simples. Ser es el verbo fractal por excelencia.",
    },
    # ── 11 SEFIROT (22–32) — Árbol de la Vida, de Malkuth a Kether ────────
    {
        "numero": 22,
        "nombre_arcano": "Malkuth",
        "verbo": "MALKUTH",
        "tipo": "sefirot",
        "sefirot_nombre": "Malkuth",
        "descripcion_breve": "El punto de contacto entre lo eterno y lo material. El Reino es el cuerpo, la tierra, el presente que pisas. Todo lo que existe en el mundo espiritual se manifiesta primero aquí.",
        "descripcion_larga": "Malkuth es el Reino, la décima sefirot. Es el mundo material, el cuerpo físico, la presencia encarnada. En la escala humana, corresponde al nivel de la experiencia sensorial directa. Es el punto de llegada de toda energía espiritual y el punto de partida de todo ascenso.",
    },
    {
        "numero": 23,
        "nombre_arcano": "Yesod",
        "verbo": "YESOD",
        "tipo": "sefirot",
        "sefirot_nombre": "Yesod",
        "descripcion_breve": "El sustrato invisible que sostiene la forma visible. El Fundamento es la arquitectura del yo antes de que el yo sepa que existe.",
        "descripcion_larga": "Yesod es el Fundamento, la novena sefirot. Corresponde al inconsciente personal, a los sueños, a la imaginación. Es el espejo que refleja las energías superiores hacia el mundo material. Jung lo asociaría con la función del inconsciente como soporte de la conciencia.",
    },
    {
        "numero": 24,
        "nombre_arcano": "Netzach",
        "verbo": "NETZACH",
        "tipo": "sefirot",
        "sefirot_nombre": "Netzach",
        "descripcion_breve": "La fuerza de la naturaleza como principio eterno. Victoria no como triunfo sobre otro, sino como expresión plena y sin obstáculos de lo que eres.",
        "descripcion_larga": "Netzach es la Victoria, la séptima sefirot. Corresponde a las emociones, los instintos, la naturaleza salvaje, el deseo en su forma más pura. Es la fuerza que impulsa la vida sin racionalizar. Jung lo conectaría con la función sentimiento y con la vitalidad del inconsciente.",
    },
    {
        "numero": 25,
        "nombre_arcano": "Hod",
        "verbo": "HOD",
        "tipo": "sefirot",
        "sefirot_nombre": "Hod",
        "descripcion_breve": "La forma a través de la cual la energía se vuelve reconocible. El Esplendor es el lenguaje que el alma usa para hacerse visible al mundo.",
        "descripcion_larga": "Hod es la Gloria o el Esplendor, la octava sefirot. Corresponde al intelecto concreto, al lenguaje, a la forma que estructura la experiencia. Es el principio que da nombre a las cosas y en ese acto les da realidad. Jung lo conectaría con la función pensamiento en su vertiente práctica.",
    },
    {
        "numero": 26,
        "nombre_arcano": "Tipheret",
        "verbo": "TIPHERET",
        "tipo": "sefirot",
        "sefirot_nombre": "Tipheret",
        "descripcion_breve": "El punto de equilibrio en el árbol. Belleza como integración de opuestos, no como armonía superficial. El corazón del cosmos late aquí.",
        "descripcion_larga": "Tipheret es la Belleza, la sexta sefirot y el centro del Árbol de la Vida. Corresponde al Self jungiano: el principio central que organiza y equilibra todos los aspectos de la psique. Es el lugar donde lo superior y lo inferior se encuentran, donde lo espiritual toca lo emocional.",
    },
    {
        "numero": 27,
        "nombre_arcano": "Geburah",
        "verbo": "GEBURAH",
        "tipo": "sefirot",
        "sefirot_nombre": "Geburah",
        "descripcion_breve": "El principio del rigor que purifica. La fuerza que corta lo innecesario para proteger lo esencial. El límite como forma de amor severo.",
        "descripcion_larga": "Geburah es la Fortaleza o el Rigor, la quinta sefirot. Es el principio de la discriminación severa, del corte quirúrgico que elimina lo que daña para preservar lo que da vida. Jungianamente, conecta con la sombra cuando está integrada: la capacidad de decir no como acto de amor.",
    },
    {
        "numero": 28,
        "nombre_arcano": "Chesed",
        "verbo": "CHESED",
        "tipo": "sefirot",
        "sefirot_nombre": "Chesed",
        "descripcion_breve": "La expansión generosa sin condiciones. Amor que no calcula ni mide. La misericordia como el primer acto de la creación antes de que haya algo que juzgar.",
        "descripcion_larga": "Chesed es la Misericordia o el Amor, la cuarta sefirot. Es el principio de la expansión, de la gracia sin condiciones. Corresponde al arquetipo del padre bondadoso, al impulso de dar sin medir. Jungianamente, es el principio del amor como fuerza organizadora.",
    },
    {
        "numero": 29,
        "nombre_arcano": "Binah",
        "verbo": "BINAH",
        "tipo": "sefirot",
        "sefirot_nombre": "Binah",
        "descripcion_breve": "La comprensión que emerge del silencio contemplativo. El útero del pensamiento donde las formas aún son posibilidades infinitas.",
        "descripcion_larga": "Binah es el Entendimiento, la tercera sefirot. Es el principio de la forma, del recipiente que da estructura a la energía. Corresponde a la Gran Madre, al inconsciente como matriz de toda posibilidad. Jung lo conectaría con la función intuición orientada hacia el origen.",
    },
    {
        "numero": 30,
        "nombre_arcano": "Chokmah",
        "verbo": "CHOKMAH",
        "tipo": "sefirot",
        "sefirot_nombre": "Chokmah",
        "descripcion_breve": "El primer destello de la conciencia antes de que tome forma. Sabiduría como chispa, no como acumulación. El impulso primero de toda creación.",
        "descripcion_larga": "Chokmah es la Sabiduría, la segunda sefirot. Es el primer impulso de la energía creadora, el yang puro antes de que Binah lo forme. Corresponde al Padre Divino, al logos en su estado más primitivo. Jungianamente, es el principio masculino arquetípico en su vertiente creadora.",
    },
    {
        "numero": 31,
        "nombre_arcano": "Daat",
        "verbo": "DAAT",
        "tipo": "sefirot",
        "sefirot_nombre": "Daat",
        "es_especial": True,
        "descripcion_breve": "El abismo entre el conocimiento y la comprensión. Daat no está en el árbol: está en el espacio vacío donde el árbol debería estar. Lo que no puede ser dicho.",
        "descripcion_larga": "Daat es la sefirot oculta, el Conocimiento que no figura en el Árbol de la Vida pero que existe en el abismo entre Kether y las sefirot inferiores. Es el punto de unión y de ruptura simultánea. En términos junguianos, sería el umbral entre el consciente y el inconsciente colectivo: lo que puede conocerse pero no puede articularse.",
    },
    {
        "numero": 32,
        "nombre_arcano": "Kether",
        "verbo": "KETHER",
        "tipo": "sefirot",
        "sefirot_nombre": "Kether",
        "descripcion_breve": "El origen sin origen. La Corona no es un logro: es lo que eres antes de ser algo en particular. El punto donde el fractal de tu existencia regresa a su fuente.",
        "descripcion_larga": "Kether es la Corona, la primera y más alta sefirot. Es el principio de la unidad antes de toda diferenciación, la conciencia pura antes de que haya sujeto u objeto. Corresponde al Self en su aspecto más transpersonal. En el fractal, es el punto inicial desde el cual toda la complejidad del universo emerge.",
    },
]


class Command(BaseCommand):
    help = "Seed the 33 Fractal Oracle cards (Yuda, 2023)"

    def handle(self, *args, **options):
        created = 0
        updated = 0

        for data in CARTAS:
            obj, is_new = CartaFractal.objects.update_or_create(
                numero=data["numero"],
                defaults={k: v for k, v in data.items() if k != "numero"},
            )
            if is_new:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Cartas fractales: {created} creadas, {updated} actualizadas. Total: {CartaFractal.objects.count()}"
            )
        )
