# TPSoft

A detecção de eventos raros de neutrinos e matéria escura é bastante desafiadora devido à reduzida seção de choque dessas partículas. Nestes casos, o uso de uma câmara de projeção temporal (TPC) é de extrema relevância na reconstrução de traços e calorimetria desses eventos. Este software dedica-se à simulação de sinais que permitem a identificação da interação de partículas em experimentos com câmaras de projeção temporal utilizando argônio líquido como meio (LArTPC). 

Para isto, o software divide as paredes da TPC em uma grade de bins. Para cada uma dessas sub-regiões, o ângulo sólido a partir de um determinado ponto na trajetória de uma partícula é determinado e uma quantidade específica de fótons é sorteada através dessas probabilidades. Ao iterar o procedimento pela totalidade de trajetória, obtemos a posição de todos os encontros com as placas da TPC e conseguimos simular a coleção como um todo.

### Arquitetura

A estrutura do código vem dividida em duas classes. A primeira, Partícula(), é responsável pela construção, representação e interação de feixes incidentes na TPC.

#### Métodos

- construtor(x_emissão, y_emissão, z_emissão, teta, fi): constroe um feixe incidente a partir dos parâmetros x_emissão, y_emissão, z_emissão, teta e fi.
- plotar(TPC, eixo): representa a trajetória do feixe em um sistema de coordenadas cartesiano. O método necessita de um parâmetro TPC, um objeto que discutiremos a seguir, e um sistema de eixos no qual a trajetória será traçada. 

A segunda classe é responsável pela construção, representação e configuração de uma TPC. No pacote, ela recebe o nome de TPC(). 

#### Métodos

- construtor(resolução, **kwargs): define uma TPC em diversas geometrias. Até o momento, a geometria _paralel_ é a única implmentada. A sua construção depende de um parâmetro resolução, que indica a quantidade de bins que suas paredes serão divididas para a simulação de coleção, e os parâmetros de dimensão comprimento_x, comprimento_y e comprimento_z.
- plotar(eixo): representa a TPC em um sistema de coordenadas cartesiano.
- coleção_de_luz(Partícula, delta, eixo, **kwargs): plota a coleção de luz de um objeto Partícula em um determinado plano_de_coleção (por exemplo, x=0), representado por um sistema de eixos específico e um tipo específico (hist para histograma e scatter para um conjunto de pontos). O delta escolhido representa o intervalo no espaço entre as emissões de luz na trajetória da Partícula.

Outros métodos também fazem parte do código. Estes, por sua vez, fogem do intuíto desse documento e, portanto, não serão discutidos.


# Release 2.0 

A segunda versão do software engloba uma série de novas melhorias. Anteriormente, o sorteio utilizava uma outra metodologia que acabou se mostrando pouco favorável. Buscando ultrapassá-la, o uso de ângulos sólidos e um grid de probabilidades foi implementado e resultados mais concisos foram observados.

Além disso, a expansibilidade de geometrias para a classe TPC também foi implementada. Agora, novas geometrias podem ser desenvolvidas sem a necessidade de alteração do código base. 

# Contato

Se surgirem quaisquer dúvidas à respeito do software, não hesitem em entrar em contato.

Autor: Henrique Gallon Gadioli.

E-mail institucional: h.gallon@aluno.ufabc.edu.br