#!/bin/bash
###########################################################
# If you own this source, feel free for change this file  #
#                      AiBox labs                         #
###########################################################

E_OK=0
CHANGELOG="changelog.md"

TAG="Non released"
DATE="TODAY"
declare -a FEATURES
declare -a FIXES
declare -a CHANGES

function print_help() {
	echo -e "\x1b[33m"
	echo "$0 [--help] [--logname=logfilename]"
	echo "--help				show this message and exit"
	echo "--logname=logfilename		explicitly set the log filename"
	echo -e "\x1b[36m"
	echo "commit message format:"
	echo "[feature]|[fix]|[changelog] actual_commit_message"
	echo "[feature] stands for new major features introduced by the commit"
	echo "[fix] for major buxfixes made by commit"
	echo "[changelog] else additional helpfull information for changelog"
	echo -e "\x1b[0m"
	exit "$E_OK"
}

function parse_args() {
	while [[ "$1" != "" ]]
	do
		IFS="=" read -ra ARG <<< "$1"
		PARAM="${ARG[0]}"
		VALUE="${ARG[1]}"
		case $PARAM in
    		--help)
						print_help
							;;
				--logname)
						CHANGELOG="$VALUE"
							;;
		esac
		shift
	done
}

function log_release(){
	#echo formated arrays to stdout
	echo "# $TAG ($DATE)"
	echo '```'
	echo `git for-each-ref refs/tags/$TAG --format='%(contents)'`
	echo '```'
	if [[ ${!FEATURES[@]} ]]; then
		echo -e "\n***new features***"
		for FEAT in "${FEATURES[@]}"; do echo "$FEAT"; done
	fi
	if [[ ${!FIXES[@]} ]]; then
		echo -e "\n***bug fixes***"
		for BUG in "${FIXES[@]}"; do echo "$BUG"; done
	fi
	if [[ ${!CHANGES[@]} ]]; then
		echo -e "\n***minor changes***"
		for CHANGE in "${CHANGES[@]}"; do echo "$CHANGE"; done
	fi
}

function parse_git_log(){
	while read LINE
	do
		IFS="|" read -ra COMMIT <<< $LINE
		MESSAGE=${COMMIT[0]}
		REFLOG=${COMMIT[1]}
		DATE=${COMMIT[2]}
		if [[ "$REFLOG" =~ .*"tag:".* ]]; then
			#new tag encountered. log previous artefacts if any.
			log_release
			#clear artefacts.
			unset FEATURES
			unset FIXES
			unset CHANGES
			#set new tag name.
			TAG=`echo $REFLOG | sed -re 's/.*tag: ([v0-9.]*).*/\1/'`
		fi
		#parse commit message, as it can any of
		#[fix], [feats], [changelog] in single message.
		IFS="[" read -ra SUBS <<< $MESSAGE
		for SUB in "${SUBS[@]}"; do
			if [[ "$SUB" =~ "changelog]".* ]]; then
				#it contains changelog] preffix
				SUB=${SUB#"changelog]"}
				CHANGES+=("- [x]$SUB")
			elif [[ "$SUB" =~ "feature]".* ]]; then
				#it contains feature] preffix
				SUB=${SUB#"feature]"}
				FEATURES+=("- [x]$SUB")
				#it contains fix] preffix
			elif [[ "$SUB" =~ "fix]".* ]]; then
				SUB=${SUB#"fix]"}
				FIXES+=("- [x]$SUB")
			fi
		done
	done <<< `git log --date=format:'%Y.%m.%d' --pretty=format:'%s | %D | %ad'`
	#log final tag artefacts, as there no more strings.
	log_release
}

parse_args $@
parse_git_log > $CHANGELOG
exit "$E_OK"
