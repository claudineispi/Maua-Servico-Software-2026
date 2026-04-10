"""
Seed inicial do banco de dados.
Executado no startup da API, após Base.metadata.create_all.
Idempotente: não insere dados que já existem.
"""
from sqlalchemy.orm import Session
from app.models.models import Raca, Cuidado, VacinaRecomendada

RACAS = [
    {"nome": "Golden Retriever",   "especie": "cao",  "porte": "grande",  "expectativa_vida_anos": 12, "nivel_atividade": "alto",  "descricao": "Cão amigável, inteligente e dedicado. Ótimo para famílias."},
    {"nome": "Labrador Retriever", "especie": "cao",  "porte": "grande",  "expectativa_vida_anos": 12, "nivel_atividade": "alto",  "descricao": "Um dos cães mais populares do mundo. Dócil e brincalhão."},
    {"nome": "Bulldog Francês",    "especie": "cao",  "porte": "pequeno", "expectativa_vida_anos": 10, "nivel_atividade": "baixo", "descricao": "Compacto, muscular e afetivo. Adapta-se bem a apartamentos."},
    {"nome": "Poodle",             "especie": "cao",  "porte": "medio",   "expectativa_vida_anos": 14, "nivel_atividade": "medio", "descricao": "Altamente inteligente e hipoalergênico. Ótimo para pessoas com alergia."},
    {"nome": "Yorkshire Terrier",  "especie": "cao",  "porte": "pequeno", "expectativa_vida_anos": 14, "nivel_atividade": "medio", "descricao": "Pequeno e corajoso. Muito apegado ao dono."},
    {"nome": "Shih Tzu",           "especie": "cao",  "porte": "pequeno", "expectativa_vida_anos": 13, "nivel_atividade": "baixo", "descricao": "Carinhoso e tranquilo. Ideal para idosos e apartamentos."},
    {"nome": "Border Collie",      "especie": "cao",  "porte": "medio",   "expectativa_vida_anos": 14, "nivel_atividade": "alto",  "descricao": "O cão mais inteligente do mundo. Precisa de muito estímulo mental."},
    {"nome": "Dachshund",          "especie": "cao",  "porte": "pequeno", "expectativa_vida_anos": 14, "nivel_atividade": "medio", "descricao": "Curioso e teimoso. Adora cavar e farejar."},
    {"nome": "Pastor Alemão",      "especie": "cao",  "porte": "grande",  "expectativa_vida_anos": 11, "nivel_atividade": "alto",  "descricao": "Leal, corajoso e versátil. Excelente cão de trabalho."},
    {"nome": "Persa",              "especie": "gato", "porte": "medio",   "expectativa_vida_anos": 15, "nivel_atividade": "baixo", "descricao": "Tranquilo e elegante. Requer cuidados especiais com o pelo."},
    {"nome": "Siamês",             "especie": "gato", "porte": "medio",   "expectativa_vida_anos": 15, "nivel_atividade": "medio", "descricao": "Vocal e social. Gosta de interação constante."},
    {"nome": "Maine Coon",         "especie": "gato", "porte": "grande",  "expectativa_vida_anos": 14, "nivel_atividade": "medio", "descricao": "Um dos maiores gatos domésticos. Gentil e brincalhão."},
    {"nome": "British Shorthair",  "especie": "gato", "porte": "medio",   "expectativa_vida_anos": 15, "nivel_atividade": "baixo", "descricao": "Calmo e independente. Adapta-se bem a diversas rotinas."},
    {"nome": "Vira-lata / SRD",    "especie": "cao",  "porte": "medio",   "expectativa_vida_anos": 15, "nivel_atividade": "medio", "descricao": "Mistura de raças. Geralmente muito saudável e resistente."},
]

# 5 cuidados específicos por raça — 70 itens no total
CUIDADOS_POR_RACA = {
    # ── Golden Retriever ──────────────────────────────────────
    "Golden Retriever": [
        {"categoria": "alimentacao", "titulo": "Controle de porções para prevenir obesidade", "descricao": "Goldens têm alta predisposição ao ganho de peso. Divida a ração diária em duas refeições e evite petiscos em excesso. Prefira alimentos ricos em proteínas (25-30%) e ômega-3.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "higiene", "titulo": "Escovação da pelagem dupla", "descricao": "A pelagem dupla densa requer escovação de 3 a 5 vezes por semana com escova slicker para evitar emaranhados. Durante as trocas sazonais a escovação deve ser diária.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "higiene", "titulo": "Limpeza das orelhas caídas", "descricao": "As orelhas caídas criam ambiente úmido propício a otites. Limpe com solução auricular veterinária mensalmente e sempre após nadar.", "frequencia": "mensal", "prioridade": "alta"},
        {"categoria": "saude", "titulo": "Monitoramento contra câncer e displasia", "descricao": "Goldens têm 60% de risco de câncer ao longo da vida e alta incidência de displasia coxofemoral. Check-ups semestrais e suplementos de condroitina auxiliam na prevenção.", "frequencia": "anual", "prioridade": "alta"},
        {"categoria": "exercicio", "titulo": "Exercício físico intenso e variado", "descricao": "Adultos necessitam de 90 a 120 minutos de exercício diário, incluindo caminhadas, natação e jogos de busca. Filhotes devem ter exercícios controlados.", "frequencia": "diário", "prioridade": "alta"},
    ],
    # ── Labrador Retriever ────────────────────────────────────
    "Labrador Retriever": [
        {"categoria": "alimentacao", "titulo": "Controle rigoroso de peso e porções", "descricao": "Labradores têm predisposição genética à obesidade e compulsão alimentar. Controle as porções com precisão e prefira ração com alto teor proteico e baixo índice glicêmico.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "higiene", "titulo": "Escovação semanal da pelagem dupla", "descricao": "A pelagem dupla requer escovação semanal para remover pelos soltos. Durante a muda sazonal a frequência deve ser diária. Banhos a cada 2-3 meses.", "frequencia": "semanal", "prioridade": "media"},
        {"categoria": "higiene", "titulo": "Limpeza semanal das orelhas", "descricao": "As orelhas pendentes retêm umidade e facilitam otites. Limpe semanalmente com solução auricular aprovada por veterinário.", "frequencia": "semanal", "prioridade": "alta"},
        {"categoria": "saude", "titulo": "Prevenção de displasia coxofemoral", "descricao": "Labradores são predispostos à displasia de quadril. Evite exercícios de alto impacto em filhotes até 12-18 meses. Consultas ortopédicas preventivas são essenciais.", "frequencia": "anual", "prioridade": "alta"},
        {"categoria": "exercicio", "titulo": "Atividade física diária intensa", "descricao": "Necessitam de pelo menos 1 hora de exercício vigoroso por dia: corridas, natação e jogos de busca. Brinquedos de quebra-cabeça complementam a estimulação mental.", "frequencia": "diário", "prioridade": "alta"},
    ],
    # ── Bulldog Francês ───────────────────────────────────────
    "Bulldog Francês": [
        {"categoria": "alimentacao", "titulo": "Dieta sem alimentos flatulentos", "descricao": "Muito predispostos à flatulência. Evite alimentos fermentáveis e prefira rações de alta qualidade para raças pequenas com ômega-3 e ômega-6. Divida em duas refeições diárias.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "higiene", "titulo": "Limpeza das rugas faciais", "descricao": "As pregas da pele acumulam umidade, sujeira e bactérias que causam infecções cutâneas. Limpe diariamente com pano úmido ou gaze e seque bem entre os sulcos.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "saude", "titulo": "Monitoramento respiratório braquicefálico", "descricao": "Suscetível à Síndrome Obstrutiva das Vias Aéreas (BOAS). Evite exposição ao calor intenso, exercícios extenuantes e situações de estresse.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "higiene", "titulo": "Limpeza e verificação das orelhas", "descricao": "As orelhas eretas devem ser verificadas semanalmente e limpas com produto específico para evitar acúmulo de cera e otites.", "frequencia": "semanal", "prioridade": "media"},
        {"categoria": "exercicio", "titulo": "Exercícios leves em horários frescos", "descricao": "Devido à anatomia braquicefálica, exercícios devem ser curtos e de baixa intensidade, em períodos frescos do dia. Caminhadas de 15-20 minutos são suficientes.", "frequencia": "diário", "prioridade": "alta"},
    ],
    # ── Poodle ────────────────────────────────────────────────
    "Poodle": [
        {"categoria": "higiene", "titulo": "Tosa profissional frequente", "descricao": "O pelo denso e encaracolado cresce continuamente, exigindo tosa profissional a cada 4-6 semanas. Em casa, escove diariamente com escova slicker para prevenir nós.", "frequencia": "mensal", "prioridade": "alta"},
        {"categoria": "higiene", "titulo": "Limpeza do canal auricular", "descricao": "Poodles acumulam pelos dentro do canal auricular que devem ser retirados durante a tosa. Limpe semanalmente com solução auricular para prevenir otites.", "frequencia": "semanal", "prioridade": "alta"},
        {"categoria": "saude", "titulo": "Higiene dental diária", "descricao": "Poodles são altamente propensos a problemas dentários. Escove os dentes pelo menos 3 vezes por semana com pasta específica para cães. Profilaxia dental anual.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "saude", "titulo": "Triagem genética para doenças hereditárias", "descricao": "Predispostos a doença de Addison, atrofia progressiva da retina e luxação patelar (Toy/Mini). Exames preventivos anuais e raio-X de quadril são recomendados.", "frequencia": "anual", "prioridade": "media"},
        {"categoria": "exercicio", "titulo": "Exercício adequado ao porte", "descricao": "Padrão: 60 min/dia. Miniatura: 40-60 min/dia. Toy: 20-40 min/dia. Incluir agilidade e obediência, que estimulam a alta inteligência da raça.", "frequencia": "diário", "prioridade": "media"},
    ],
    # ── Yorkshire Terrier ─────────────────────────────────────
    "Yorkshire Terrier": [
        {"categoria": "alimentacao", "titulo": "Ração específica para raças pequenas", "descricao": "Metabolismo acelerado e tendência a problemas intestinais. Use ração premium para raças miniaturas com grânulos pequenos e alto teor proteico. Duas refeições diárias.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "higiene", "titulo": "Escovação diária do pelo sedoso", "descricao": "O pelo fino e sedoso, semelhante ao cabelo humano, emaranham facilmente. Escove diariamente com escova de cerdas macias. Banhos a cada 15 dias com secagem completa.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "saude", "titulo": "Higiene bucal para prevenir tártaro", "descricao": "Extremamente propensos ao acúmulo de tártaro e doenças periodontais devido à boca pequena. Escovação dentária 2-3 vezes por semana com produtos veterinários.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "saude", "titulo": "Monitoramento do peso e check-up regular", "descricao": "Ganha peso facilmente e pode desenvolver problemas cardíacos e articulares. Visitas veterinárias semestrais e monitoramento mensal do peso são essenciais.", "frequencia": "mensal", "prioridade": "media"},
        {"categoria": "comportamento", "titulo": "Socialização precoce e treinamento firme", "descricao": "Temperamento terrier forte. Pode desenvolver dominância se não treinado com firmeza desde filhote. Socialização precoce previne agressividade e latidos excessivos.", "frequencia": "diário", "prioridade": "media"},
    ],
    # ── Shih Tzu ──────────────────────────────────────────────
    "Shih Tzu": [
        {"categoria": "higiene", "titulo": "Limpeza diária dos olhos salientes", "descricao": "Olhos grandes e proeminentes propensos a úlceras de córnea e infecções. Limpe diariamente as secreções com gaze e solução oftálmica. Mantenha os pelos faciais presos.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "higiene", "titulo": "Escovação e banho regulares", "descricao": "Pelagem densa e longa deve ser escovada diariamente para evitar nós. Banhos a cada 10-15 dias com xampus de pH adequado, seguidos de secagem completa.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "alimentacao", "titulo": "Alimentação balanceada para raça pequena", "descricao": "Metabolismo rápido e tendência ao sobrepeso. Porções pequenas mas nutricionalmente densas, divididas em 2-3 refeições diárias. Evite petiscos calóricos.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "higiene", "titulo": "Verificação e limpeza das orelhas", "descricao": "Orelhas longas e pendentes acumulam umidade e sujeira que favorecem otites. Limpeza semanal com produto específico veterinário.", "frequencia": "semanal", "prioridade": "media"},
        {"categoria": "saude", "titulo": "Monitoramento respiratório braquicefálico", "descricao": "Como raça braquicefálica, pode apresentar dificuldades respiratórias em ambientes quentes ou durante exercícios intensos. Evite exposição ao calor excessivo.", "frequencia": "diário", "prioridade": "alta"},
    ],
    # ── Border Collie ─────────────────────────────────────────
    "Border Collie": [
        {"categoria": "exercicio", "titulo": "Exercício físico intenso diariamente", "descricao": "Raça mais ativa do mundo canino. Mínimo 1,5 a 2 horas de exercício vigoroso diário: corrida, agilidade, frisbee ou pastoreio. Falta de exercício causa ansiedade.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "comportamento", "titulo": "Estimulação mental diária obrigatória", "descricao": "Raça canina mais inteligente. Necessita de treinos de obediência, jogos de busca, brinquedos de quebra-cabeça e esportes como agility diariamente. Subestimulação causa estresse.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "higiene", "titulo": "Escovação regular da pelagem densa", "descricao": "Pelo longo: 2-3 vezes/semana. Pelo curto: semanalmente. Maior atenção nas mudas sazonais. Use pente e escova slicker para a subpelagem.", "frequencia": "semanal", "prioridade": "media"},
        {"categoria": "saude", "titulo": "Triagem para displasia e epilepsia", "descricao": "Predispostos à displasia coxofemoral e epilepsia idiopática. Exames ortopédicos e neurológicos preventivos anuais. Evitar alto impacto em filhotes até 18 meses.", "frequencia": "anual", "prioridade": "alta"},
        {"categoria": "comportamento", "titulo": "Gerenciamento do instinto de pastoreio", "descricao": "O instinto de pastoreio pode levá-lo a perseguir crianças, carros e outros animais. Treino com reforço positivo desde filhote. Redirecione para atividades esportivas.", "frequencia": "diário", "prioridade": "media"},
    ],
    # ── Dachshund ─────────────────────────────────────────────
    "Dachshund": [
        {"categoria": "saude", "titulo": "Proteção da coluna vertebral contra hérnias", "descricao": "Risco 10-12x maior de hérnia de disco devido ao corpo longo e pernas curtas. Evite saltos de sofás e escadas. Instale rampas e apoie sempre dianteiro e traseiro ao carregar.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "alimentacao", "titulo": "Controle de peso rigoroso", "descricao": "Sobrepeso aumenta drasticamente a pressão sobre os discos intervertebrais. Ração rica em ômega-3 e cálcio, com refeições fracionadas para evitar distensão.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "exercicio", "titulo": "Exercício moderado sem impacto à coluna", "descricao": "Caminhadas suaves e brincadeiras moderadas diárias para manter a musculatura. Evitar saltos e movimentos bruscos. Natação é ideal pois fortalece sem sobrecarregar.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "higiene", "titulo": "Cuidados conforme tipo de pelo", "descricao": "Pelo curto: escovação semanal. Pelo longo: escovação diária. Pelo duro: stripping semestral por profissional. Limpeza das orelhas pendentes mensalmente.", "frequencia": "semanal", "prioridade": "media"},
        {"categoria": "saude", "titulo": "Exames periódicos de coluna", "descricao": "Consultas com avaliação neurológica e ortopédica para monitorar saúde da coluna e degeneração dos discos. Fraqueza nas patas traseiras exige atendimento imediato.", "frequencia": "anual", "prioridade": "alta"},
    ],
    # ── Pastor Alemão ─────────────────────────────────────────
    "Pastor Alemão": [
        {"categoria": "alimentacao", "titulo": "Dieta rica em proteínas e suporte articular", "descricao": "Dieta com alto teor proteico (frango, carne, peixe) e suplementos de glucosamina e condroitina para saúde articular. Vitaminas A, D, E e minerais essenciais.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "higiene", "titulo": "Escovação frequente da subpelagem densa", "descricao": "Pelagem dupla e densa: escovação pelo menos 2x/semana, diária nas trocas sazonais. Evitar banhos excessivos que ressecam a pele.", "frequencia": "semanal", "prioridade": "media"},
        {"categoria": "saude", "titulo": "Prevenção da displasia coxofemoral", "descricao": "Displasia é a terceira doença mais frequente na raça. Escolha filhotes de reprodutores com boas classificações ortopédicas. Peso ideal e raio-X anuais.", "frequencia": "anual", "prioridade": "alta"},
        {"categoria": "exercicio", "titulo": "Exercício físico e mental intenso", "descricao": "Pelo menos 2 horas de atividade diária variada: corridas, caminhadas, rastreamento e obediência avançada. Subestimulação causa ansiedade e destruição.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "comportamento", "titulo": "Socialização e treinamento desde filhote", "descricao": "Socialização precoce e treinamento consistente com reforço positivo são essenciais para canalizar inteligência e instinto protetor de forma equilibrada.", "frequencia": "diário", "prioridade": "alta"},
    ],
    # ── Persa (gato) ──────────────────────────────────────────
    "Persa": [
        {"categoria": "higiene", "titulo": "Escovação diária do pelo longo e denso", "descricao": "O pelo longo emaranham com facilidade. Escove diariamente com pente de dentes largos e escova de cerdas macias. Banho mensal com xampus para gatos de pelo longo.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "higiene", "titulo": "Limpeza diária dos olhos e face achatada", "descricao": "Braquicefálico, sofre de lacrimejamento excessivo que mancha e causa infecções. Limpe diariamente com gaze e solução oftálmica. Limpe os sulcos faciais.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "saude", "titulo": "Monitoramento de doenças renais e respiratórias", "descricao": "Predisposição a doença renal policística (PKD) e problemas respiratórios pela face achatada. Check-ups anuais com exames de sangue e urina.", "frequencia": "anual", "prioridade": "alta"},
        {"categoria": "alimentacao", "titulo": "Ração adaptada ao formato braquicefálico", "descricao": "Precisa de ração com grânulos adaptados à mandíbula curta para facilitar a preensão. Dieta equilibrada que apoie a saúde da pele e pelo denso.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "comportamento", "titulo": "Ambiente tranquilo e enriquecimento moderado", "descricao": "Gatos calmos que preferem ambientes tranquilos e rotinas previsíveis. Ofereça arranhadores, prateleiras baixas e brinquedos interativos suaves.", "frequencia": "diário", "prioridade": "media"},
    ],
    # ── Siamês (gato) ─────────────────────────────────────────
    "Siamês": [
        {"categoria": "comportamento", "titulo": "Atenção e interação social intensa", "descricao": "Extremamente social e vocal, sofre de ansiedade quando sozinho. Necessita de interação humana diária e idealmente companhia de outro gato.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "alimentacao", "titulo": "Ração de alta proteína com suporte renal", "descricao": "Sistema digestivo sensível e predisposição a amiloidose hepática. Ração rica em proteínas animais e complementar com ração úmida para hidratação.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "higiene", "titulo": "Escovação semanal e higiene dental", "descricao": "Pelo curto requer escovação 1-2 vezes por semana. Limpeza dental com escova específica pelo menos 2x/semana para prevenir doenças periodontais.", "frequencia": "semanal", "prioridade": "media"},
        {"categoria": "exercicio", "titulo": "Brinquedos interativos e enriquecimento ambiental", "descricao": "Ativo e ágil. Sessões diárias de brincadeira com varetas, brinquedos de perseguição e ambientes com arranhadores e prateleiras. Tédio causa vocalização excessiva.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "saude", "titulo": "Monitoramento cardíaco e check-up anual", "descricao": "Predispostos à cardiomiopatia dilatada e problemas respiratórios. Check-up anual com auscultação cardíaca, exames de sangue e vacinação em dia.", "frequencia": "anual", "prioridade": "alta"},
    ],
    # ── Maine Coon (gato) ─────────────────────────────────────
    "Maine Coon": [
        {"categoria": "higiene", "titulo": "Escovação frequente da pelagem dupla longa", "descricao": "Pelagem dupla densa e longa: escove 2-3 vezes por semana com pente de dentes largos e escova slicker. Banhos a cada poucos meses pois o pelo fica oleoso.", "frequencia": "semanal", "prioridade": "alta"},
        {"categoria": "alimentacao", "titulo": "Ração de alto teor proteico em tigelas largas", "descricao": "Carnívoros obrigatórios que precisam de ração com mais de 50% de proteína, 2-4 vezes ao dia. Preferem tigelas extra largas e rasas para conforto dos bigodes.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "saude", "titulo": "Triagem para cardiomiopatia hipertrófica (CMH)", "descricao": "CMH é a condição cardíaca hereditária mais comum na raça. Ecocardiogramas anuais para detecção precoce. Sinais: respiração ofegante, letargia, perda de apetite.", "frequencia": "anual", "prioridade": "alta"},
        {"categoria": "exercicio", "titulo": "Pelo menos 30 minutos de atividade diária", "descricao": "Propensos à obesidade. Sessões de brincadeira com brinquedos interativos, varas e arranhadores grandes. A raça aprecia água e alguns aceitam passear com coleira.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "higiene", "titulo": "Verificação e limpeza das orelhas tufadas", "descricao": "Orelhas grandes com pelos densos internos retêm sujeira e umidade. Verificação e limpeza mensal com solução auricular veterinária.", "frequencia": "mensal", "prioridade": "media"},
    ],
    # ── British Shorthair (gato) ──────────────────────────────
    "British Shorthair": [
        {"categoria": "alimentacao", "titulo": "Dieta controlada para prevenir obesidade", "descricao": "Muito propensos à obesidade. Ração de alta proteína e baixo carboidrato ajustada por veterinário. Água fresca sempre disponível pela suscetibilidade renal.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "higiene", "titulo": "Escovação semanal do pelo denso", "descricao": "Pelo denso e 'plush' precisa de escovação semanal para remover pelos mortos. Nas trocas sazonais aumente para 2-3 vezes. Corte unhas a cada 2-3 semanas.", "frequencia": "semanal", "prioridade": "media"},
        {"categoria": "saude", "titulo": "Monitoramento de doença renal e cardíaca", "descricao": "Predisposição genética à PKD e CMH. Ecocardiogramas e ultrassom renal anuais para detecção precoce. Sintomas de PKD geralmente aparecem aos 7 anos.", "frequencia": "anual", "prioridade": "alta"},
        {"categoria": "exercicio", "titulo": "Brincadeiras diárias contra o sedentarismo", "descricao": "Apesar do temperamento calmo, precisa de 15-20 minutos de brincadeira interativa diária com varetas, bolinhas e laser para manter o peso saudável.", "frequencia": "diário", "prioridade": "media"},
        {"categoria": "saude", "titulo": "Higiene dental preventiva regular", "descricao": "Propensos a doenças dentais. Escovação dos dentes com pasta específica para gatos pelo menos 2 vezes por semana. Profilaxia dental veterinária anual.", "frequencia": "semanal", "prioridade": "media"},
    ],
    # ── Vira-lata / SRD ──────────────────────────────────────
    "Vira-lata / SRD": [
        {"categoria": "saude", "titulo": "Vacinação e vermifugação rigorosas", "descricao": "Apesar da robustez genética, necessitam do protocolo completo de vacinação (antirrábica, polivalente) e vermifugação regular conforme orientação veterinária.", "frequencia": "anual", "prioridade": "alta"},
        {"categoria": "saude", "titulo": "Check-up preventivo regular", "descricao": "Características físicas variadas da mistura genética exigem avaliação clínica completa anual para identificação de predisposições específicas. Expectativa de vida pode chegar a 16 anos.", "frequencia": "anual", "prioridade": "alta"},
        {"categoria": "alimentacao", "titulo": "Alimentação balanceada adequada ao porte", "descricao": "Adaptar ao porte (pequeno/médio/grande), nível de atividade e faixa etária. Ração de qualidade ou dieta natural orientada por veterinário. Evitar restos de comida humana.", "frequencia": "diário", "prioridade": "alta"},
        {"categoria": "higiene", "titulo": "Banho, escovação e cuidados gerais", "descricao": "Cuidados variam conforme o tipo de pelo herdado. Banhos a cada 15-30 dias, escovação regular e verificação de orelhas, olhos e unhas para detectar parasitas.", "frequencia": "semanal", "prioridade": "media"},
        {"categoria": "exercicio", "titulo": "Passeios e atividades físicas diárias", "descricao": "Exercícios adequados ao porte e energia individual: passeios diários, brincadeiras e atividades ao ar livre. Previne latidos excessivos e destruição de objetos.", "frequencia": "diário", "prioridade": "alta"},
    ],
}


# Calendario vacinal recomendado — Caes e Gatos (Brasil)
CALENDARIO_VACINAL = [
    # ── CAES — V10 ──
    {"especie": "cao", "grupo": "V10", "dose": 1, "idade_semanas": 6,  "obrigatoria": True, "reforco_anual": True,
     "nome": "V10 - 1a dose", "descricao": "Primeira dose da polivalente. Protege contra cinomose, parvovirose, hepatite infecciosa canina, parainfluenza, coronavirose e leptospirose."},
    {"especie": "cao", "grupo": "V10", "dose": 2, "idade_semanas": 9,  "obrigatoria": True, "reforco_anual": True,
     "nome": "V10 - 2a dose", "descricao": "Segunda dose da polivalente (V10). Reforco 3 semanas apos a 1a dose."},
    {"especie": "cao", "grupo": "V10", "dose": 3, "idade_semanas": 12, "obrigatoria": True, "reforco_anual": True,
     "nome": "V10 - 3a dose", "descricao": "Terceira e ultima dose inicial da V10. Completa a imunizacao basica do filhote."},
    {"especie": "cao", "grupo": "V10", "dose": 4, "idade_semanas": 64, "obrigatoria": True, "reforco_anual": True,
     "nome": "V10 - Reforco Anual", "descricao": "Dose anual de reforco. Manter por toda a vida do cao."},
    # ── CAES — Antirrabica ──
    {"especie": "cao", "grupo": "Antirrabica", "dose": 1, "idade_semanas": 12, "obrigatoria": True, "reforco_anual": True,
     "nome": "Antirrabica - 1a dose", "descricao": "Vacina antirrabica, obrigatoria por lei no Brasil. Aplicada a partir de 12 semanas."},
    {"especie": "cao", "grupo": "Antirrabica", "dose": 2, "idade_semanas": 64, "obrigatoria": True, "reforco_anual": True,
     "nome": "Antirrabica - Reforco Anual", "descricao": "Reforco anual obrigatorio da antirrabica. Exigida por lei durante toda a vida."},
    # ── CAES — Bordetella (Tosse dos Canis) ──
    {"especie": "cao", "grupo": "Bordetella", "dose": 1, "idade_semanas": 8,  "obrigatoria": False, "reforco_anual": True,
     "nome": "Bordetella - 1a dose", "descricao": "Vacina contra tosse dos canis (Bordetella bronchiseptica). Recomendada para caes em ambientes coletivos."},
    {"especie": "cao", "grupo": "Bordetella", "dose": 2, "idade_semanas": 12, "obrigatoria": False, "reforco_anual": True,
     "nome": "Bordetella - 2a dose", "descricao": "Segunda dose da Bordetella (protocolo injetavel). Intranasal requer dose unica."},
    {"especie": "cao", "grupo": "Bordetella", "dose": 3, "idade_semanas": 60, "obrigatoria": False, "reforco_anual": True,
     "nome": "Bordetella - Reforco Anual", "descricao": "Reforco anual contra tosse dos canis."},
    # ── CAES — Giardiase ──
    {"especie": "cao", "grupo": "Giardiase", "dose": 1, "idade_semanas": 8,  "obrigatoria": False, "reforco_anual": True,
     "nome": "Giardiase - 1a dose", "descricao": "Vacina contra Giardia. Nota: comercializacao suspensa pelo MAPA desde maio/2023 — consulte seu veterinario."},
    {"especie": "cao", "grupo": "Giardiase", "dose": 2, "idade_semanas": 11, "obrigatoria": False, "reforco_anual": True,
     "nome": "Giardiase - 2a dose", "descricao": "Segunda dose da vacina contra giardiase. Aplicada 21-28 dias apos a 1a dose."},
    # ── GATOS — V4 ──
    {"especie": "gato", "grupo": "V4", "dose": 1, "idade_semanas": 8,  "obrigatoria": True, "reforco_anual": True,
     "nome": "V4 - 1a dose", "descricao": "Quadrupla felina. Protege contra rinotraqueite, calicivirose, panleucopenia e clamidiose."},
    {"especie": "gato", "grupo": "V4", "dose": 2, "idade_semanas": 12, "obrigatoria": True, "reforco_anual": True,
     "nome": "V4 - 2a dose", "descricao": "Segunda dose da V4. Reforco 3-4 semanas apos a 1a dose."},
    {"especie": "gato", "grupo": "V4", "dose": 3, "idade_semanas": 16, "obrigatoria": True, "reforco_anual": True,
     "nome": "V4 - 3a dose", "descricao": "Terceira e ultima dose inicial da V4. Completa a imunizacao basica do filhote."},
    {"especie": "gato", "grupo": "V4", "dose": 4, "idade_semanas": 68, "obrigatoria": True, "reforco_anual": True,
     "nome": "V4 - Reforco Anual", "descricao": "Reforco anual da quadrupla felina. Manter por toda a vida do gato."},
    # ── GATOS — Antirrabica ──
    {"especie": "gato", "grupo": "Antirrabica", "dose": 1, "idade_semanas": 16, "obrigatoria": True, "reforco_anual": True,
     "nome": "Antirrabica - 1a dose", "descricao": "Vacina antirrabica felina, obrigatoria por lei. Aplicada a partir de 4 meses."},
    {"especie": "gato", "grupo": "Antirrabica", "dose": 2, "idade_semanas": 68, "obrigatoria": True, "reforco_anual": True,
     "nome": "Antirrabica - Reforco Anual", "descricao": "Reforco anual obrigatorio da antirrabica felina."},
    # ── GATOS — FeLV ──
    {"especie": "gato", "grupo": "FeLV", "dose": 1, "idade_semanas": 9,  "obrigatoria": False, "reforco_anual": True,
     "nome": "FeLV - 1a dose", "descricao": "Vacina contra Leucemia Viral Felina. Exige teste negativo de FeLV antes da aplicacao."},
    {"especie": "gato", "grupo": "FeLV", "dose": 2, "idade_semanas": 13, "obrigatoria": False, "reforco_anual": True,
     "nome": "FeLV - 2a dose", "descricao": "Segunda dose da FeLV. Aplicada 3-4 semanas apos a 1a dose."},
    {"especie": "gato", "grupo": "FeLV", "dose": 3, "idade_semanas": 65, "obrigatoria": False, "reforco_anual": True,
     "nome": "FeLV - Reforco Anual", "descricao": "Reforco anual da FeLV. Essencial para gatos com acesso ao exterior."},
]


def seed_db(db: Session) -> None:
    """Insere dados iniciais se o banco estiver vazio. Idempotente."""
    if db.query(Raca).count() > 0:
        return  # Banco já populado

    racas_criadas = {}
    for dados in RACAS:
        raca = Raca(**dados)
        db.add(raca)
        db.flush()
        racas_criadas[dados["nome"]] = raca

    for raca_nome, cuidados_lista in CUIDADOS_POR_RACA.items():
        raca = racas_criadas.get(raca_nome)
        if not raca:
            continue
        for dados in cuidados_lista:
            db.add(Cuidado(raca_id=raca.id, **dados))

    for dados in CALENDARIO_VACINAL:
        db.add(VacinaRecomendada(**dados))

    db.commit()
