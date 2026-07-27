# DESSOFT---EP2
Melissa Sumaya Kheir 

# Fortuna DesSoft

Jogo de perguntas e respostas no estilo "Show do Milhão", feito em Python
para o Exercício Programa (EP2) da disciplina.

## Como jogar

Pré-requisito: Python 3 instalado.

```bash
python3 main.py
```

O jogo vai pedir seu nome, mostrar um manual rápido e começar a rodada de
perguntas.

### Regras

- São 9 perguntas, com dificuldade crescente (fáceis → médias → difíceis).
- A cada acerto, o prêmio sobe conforme a escada:
  `1.000 → 5.000 → 10.000 → 30.000 → 50.000 → 100.000 → 300.000 → 500.000 → 1.000.000`
- Errar uma pergunta encerra o jogo na hora, sem nenhum prêmio.
- Após cada acerto (exceto o último), você escolhe entre **PARAR** (sai com
  o prêmio atual) ou **CONTINUAR** (arrisca a próxima pergunta).
- Chegar a R$ 1.000.000 encerra o jogo automaticamente com vitória.

### Opções em cada pergunta

- `A`, `B`, `C` ou `D`: responde a pergunta.
- `PULA`: troca a pergunta atual por outra do mesmo nível (você tem **3
  pulos** no total, para o jogo inteiro).
- `AJUDA`: revela 1 ou 2 alternativas erradas (você tem **2 ajudas** no
  total; só é possível usar 1 ajuda por pergunta).

Ao final de cada partida, o jogo pergunta se você quer jogar de novo, sem
precisar reiniciar o programa.

## Estrutura do projeto

```
.
├── main.py          # Programa principal: laço do jogo, interação com o usuário
├── funcoes.py        # As 7 funções obrigatórias do EP + lógica de sorteio/validação
├── perguntas.json     # Base de perguntas (edite/adicione perguntas aqui)
└── README.md
```

### As 7 funções obrigatórias (em `funcoes.py`)

| Função                    | O que faz                                                          |
|---------------------------|---------------------------------------------------------------------|
| `transforma_base`         | Reorganiza a lista de perguntas em um dicionário agrupado por nível  |
| `valida_questao`          | Valida se uma única pergunta está bem formada                       |
| `valida_lista_questoes`   | Valida a lista inteira de perguntas, devolvendo os erros encontrados |
| `sorteia_questao`         | Sorteia uma pergunta aleatória de um nível                           |
| `sorteia_questao_inedita` | Sorteia uma pergunta de um nível que ainda não foi usada na partida  |
| `questao_para_texto`      | Formata uma pergunta em texto pronto para exibir no terminal         |
| `gera_ajuda`               | Sorteia 1 ou 2 alternativas erradas para dar de dica                 |

## Adicionando novas perguntas

Edite `perguntas.json` e adicione um novo objeto no formato:

```json
{
  "titulo": "Sua pergunta aqui?",
  "nivel": "facil",
  "opcoes": {"A": "opção 1", "B": "opção 2", "C": "opção 3", "D": "opção 4"},
  "correta": "A"
}
```

`nivel` deve ser `"facil"`, `"medio"` ou `"dificil"`. Ao iniciar, o jogo
valida automaticamente a base inteira e avisa se alguma pergunta estiver
mal formatada.

## Autor

Feito individualmente para o EP2 da disciplina, com commits registrando o
histórico de desenvolvimento.