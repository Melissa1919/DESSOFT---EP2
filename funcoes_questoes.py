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