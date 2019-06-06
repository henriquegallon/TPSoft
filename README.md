# TPSoft

<<<<<<< HEAD
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
=======
A detecÃ§Ã£o de eventos raros de neutrinos e matÃ©ria escura Ã© bastante desafiadora devido Ã  reduzida seÃ§Ã£o de choque dessas partÃ­culas. Nestes casos, o uso de uma cÃ¢mara de projeÃ§Ã£o temporal (TPC) Ã© de extrema relevÃ¢ncia na reconstruÃ§Ã£o de traÃ§os e calorimetria desses eventos. Este software dedica-se Ã  simulaÃ§Ã£o de sinais que permitem a identificaÃ§Ã£o da interaÃ§Ã£o de partÃ­culas em experimentos com cÃ¢maras de projeÃ§Ã£o temporal utilizando argÃ´nio lÃ­quido como meio (LArTPC). 

# Release 1.0

Em sua primeira versÃ£o, o software engloba uma sÃ©rie de ferramentas para a simulaÃ§Ã£o dessas condiÃ§Ãµes. Todas elas podem ser encontradas no pacote TPSoft que estÃ¡ incluÃ­do na raÃ­z do diretÃ³rio. TambÃ©m estÃ£o incluÃ­dos no repositÃ³rio alguns exemplos de simulaÃ§Ãµes prontas para serem executadas.

### Arquitetura

A estrutura do cÃ³digo vem dividida em duas classes. A primeira, PartÃ­cula(), Ã© responsÃ¡vel pela construÃ§Ã£o, representaÃ§Ã£o e interaÃ§Ã£o de feixes incidentes na TPC.

#### MÃ©todos

- construtor(x_emissÃ£o, y_emissÃ£o, z_emissÃ£o, teta, fi): constroe um feixe incidente a partir dos parÃ¢metros x_emissÃ£o, y_emissÃ£o, z_emissÃ£o, teta e fi.
- plotar(TPC, eixo): representa a trajetÃ³ria do feixe em um sistema de coordenadas cartesiano. O mÃ©todo necessita de um parÃ¢metro TPC, um objeto que discutiremos a seguir, e um sistema de eixos no qual a trajetÃ³ria serÃ¡ traÃ§ada. 

A segunda classe Ã© responsÃ¡vel pela construÃ§Ã£o, representaÃ§Ã£o e configuraÃ§Ã£o de uma TPC. No pacote, ela recebe o nome de TPC(). 

#### MÃ©todos

- construtor(comprimento_x, comprimento_y, comprimento_z): constroe uma TPC em forma de paralelepÃ­pedo com dimensÃµes comprimento_x, comprimento_y e compriemento_z.
- plotar(eixo): representa a TPC em um sistema de coordenadas cartesiano. A origem do paralelepÃ­pedo sempre coincide com a origem do sistema. 
- coleÃ§Ã£o_de_luz(PartÃ­cula, delta, eixo, plano_de_coleÃ§Ã£o, tipo): plota a coleÃ§Ã£o de luz de um objeto PartÃ­cula em um determinado plano_de_coleÃ§Ã£o (por exemplo, x=0), representado por um sistema de eixos especÃ­fico e um tipo especÃ­fico (hist para histograma e scatter para um conjunto de pontos). O delta escolhido representa o intervalo no espaÃ§o entre as emissÃµes de luz na trajetÃ³ria da PartÃ­cula.

Outros mÃ©todos tambÃ©m fazem parte do cÃ³digo. Estes, por sua vez, fogem do intuÃ­to desse documento e, portanto, nÃ£o serÃ£o discutidos.

### Bugs

Durante o desenvolvimento, me deparei com algumas situaÃ§Ãµes em que a coleÃ§Ã£o de luz simulada nÃ£o encaixava com o esperado teoricamente. Ao simular a detecÃ§Ã£o para um feixe paralelo Ã  base na direÃ§Ã£o y, o padrÃ£o resultante para um plano z constante e x constante resultaram diferente. Um com um feixe bastante definido e outro com uma distribuiÃ§Ã£o crescente no sentido do centro da placa.
Esse problema estÃ¡ exemplificado no exemplo muon_crossing_x_y_z e fico aberto para qualquer sugestÃ£o.

Qualquer outra dÃºvida sobre o software, nÃ£o deixem de me procurar.

Autor: Henrique Gallon Gadioli.

E-mail institucional: h.gallon@aluno.ufabc.edu.br
>>>>>>> fbfb9ecccb501479662011ab154c47073d19fc29
