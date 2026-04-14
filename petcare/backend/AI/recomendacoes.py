from datetime import date
from typing import Dict, List, Any, Tuple


def calcular_idade(data_nascimento: date) -> int:
    """
    Calcula a idade do pet em anos completos.

    para data_nascimento: data de nascimento do pet
    return: idade em anos
    """
    hoje = date.today()
    return (
        hoje.year
        - data_nascimento.year
        - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
    )


def calcular_idade_detalhada(data_nascimento: date) -> Tuple[int, int]:
    """
    Calcula a idade do pet em anos e meses completos.

    para data_nascimento: data de nascimento do pet
    return: tupla (anos, meses_restantes) — ex: (1, 2) para 1 ano e 2 meses
    """
    hoje = date.today()
    anos = hoje.year - data_nascimento.year
    meses = hoje.month - data_nascimento.month
    if hoje.day < data_nascimento.day:
        meses -= 1
    if meses < 0:
        anos -= 1
        meses += 12
    return max(anos, 0), max(meses, 0)


def gerar_recomendacoes(pet: Any, raca: Any) -> Dict[str, Any]:
    """
    Recebe um Pet e sua Raça e retorna recomendações personalizadas
    de atividades e cuidados..

    para pet: objeto Pet
    para raca: objeto Raca
    return: dicionário com recomendações e alertas
    """

    idade = calcular_idade(pet.data_nascimento)
    anos, meses = calcular_idade_detalhada(pet.data_nascimento)

    recomendacoes: Dict[str, Any] = {
        "frequencia_semanal": "",
        "intensidade": "",
        "atividades_sugeridas": [],
        "cuidados_prioritarios": [],
        "alertas": []
    }

    # REGRA 1 - NÍVEL DE ATIVIDADE DA RAÇA
    if raca.nivel_atividade == "alto":
        recomendacoes["frequencia_semanal"] = "5 a 7 vezes por semana"
        recomendacoes["intensidade"] = "alta"
        recomendacoes["atividades_sugeridas"] = [
            "caminhada",
            "corrida leve",
            "brincadeiras ativas"
        ]
        recomendacoes["cuidados_prioritarios"].append(
            "estimulação física diária"
        )

    elif raca.nivel_atividade == "medio":
        recomendacoes["frequencia_semanal"] = "3 a 4 vezes por semana"
        recomendacoes["intensidade"] = "moderada"
        recomendacoes["atividades_sugeridas"] = [
            "caminhada",
            "brincadeiras leves"
        ]
        recomendacoes["cuidados_prioritarios"].append(
            "manutenção da rotina de exercícios"
        )

    else:
        recomendacoes["frequencia_semanal"] = "2 a 3 vezes por semana"
        recomendacoes["intensidade"] = "leve"
        recomendacoes["atividades_sugeridas"] = [
            "caminhada curta",
            "enriquecimento ambiental"
        ]
        recomendacoes["cuidados_prioritarios"].append(
            "estimulação leve e regular"
        )

    # REGRA 2 - PET IDOSO (só avalia se a raça tem expectativa de vida definida)
    if raca.expectativa_vida_anos and idade > (raca.expectativa_vida_anos * 0.75):
        recomendacoes["intensidade"] = "leve"
        recomendacoes["alertas"].append(
            "Pet idoso: evite atividades intensas e de alto impacto"
        )
        recomendacoes["cuidados_prioritarios"].append(
            "acompanhamento veterinário regular"
        )

    # REGRA 3 - PORTE DO PET
    if raca.porte == "grande":
        recomendacoes["cuidados_prioritarios"].append(
            "atenção especial às articulações"
        )

    # REGRA 4 - FILHOTES
    if idade < 1:
        recomendacoes["alertas"].append(
            "Filhote: priorize socialização e atividades adequadas à idade"
        )
        recomendacoes["cuidados_prioritarios"].append(
            "treinamento básico e socialização"
        )

    return {
        "pet_id": pet.id,
        "idade_anos": idade,
        "idade_anos_detalhe": anos,
        "idade_meses_detalhe": meses,
        "perfil_ia": raca.nivel_atividade,
        "recomendacoes": recomendacoes
    }