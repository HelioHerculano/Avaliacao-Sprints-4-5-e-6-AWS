# Avaliação Sprints 4, 5 e 6 - Programa de Bolsas Compass UOL / AWS e Moçambique

Avaliação da quarta, quinta e sexta sprints do programa de bolsas Compass UOL para formação em machine learning para AWS.

***

## Execução (Código Fonte)

Com base nas atividades anteriores realizadas, crie uma página html que irá capturar uma frase qualquer inserida pelo usuário e transformará essa frase em um audio em mp3 via polly.

**Especificações**:

A aplicação deverá ser desenvolvida com o framework 'serverless' e deverá seguir a estrutura que já foi desenvolvida neste repo.

Passo a passo para iniciar o projeto:

1. Crie um repositório para sua equipe;

2. Instale o framework serverless em seu computador. Mais informações [aqui](https://www.serverless.com/framework/docs/getting-started)

```json
npm install -g serverless
```

3. Gere suas credenciais (AWS Acess Key e AWS Secret) na console AWS pelo IAM. Mais informações [aqui](https://www.serverless.com/framework/docs/providers/aws/guide/credentials/)

4. Em seguida insira as credenciais e execute o comando conforme exemplo:

```json
serverless config credentials \
  --provider aws \
  --key AKIAIOSFODNN7EXAMPLE \
  --secret wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
  ```

Também é possivel configurar via [aws-cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) executando o comando:

```json
$ aws configure
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-east-1
Default output format [None]: ENTER
  ```

#### Observação

As credenciais devem ficar apenas localmente no seu ambiente. Nunca exponha as crendenciais no Readme ou qualquer outro ponto do codigo.

Após executar as instruções acima, o serverless estará pronto para ser utilizado e poderemos publicar a solução na AWS.

5. Para efetuar o deploy da solução na sua conta aws execute (acesse a pasta `api-tts`):

```
serverless deploy
```

Depois de efetuar o deploy, vocẽ terá um retorno parecido com isso:

```bash
Deploying api-tts to stage dev (us-east-1)

Service deployed to stack api-tts-dev (85s)

endpoints:
  GET - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/
  GET - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/v1
  GET - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/v2
functions:
  health: api-tts-dev-health (2.1 kB)
  v1Description: api-tts-dev-v1Description (2.1 kB)
  v2Description: api-tts-dev-v2Description (2.1 kB)
```

6. Abra o browser e confirme que a solução está funcionando colando os 3 endpoints que deixamos como exemplo:

### Rota 1 → Get /

1. Esta rota já está presente no projeto
2. O retorno rota é:

```json
  {
    "message": "Go Serverless v3.0! Your function executed successfully!",
    "input": { 
        ...(event)
      }
  }
```

3. Status code para sucesso da requisição será `200`

### Rota 2 → Get /v1

1. Esta rota já está presente no projeto
2. O retorno rota é:

```json
  {
    "message": "TTS api version 1."
  }
 
```

3. Status code para sucesso da requisição será `200`

### Rota 3 → Get /v2

1. Esta rota já está presente no projeto
2. O retorno rota é:

```json
  {
    "message": "TTS api version 2."
  }
 
```

***

Após conseguir rodar o projeto base o objetivo final será divida em duas partes:

## Atividade -> Parte 1

### Rota 4 -> Post /v1/tts

Deverá ser criada a rota `/v1/tts` que receberá um post no formato abaixo:

```json
  {
    "phrase": "converta esse texto para áudio"
  }
```

- Essa frase recebida deverá ser transformada em áudio via AWS Polly
- Deverá ser armazenada em um S3 (Que deverá ser público, apenas para a nossa avaliação)
- A resposta da chamada da API deverá constar o endereço do audio gerado no S3

Resposta a ser entregue:

```json
  {
    "received_phrase": "converta esse texto para áudio",
    "url_to_audio": "https://meu-buckect/audio-xyz.mp3",
    "created_audio": "02-02-2023 17:00:00"
  }
```

Dessa maneira essa será a arquitetura a ser implantada:

![post-v1-tts](./assets/post-v1-tts.png)

Exemplos de referência:

- <https://github.com/SC5/serverless-blog-to-podcast> (JS)
- <https://github.com/hussainanjar/polly-lambda> (Python)

## Atividade -> Parte 2

### Rota 5 -> Post /v2/tts

Deverá ser criada a rota `/v2/tts` que receberá um post no formato abaixo:

```json
  {
    "phrase": "converta esse texto para áudio e salve uma referencia no dynamoDB"
  }
```

- Deverá ser criada uma lógica para que essa frase recebida seja um id unico (um hash).
- Esse hash será o principal atributo em nosso dynamo db
Exemplo: "Teste 123" será sempre o id "123456"
- Com essa frase recebida deverá ser transformada em áudio via AWS Polly
- Deverá ser armazenada em um S3 (Que deverá ser público, apenas para a nossa avaliação)
- Deverá ser salva uma referencia no dynamoBD com as seguintes informações: id, frase e url do s3
- A resposta da chamada da API deverá constar o endereço do audio gerado no S3

Resposta a ser entregue:

```json
  {
    "received_phrase": "converta esse texto para áudio",
    "url_to_audio": "https://meu-buckect/audio-xyz.mp3",
    "created_audio": "02-02-2023 17:00:00",
    "unique_id": "123456"
    
  }
```

Dessa maneira essa será a arquitetura a ser implantada:

![post-v2-tts](./assets/post-v2-tts.png)

Exemplos de referência com inserção no dynamoDb:

- <https://github.com/serverless/examples/tree/v3/aws-python-http-api-with-dynamodb> (Python)

## Atividade -> Parte 3

### Rota 6 -> Post /v3/tts

Deverá ser criada a rota `/v3/tts` que receberá um post no formato abaixo:

```json
  {
    "phrase": "converta esse texto para áudio e salve uma referencia no dynamoDB. Caso a referencia já exista me devolva a URL com audio já gerado"
  }
```

- Deverá utilizar a lógica do hash para verificar se a frase já foi gerada anteriormente.
- Caso o hash já exista no dynamo entregue o retorno conforme abaixo.
- Caso não exista faça a geração do audio, grave no s3 e grave as referencias no dynamo conforme Parte 2

Resposta a ser entregue:

```json
  {
    "received_phrase": "converta esse texto para áudio",
    "url_to_audio": "https://meu-buckect/audio-xyz.mp3",
    "created_audio": "02-02-2023 17:00:00",
    "unique_id": "123456"
  }
```

Dessa maneira essa será a arquitetura a ser implantada:

![post-v3-tts](./assets/post-v3-tts.png)

***

## Observações retorno esperado

- os campos de entrada e saida deverão estar nos formatos e com os nomes apresentados.
- status code para sucesso da requisição será `200`
- status code para erros deverá ser `4XX` ou `5XX` (dica: o SDK retorna o tipo de erro)

***

## O que será avaliado?

- Projeto em produção na AWS
- Em python conforme projeto base disponibilizado
- Infra estrutura como codigo
- Seguir as atividades na ordem proposta
- Sobre as rotas:
  - Possuir em cada rota os retornos esperados (somente campos solicitados conforme especificação)
- Organização geral do código fonte
  - Estrutura de pastas
  - Estrutura da logica de negócio
  - Divisão de responsabilidades em arquivos/pastas distintos
  - Otimização do código fonte (evitar duplicações de código)
- Objetividade do README.md

***


## Entrega

- **O trabalho deve ser feito em grupos de três ou quatro pessoas**;
- Criar um repositório no Github;
  - Colocar os avaliadores como membros do repositório criado; 
- Subir o trabalho no repositório da equipe com um README.md:
  - documentar detalhes sobre como a avaliação foi desenvolvida;
  - dificuldades conhecidas;
  - como utilizar o sistema;
  - URL para acesso à página;
- 🔨 Disponibilizar o código fonte desenvolvido (Sugestão: pasta `src`).

- **O prazo de entrega do link do repositório no chat da weekly do dia 03/04/2024**.
