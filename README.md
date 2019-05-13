# TPSoft

A detecção de eventos raros de neutrinos e matéria escura é bastante desafiadora devido à reduzida seção de choque dessas partículas. Nestes casos, o uso de uma câmara de projeção temporal (TPC) é de extrema relevância na reconstrução de traços e calorimetria desses eventos. Este software dedica-se à simulação de sinais que permitem a identificação da interação de partículas em experimentos com câmaras de projeção temporal utilizando argônio líquido como meio (LArTPC). 

# Release 1.0

Em sua primeira versão, o software engloba uma série de ferramentas para a simulação dessas condições. Todas elas podem ser encontradas no pacote TPSoft que está incluído na raíz do diretório. Também estão incluídos no repositório alguns exemplos de simulações prontas para serem executadas.

### Arquitetura

A estrutura do código vem dividida em duas classes. A primeira, Partícula(), é responsável pela construção, representação e interação de feixes incidentes na TPC.

#### Métodos

- construtor(x_emissão, y_emissão, z_emissão, teta, fi): constroe um feixe incidente a partir dos parâmetros x_emissão, y_emissão, z_emissão, teta e fi.
- plotar(TPC, eixo): representa a trajetória do feixe em um sistema de coordenadas cartesiano. O método necessita de um parâmetro TPC, um objeto que discutiremos a seguir, e um sistema de eixos no qual a trajetória será traçada. 

A segunda classe é responsável pela construção, representação e configuração de uma TPC. No pacote, ela recebe o nome de TPC(). 

#### Métodos

- construtor(comprimento_x, comprimento_y, comprimento_z): constroe uma TPC em forma de paralelepípedo com dimensões comprimento_x, comprimento_y e compriemento_z.
- plotar(eixo): representa a TPC em um sistema de coordenadas cartesiano. A origem do paralelepípedo sempre coincide com a origem do sistema. 
- coleção_de_luz(Partícula, delta, eixo, plano_de_coleção, tipo): plota a coleção de luz de um objeto Partícula em um determinado plano_de_coleção (por exemplo, x=0), representado por um sistema de eixos específico e um tipo específico (hist para histograma e scatter para um conjunto de pontos). O delta escolhido representa o intervalo no espaço entre as emissões de luz na trajetória da Partícula.

Outros métodos também fazem parte do código. Estes, por sua vez, fogem do intuíto desse documento e, portanto, não serão discutidos.

### Bugs

Durante o desenvolvimento, me deparei com algumas situações em que a coleção de luz simulada não encaixava com o esperado teoricamente. Ao simular a detecção para um feixe paralelo à base na direção y, o padrão resultante para um plano z constante e x constante resultaram diferente. Um com um feixe bastante definido e outro com uma distribuição crescente no sentido do centro da placa.
Esse problema está exemplificado no exemplo muon_crossing_x_y_z e fico aberto para qualquer sugestão.

Qualquer outra dúvida sobre o software, não deixem de me procurar.

Autor: Henrique Gallon Gadioli.

E-mail institucional: h.gallon@aluno.ufabc.edu.br
