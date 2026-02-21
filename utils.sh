#!/bin/bash

rename_player() {
	OLD_NAME=$1
	NEW_NAME=$2
	
	# for gamefile in $(ls data/pgn/mgr/*.pgn);
	# do
	# 	echo "${gamefile} --> ${OLD_NAME} ::: ${NEW_NAME}"
		
	# done
	echo "${OLD_NAME} ::: ${NEW_NAME}"
	# grep -irnw "${OLD_NAME}" data/pgn/mgr/*.pgn # search player into my games
	# sed -i "s/${OLD_NAME}/${NEW_NAME}/g" data/pgn/mgr/*.pgn # replace old player to new player in my games
}

fix_movetext() {
	# Configurações
	# DIR="${1:-.}"
	DIR="data/pgn/mgr"
	MODO_FIX=false

	# Inicialização de contadores
	TOTAL=0
	CORRIGIDOS=0
	ERROS_TAG=0
	SAUDAVEIS=0

	# Verifica se o usuário quer corrigir os arquivos
	if [[ "$2" == "--fix" ]]; then
		MODO_FIX=true
		# DIR="${2:-.}"
	fi

	echo "------------------------------------------"
	echo "🔍 Processando diretório: $DIR"
	[[ "$MODO_FIX" == true ]] && echo "⚠️  MODO DE CORREÇÃO ATIVADO"
	echo "------------------------------------------"

	# for arquivo in "$DIR"/*.pgn; do
	for arquivo in "$DIR"/2025-0[1-1]*.pgn; do
		[ -e "$arquivo" ] || continue
		((TOTAL++))

		# 1. Extrai o valor da tag Result
		RESULT_TAG=$(grep -oP '^\[Result "\K[^"]+' "$arquivo")
		
		if [ -z "$RESULT_TAG" ]; then
			echo "❌ Ignorado: $(basename "$arquivo") (Tag Result ausente)"
			((ERROS_TAG++))
			continue
		fi

		# 2. Captura o último token do conteúdo (ignora linhas vazias)
		RESULT_MOVETEXT=$(grep -v '^$' "$arquivo" | tail -n 1 | awk '{print $NF}')

		# 3. Verifica se o arquivo termina com exatamente uma linha vazia
		# Comparamos o número de bytes do arquivo com a posição do último caractere não-vazio
		ULTIMA_LINHA_OK=false
		if [ "$(tail -c 1 "$arquivo" | wc -l)" -eq 1 ] && [ "$(tail -c 2 "$arquivo" | head -c 1 | tr -d '\n' | wc -c)" -eq 1 ]; then
			ULTIMA_LINHA_OK=true
		fi

		# Lógica de Validação e Decisão
		if [ "$RESULT_TAG" != "$RESULT_MOVETEXT" ] || [ "$ULTIMA_LINHA_OK" = false ]; then
			
			if [ "$MODO_FIX" = true ]; then
				# A) Remove todas as linhas em branco do final
				sed -i -e :a -e '/^\n*$/{$d;N;ba' -e '}' "$arquivo"
				
				# B) Corrige o resultado se divergir
				if [ "$RESULT_TAG" != "$RESULT_MOVETEXT" ]; then
					sed -i "$ s/$RESULT_MOVETEXT$/$RESULT_TAG/" "$arquivo"
				fi

				# C) Adiciona a linha em branco regulamentar (padrão PGN)
				echo "" >> "$arquivo"
				
				((CORRIGIDOS++))
				echo "✅ Corrigido: $(basename "$arquivo")"
			else
				echo "⚠️  Divergência: $(basename "$arquivo")"
				[ "$RESULT_TAG" != "$RESULT_MOVETEXT" ] && echo "   - Esperado: $RESULT_TAG | Encontrado: $RESULT_MOVETEXT"
				[ "$ULTIMA_LINHA_OK" = false ] && echo "   - Erro de formatação (final do arquivo)"
			fi
		else
			((SAUDAVEIS++))
		fi
	done

	# Resumo Final
	echo "------------------------------------------"
	echo "📊 RESUMO DA EXECUÇÃO:"
	echo "   Total de arquivos analisados: $TOTAL"
	echo "   Arquivos saudáveis:           $SAUDAVEIS"
	[[ "$MODO_FIX" == true ]] && echo "   Arquivos corrigidos:          $CORRIGIDOS"
	[[ "$MODO_FIX" == false ]] && echo "   Arquivos com problemas:       $((TOTAL - SAUDAVEIS - ERROS_TAG))"
	echo "   Arquivos sem tag [Result]:    $ERROS_TAG"
	echo "------------------------------------------"
}

case $1 in
    "rename_player")
        clear
		date
        rename_player "$2" "$3"
        ;;
	"fix_movetext")
		clear
		date
		fix_movetext "$2" "$3"
		;;
	*)
        # TODO better usage message
        echo "Function not found! $1"
esac
