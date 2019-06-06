# TPSoft

A detec��o de eventos raros de neutrinos e mat�ria escura � bastante desafiadora devido � reduzida se��o de choque dessas part�culas. Nestes casos, o uso de uma c�mara de proje��o temporal (TPC) � de extrema relev�ncia na reconstru��o de tra�os e calorimetria desses eventos. Este software dedica-se � simula��o de sinais que permitem a identifica��o da intera��o de part�culas em experimentos com c�maras de proje��o temporal utilizando arg�nio l�quido como meio (LArTPC). 

# Release 1.0

Em sua primeira vers�o, o software engloba uma s�rie de ferramentas para a simula��o dessas condi��es. Todas elas podem ser encontradas no pacote TPSoft que est� inclu�do na ra�z do diret�rio. Tamb�m est�o inclu�dos no reposit�rio alguns exemplos de simula��es prontas para serem executadas.

### Arquitetura

A estrutura do c�digo vem dividida em duas classes. A primeira, Part�cula(), � respons�vel pela constru��o, representa��o e intera��o de feixes incidentes na TPC.

#### M�todos

- construtor(x_emiss�o, y_emiss�o, z_emiss�o, teta, fi): constroe um feixe incidente a partir dos par�metros x_emiss�o, y_emiss�o, z_emiss�o, teta e fi.
- plotar(TPC, eixo): representa a trajet�ria do feixe em um sistema de coordenadas cartesiano. O m�todo necessita de um par�metro TPC, um objeto que discutiremos a seguir, e um sistema de eixos no qual a trajet�ria ser� tra�ada. 

A segunda classe � respons�vel pela constru��o, representa��o e configura��o de uma TPC. No pacote, ela recebe o nome de TPC(). 

#### M�todos

- construtor(comprimento_x, comprimento_y, comprimento_z): constroe uma TPC em forma de paralelep�pedo com dimens�es comprimento_x, comprimento_y e compriemento_z.
- plotar(eixo): representa a TPC em um sistema de coordenadas cartesiano. A origem do paralelep�pedo sempre coincide com a origem do sistema. 
- cole��o_de_luz(Part�cula, delta, eixo, plano_de_cole��o, tipo): plota a cole��o de luz de um objeto Part�cula em um determinado plano_de_cole��o (por exemplo, x=0), representado por um sistema de eixos espec�fico e um tipo espec�fico (hist para histograma e scatter para um conjunto de pontos). O delta escolhido representa o intervalo no espa�o entre as emiss�es de luz na trajet�ria da Part�cula.

Outros m�todos tamb�m fazem parte do c�digo. Estes, por sua vez, fogem do intu�to desse documento e, portanto, n�o ser�o discutidos.

### Bugs

Durante o desenvolvimento, me deparei com algumas situa��es em que a cole��o de luz simulada n�o encaixava com o esperado teoricamente. Ao simular a detec��o para um feixe paralelo � base na dire��o y, o padr�o resultante para um plano z constante e x constante resultaram diferente. Um com um feixe bastante definido e outro com uma distribui��o crescente no sentido do centro da placa.
Esse problema est� exemplificado no exemplo muon_crossing_x_y_z e fico aberto para qualquer sugest�o.

Qualquer outra d�vida sobre o software, n�o deixem de me procurar.

Autor: Henrique Gallon Gadioli.

E-mail institucional: h.gallon@aluno.ufabc.edu.br