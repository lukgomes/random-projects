#!/bin/bash
#
###############################################################################
# Ferramenta: gera_sha.sh
#
# Objetivo da ferramenta
# Gerar hashes de senha no formato {SHA}<hash_base64>, utilizando o algoritmo
# SHA-1 codificado em Base64. O formato gerado é compatível com diversos
# sistemas de autenticação que armazenam credenciais utilizando o padrão
# {SHA}, como algumas implementações LDAP.
#
# Requisitos de execução
# - Sistema operacional Linux ou Unix compatível.
# - Interpretador Bash.
# - OpenSSL instalado e acessível no PATH do sistema.
# - Utilitário Base64 instalado e acessível no PATH do sistema.
#
# Forma de utilização
# 1. Execute o script:
#      ./gera_sha.sh
# 2. Digite a senha quando solicitado.
# 3. Confirme a senha quando solicitado.
# 4. Se as senhas forem iguais, o hash será gerado e exibido no terminal.
#
# Exemplos de uso
#
# Exemplo de execução:
#
#   $ ./gera_sha.sh
#   Digite a senha:
#   Retype a senha:
#   {SHA}W6ph5Mm5Pz8GgiULbPgzG37mj9g=
#
# Exemplo de utilização do resultado:
#
#   userPassword: {SHA}W6ph5Mm5Pz8GgiULbPgzG37mj9g=
#
###############################################################################

echo "Gera senha hash sha1 para o openldap"

# Solicita a senha sem exibir no terminal
read -s -p "Digite a senha: " senha
echo

# Solicita confirmacao
read -s -p "Redigite a senha: " confirma
echo

# Verifica se as senhas são iguais
if [ "$senha" != "$confirma" ]; then
	echo "Erro: As senhas não conferem."
	exit 1
fi

# Gera hash SHA1 em Base64 no formato {SHA}
hash=$(printf "%s" "$senha" | openssl dgst -sha1 -binary | base64)

# Exibe o resultado
echo "{SHA}$hash"

