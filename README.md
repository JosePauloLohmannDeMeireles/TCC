Visão Geral da API
Esta API oferece funcionalidades para cadastro e validação facial através de dois endpoints principais. A API permite validação do roto no cadastro de fotos faciais em diferentes posições e a validação de uma imagem facial em tempo real, retornando informações sobre a biometria facial.

Como Executar
Build do Contêiner Docker: Execute build para criar o contêiner Docker da aplicação.
Start do Contêiner: Execute start para inicializar o contêiner. A aplicação estará acessível na porta 5000.
Endpoints
1. criar_face
Descrição: Este endpoint recebe uma foto e verifica se o rosto está na posição correta para cadastro.
Rota: /criar_face
Método: POST
Parâmetros:
position: Número indicando a posição da foto (1 a 5), onde cada número representa uma orientação específica (frontal, esquerda, direita, acima e abaixo).
image: A imagem que será verificada quanto à posição.
Retorno:
JSON com as seguintes chaves:
mensagem: Mensagem sobre o resultado da verificação.
valido: Confirmação se a posição está correta (true ou false).
sugestao: Sugestão para melhorar o alinhamento do rosto, se necessário.
2. validate_face
Descrição: Este endpoint recebe múltiplas fotos de referência de diferentes posições do rosto para validação de um rosto em tempo real.
Rota: /validate_face
Método: POST
Parâmetros:
image_url_ref: Array contendo URLs de imagens de referência do rosto em diferentes posições.
image_url: URL da imagem a ser validada.
Retorno:
JSON com as seguintes chaves:
valido: Indica se o rosto foi validado com sucesso (true ou false).
mensagem: Mensagem com o status da validação (válido ou inválido).
Exemplos de Uso
Usando uma Ferramenta como Postman:

No Postman, envie uma requisição POST para /criar_face ou /validate_face com os parâmetros descritos acima no corpo da requisição.

