def transforma_base(questoes):
    
    por_nivel = {}

    i = 0
    while i < len(questoes):
        questao = questoes[i]
        nivel = questao["nivel"]

        if nivel not in por_nivel:
            por_nivel[nivel] = []

        por_nivel[nivel].append(questao)
        i += 1

    return por_nivel

def valida_questao(questao):
    retorno = {}

    # verifica se as chaves principais existem
    if 'titulo' not in questao:
        retorno['titulo'] = 'nao_encontrado'
    if 'nivel' not in questao:
        retorno['nivel'] = 'nao_encontrado'
    if 'opcoes' not in questao:
        retorno['opcoes'] = 'nao_encontrado'
    if 'correta' not in questao:
        retorno['correta'] = 'nao_encontrado'

    # verifica se tem exatamente 4 chaves
    if len(questao) != 4:
        retorno['outro'] = 'numero_chaves_invalido'

    # valida titulo
    if 'titulo' in questao:
        if questao['titulo'].strip() == '':
            retorno['titulo'] = 'vazio'

    # valida nivel
    if 'nivel' in questao:
        if questao['nivel'] not in ['facil', 'medio', 'dificil']:
            retorno['nivel'] = 'valor_errado'

    # valida correta
    if 'correta' in questao:
        if questao['correta'] not in ['A', 'B', 'C', 'D']:
            retorno['correta'] = 'valor_errado'

    # valida opcoes
    if 'opcoes' in questao:
        opcoes = questao['opcoes']

        if len(opcoes) != 4:
            retorno['opcoes'] = 'tamanho_invalido'
        else:
            if set(opcoes.keys()) != {'A', 'B', 'C', 'D'}:
                retorno['opcoes'] = 'chave_invalida_ou_nao_encontrada'
            else:
                vazias = {}

                if opcoes['A'].strip() == '':
                    vazias['A'] = 'vazia'
                if opcoes['B'].strip() == '':
                    vazias['B'] = 'vazia'
                if opcoes['C'].strip() == '':
                    vazias['C'] = 'vazia'
                if opcoes['D'].strip() == '':
                    vazias['D'] = 'vazia'

                if len(vazias) > 0:
                    retorno['opcoes'] = vazias

    return retorno