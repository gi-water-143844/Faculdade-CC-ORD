Primeiro trabalho de ORD:
  - Fazer um programa que através da flag '-b' ele crie arquivos binários ordenados dos índices primários e secundários do arquivo 'games.dat', e a lista invertida
  que estará ordenada:
    - O índice primário é o ID do jogo, e os secundários são gênero e publicadora.
    - A lista de índices primários consiste em tuplas com 2 campos: id (int) e byte-offset (int), além disso deve estar ordenado.
    - A lista de gêneros e publicadoras consiste em listas de 2 campos: o nome (str) e a posição do menor ID na lista invertida (int), além disso deve estar ordenado.
    - A lista invertida contém listas de 3 campos: id (int), próximo gênero (int) e próxima publicadora (int), os IDs não estão ordenados, 
      pois foram colocados na ordem que consta o arquivo 'games.dat'.
  - Após essa organização, o programa deve rodar o arquivo 'operacoes.txt', ler cada linha e aplicar sua devida operação:
    - As operações são bp (busca primário), bs1 (busca secundária por gênero), bs2 (busca secundária por publicadora), i (inserção) e r (remoção).
    - BP: busca o id na lista dos índices primários através da busca binária. Caso o id seja encontrado, retorna seu byte-offset
      e faz a busca do registro no arquivo 'games.dat' e o retorna.
    - BS1/BS2: busca o gênero/publicadora na lista de índices secundários através da busca binária. Caso seja encontrado, será buscado na lista invertida
      a posição salva, e enquanto a posição ser diferente de -1, os IDs de cada posição serão salvos em uma lista auxiliar. A lista auxiliar será utilizada
      para fazer a busca primária de cada id e salvar em uma nova lista auxiliar seus respectivos byte-offset. Por fim, será feito uma busca no 'games.dat' de cada
      byte-offset para retornar os registros daquele(a) gênero/publicadora.
    - I: verifica se o id não está na lista de índices primários, caso não esteja ele escreve o novo registro no final do arquivo 'games.dat' e atualiza os
      índices e a lista invertida.
    - R: verifica se o id consta na lista de índices primários, caso esteja ele irá buscar seu byte-offset através do busca primário e se posicionar no 'games.dat'
      onde ele irá ler seu tamanho, e no primeiro caracter do registro (no caso,o primeiro número do id) ele irá substituir por um '*' que será utilizado na
      compactação para identificar arquivos 'excluídos'. Após isso deve-se remover o id da lista de índices primários e atualizar a lista invertida.
  - Por fim, através da flag '-c' o programa deve compactar o arquivo 'games.dat' reescrendo ele com exceção dos arquivos 'excluídos'. Portando, essa função
  irá ler cada registro, e caso ele não tenha um '*', ele será escrito em um novo arquivo ('games_novo.dat'). Caso encontre um registro excluído, ele irá
  ler seu tamanho e 'pular' esse registro.
