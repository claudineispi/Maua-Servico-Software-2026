"""
Seed inicial do banco de dados.
Executado no startup da API, após Base.metadata.create_all.
Idempotente: não insere dados que já existem.
"""
from sqlalchemy.orm import Session
from app.models.models import Raca, Cuidado

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

CUIDADOS_GOLDEN = [
    {
        "categoria": "alimentacao",
        "titulo": "Ração Premium para Raças Grandes",
        "descricao": "Golden Retrievers necessitam de ração específica para raças grandes com controle de cálcio e fósforo para proteger as articulações.",
        "frequencia": "diário",
        "prioridade": "alta",
    },
    {
        "categoria": "higiene",
        "titulo": "Escovação do Pelo",
        "descricao": "O pelo dourado do Golden precisa ser escovado regularmente para evitar nós e remover pelos mortos, especialmente na muda.",
        "frequencia": "semanal",
        "prioridade": "alta",
    },
    {
        "categoria": "saude",
        "titulo": "Monitoramento de Displasia Coxofemoral",
        "descricao": "Golden Retrievers são predispostos a displasia coxofemoral. Manter peso ideal e fazer exames regulares é essencial.",
        "frequencia": "anual",
        "prioridade": "alta",
    },
]


def seed_db(db: Session) -> None:
    """Insere dados iniciais se o banco estiver vazio. Idempotente."""
    if db.query(Raca).count() > 0:
        return  # Banco já populado, não faz nada

    racas_criadas = {}
    for dados in RACAS:
        raca = Raca(**dados)
        db.add(raca)
        db.flush()  # Obtém o ID sem commitar
        racas_criadas[dados["nome"]] = raca

    golden = racas_criadas.get("Golden Retriever")
    if golden:
        for dados in CUIDADOS_GOLDEN:
            db.add(Cuidado(raca_id=golden.id, **dados))

    db.commit()
