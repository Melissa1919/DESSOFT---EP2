"""
Fortuna DesSoft - EP2
Jogo de perguntas e respostas estilo "Show do Milhão".
 
Usa as 7 funções obrigatórias implementadas em funcoes.py:
- transforma_base
- valida_questao
- valida_lista_questoes
- sorteia_questao
- sorteia_questao_inedita
- questao_para_texto
- gera_ajuda
"""


import json

from funcoes import (
    transforma_base,
    valida_questao,
    valida_questoes,
    sorteia_questao,
    sorteia_questao_inedita,
    questao_para_texto,
    gera_ajuda,
)

# ---------------------------------------------------------------------------
# Configurações do jogo
# ---------------------------------------------------------------------------

CAMINHO_BASE = "perguntas.json"

PREMIOS = [1000, 5000, 10000, 30000, 50000, 100000, 300000, 500000, 1000000]

# as 9 perguntas do jogo: 3 fáceis, 3 médias, 3 difíceis (na ordem dos prêmios)
NIVEL_POR_INDICE = ["facil"] * 3 + ["medio"] * 3 + ["dificil"] * 3

PULOS_INICIAIS = 3
AJUDAS_INICIAIS = 2

OPCOES_VALIDAS = ["A", "B", "C", "D", "PULA", "AJUDA"]

# ---------------------------------------------------------------------------
# Cores 
# ---------------------------------------------------------------------------

RESET = "\033[0m"
VERDE = "\033[92m"
AMARELO = "\033[93m"
VERMELHO = "\033[91m"
CIANO = "\033[96m"
NEGRITO = "\033[1m"


def cor_por_premio(premio):
    """Retorna uma cor conforme o valor do prêmio atual."""
    if premio >= 300000:
        return VERMELHO
    if premio >= 30000:
        return AMARELO
    return VERDE


def imprime_titulo(texto):
    print(f"\n{NEGRITO}{CIANO}{texto}{RESET}")


def imprime_erro(texto):
    print(f"{VERMELHO}{texto}{RESET}")


def imprime_aviso(texto):
    print(f"{AMARELO}{texto}{RESET}")


def imprime_sucesso(texto):
    print(f"{VERDE}{texto}{RESET}")


def formata_dinheiro(valor):
    return "R$ " + "{:,}".format(valor).replace(",", ".")


# ---------------------------------------------------------------------------
# Carregamento 
# ---------------------------------------------------------------------------

def carrega_base(caminho):
    """Lê o arquivo json, valida a lista de questões e organiza por nível."""
    with open(caminho, "r", encoding="utf-8") as arquivo:
        questoes = json.load(arquivo)

    erros = valida_lista_questoes(questoes)

    if len(erros) > 0:
        imprime_erro("A base de perguntas está inconsistente. Erros encontrados:")
        for indice, erro in erros.items():
            print(f"  Questão {indice}: {erro}")
        raise SystemExit(1)

    return transforma_base(questoes)


# ---------------------------------------------------------------------------
# Interações com o jogador
# ---------------------------------------------------------------------------

def pede_nome():
    nome = ""
    while nome.strip() == "":
        nome = input("Qual é o seu nome? ")
        if nome.strip() == "":
            imprime_erro("O nome não pode ser vazio.")
    return nome.strip()


def exibe_manual(nome):
    imprime_titulo("=" * 50)
    imprime_titulo("BEM-VINDO AO FORTUNA DESSOFT!")
    imprime_titulo("=" * 50)
    print(f"""
Olá, {nome}! As regras são simples:

- Você vai responder {len(PREMIOS)} perguntas, cada uma com 4 alternativas
  (A, B, C ou D).
- A cada resposta correta, seu prêmio aumenta, seguindo esta escada:
  {", ".join(formata_dinheiro(p) for p in PREMIOS)}
- Se errar uma pergunta, perde tudo e o jogo acaba na hora.
- Você tem {PULOS_INICIAIS} pulos: pode pular uma pergunta (ela não conta
  como erro, mas também não aumenta o prêmio) e receber outra pergunta
  do mesmo nível.
- Você tem {AJUDAS_INICIAIS} ajudas: ao usar, o jogo revela 1 ou 2
  alternativas erradas. Só é possível usar 1 ajuda por pergunta.
- Ao acertar qualquer pergunta, você pode escolher parar e sair com o
  prêmio atual, ou continuar para o próximo valor.
- Ao chegar em R$ 1.000.000, o jogo termina automaticamente e você
  vence!
""")


def pede_entrada():
    entrada = input("\nResposta (A, B, C ou D), PULA ou AJUDA: ").strip().upper()
    return entrada


def responde_questao(questao, estado):
    """
    Toca uma única questão até o jogador responder (A/B/C/D) ou decidir
    pular (se ainda tiver pulos). Retorna 'correta', 'errada' ou 'pula'.
    """
    ajuda_usada_nesta_questao = False

    while True:
        entrada = pede_entrada()

        if entrada not in OPCOES_VALIDAS:
            imprime_erro("Opção inválida! Escolha entre A, B, C, D, PULA ou AJUDA.")
            continue

        if entrada == "AJUDA":
            if ajuda_usada_nesta_questao:
                imprime_erro("Você já usou ajuda nesta pergunta!")
                continue
            if estado["ajudas"] <= 0:
                imprime_erro("Você não tem mais ajudas disponíveis!")
                continue

            estado["ajudas"] -= 1
            ajuda_usada_nesta_questao = True
            imprime_aviso(gera_ajuda(questao))
            print(f"(Ajudas restantes: {estado['ajudas']})")
            continue

        if entrada == "PULA":
            if estado["pulos"] > 0:
                estado["pulos"] -= 1
                print(f"(Pulos restantes: {estado['pulos']})")
                return "pula"
            else:
                imprime_erro("Você não tem mais pulos! Responda a pergunta atual.")
                print(questao_para_texto(questao, estado["indice_exibicao"]))
                continue

        # entrada é A, B, C ou D
        if entrada == questao["correta"]:
            return "correta"
        else:
            return "errada"


def joga_partida(base_por_nivel):
    """Joga uma partida completa. Retorna o prêmio final conquistado."""

    estado = {
        "pulos": PULOS_INICIAIS,
        "ajudas": AJUDAS_INICIAIS,
        "indice_exibicao": 0,
    }
    questoes_sorteadas = []
    premio_atual = 0

    for indice, premio in enumerate(PREMIOS):
        nivel = NIVEL_POR_INDICE[indice]
        estado["indice_exibicao"] = indice + 1

        while True:
            questao = sorteia_questao_inedita(base_por_nivel, nivel, questoes_sorteadas)

            cor = cor_por_premio(premio)
            print(f"\n{cor}Prêmio atual: {formata_dinheiro(premio_atual)}{RESET}")
            print(f"{cor}Jogando por: {formata_dinheiro(premio)}{RESET}")
            print(questao_para_texto(questao, indice + 1))

            resultado = responde_questao(questao, estado)

            if resultado == "pula":
                # sorteia outra pergunta do mesmo nível
                continue
            break

        if resultado == "errada":
            imprime_erro(
                f"\nResposta errada! A alternativa correta era "
                f"{questao['correta']}: {questao['opcoes'][questao['correta']]}"
            )
            imprime_erro("Você perdeu tudo e saiu sem nenhum prêmio!")
            return 0

        # resposta correta
        premio_atual = premio
        imprime_sucesso(f"\nResposta correta! Seu prêmio agora é {formata_dinheiro(premio_atual)}")

        if premio_atual == PREMIOS[-1]:
            imprime_sucesso("\nVOCÊ CHEGOU A R$ 1.000.000! VOCÊ VENCEU O FORTUNA DESSOFT!")
            return premio_atual

        continuar = ""
        while continuar not in ["PARAR", "CONTINUAR"]:
            continuar = input(
                "\nDeseja PARAR e sair com o prêmio ou CONTINUAR para a próxima pergunta? "
            ).strip().upper()
            if continuar not in ["PARAR", "CONTINUAR"]:
                imprime_erro("Digite PARAR ou CONTINUAR.")

        if continuar == "PARAR":
            imprime_sucesso(f"\nVocê saiu com {formata_dinheiro(premio_atual)}!")
            return premio_atual

    return premio_atual


def main():
    try:
        base_por_nivel = carrega_base(CAMINHO_BASE)
    except FileNotFoundError:
        imprime_erro(f"Arquivo de base '{CAMINHO_BASE}' não encontrado.")
        return
    except (json.JSONDecodeError, KeyError) as erro:
        imprime_erro(f"Erro ao ler a base de perguntas: {erro}")
        return

    nome = pede_nome()
    exibe_manual(nome)

    jogar_de_novo = "S"
    while jogar_de_novo == "S":
        joga_partida(base_por_nivel)

        jogar_de_novo = ""
        while jogar_de_novo not in ["S", "N"]:
            jogar_de_novo = input(f"\n{nome}, deseja jogar novamente? (S/N) ").strip().upper()
            if jogar_de_novo not in ["S", "N"]:
                imprime_erro("Digite S para sim ou N para não.")

    print("\nObrigado por jogar o Fortuna DesSoft!")


if __name__ == "__main__":
    main()