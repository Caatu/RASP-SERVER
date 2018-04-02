# RASP-SERVER

## Descrição:
    Codigo responsavel por carregar informações (portas GPIO, nome, unidade de medida de um arquivo) e capturar/processar/enviar os dados de sensores conectados as portas GPIO enviando por meio do protocolo mqtt a um servidor especificado.

## Utilização:
### Requisitos:
    - Python 3
    - Pip

### Instalação:
```bash
# Recomenda-se utilizar virtualenv

# Dentro da pasta do projeto execute:
pip install -r requirements.txt 

# Crie uma copia do .env.example renomeando para .env
cp .env.example .env

# Configure o .env com seu usuario/senha
 ```

 ### Utilização:
```bash
# Dentro da pasta do projeto execute:
python main.py
 ```

 ### Padrão de Rotas do MQTT

 ## T