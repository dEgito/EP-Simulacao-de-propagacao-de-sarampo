## EP-Simulacao-de-propagacao-de-sarampo

**Danielly Egito de Moura¹**  
¹ Departamento de Estatística e Informática Universidade Federal Rural de Pernambuco (UFRPE) – Recife, PE – Brasil  
¹danielly.egitom@ufrpe.br 

**Resumo:** *A cobertura vacinal possui um papel central no controle epidemiológico do sarampo, especialmente ao considerar a sua taxa de transmissão e o impacto imunológico. Este estudo propõe um modelo baseado em autômatos celulares para simular a dinâmica de propagação espaço-temporal do vírus em uma população fechada, considerando os estados Suscetível, Infectado e Recuperado (SIR) por meio de interações locais. O modelo computacional foi implementado em Python, utilizando os parâmetros biológicos reais da doença em três testes. Os resultados indicam um avanço acelerado da contaminação, concentrando o pico de doentes em menos de duas semanas e infectando o grupo inteiro. A análise paramétrica aponta que o contato contínuo por vizinhanças é capaz de sustentar grandes surtos mesmo com variantes mais fracas do vírus. O comportamento observado nas simulações valida os alertas das autoridades de saúde sobre a queda na cobertura vacinal.*

## Descrição do repositório:

- Pasta de Resultados:
  Pasta contendo as imagens geradas pelas simulações.
  Cada experimento apresenta:
  - Figura com o início, pico e final da epidemia
  - Gráfico da evolução temporal da infecção
  - Gráfico da variação paramétrica do coeficiente de contágio (beta) com gama fixo

- Artigo final:
  Versão final do artigo que descreve o modelo, metodologia e a análise dos resultados obtidos nas simulações.

- Index.py:
  Versão do código que simula a propagação do sarampo em uma população fechada, de acordo com o modelo SIR.

- Pseudocódigo.txt:
  Representação abstrata da lógica do modelo.


## Parâmetros do modelo:

Todos as versões presentes no repositório utilizam os arranjo estável de parámetros definidos da seguinte maneira:

- n = 20                       # tamanho da grade (NxN)
- beta = 0.4                   # probabilidade de transmissão por vizinho infectado
- gama = 0.125                 # probabilidade de recuperação (1/8 dias)
- iteracoes = 200
