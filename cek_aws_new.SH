# !/bin/bash
# Created by : ./LazyBoy - JavaGhost Team

for aws_cred in $(cat $1); do
 	sed -i "2c aws_access_key_id = $(echo $aws_cred | cut -d "|" -f1)" ~/.aws/credentials
    sed -i "3c aws_secret_access_key = $(echo $aws_cred | cut -d "|" -f2)" ~/.aws/credentials
    sed -i "2c region = $(echo $aws_cred | cut -d "|" -f3)" ~/.aws/config

    if [[ $(/C/Python27/Scripts/./aws sesv2 get-account 2> >(grep -o "Max24HourSend")) =~ "Max24HourSend" ]]; then
    	GET_EnforcementStatus=$(/C/Python27/Scripts/./aws sesv2 get-account | grep -oP '"EnforcementStatus": "\K[^"]+')
    	GET_ProductionAccessEnabled=$(/C/Python27/Scripts/./aws sesv2 get-account | grep -oP '"ProductionAccessEnabled": \K[^,]+')
    	GET_Max24HourSend=$(/C/Python27/Scripts/./aws sesv2 get-account | grep -oP '"Max24HourSend": \K[^,]+')

        if [[ $GET_EnforcementStatus =~ "SHUTDOWN" ]]; then
            echo -e "[ GOOD ] - ${aws_cred}"
            echo -e "* INFO : - STATUS            : ${GET_EnforcementStatus}\n         - PRODUCTION ACCESS : ${GET_ProductionAccessEnabled}\n         - LIMIT             : ${GET_Max24HourSend}\n         - SKIPPED FOR SAVE"
        else
            echo -e "[ GOOD ] - ${aws_cred}"
            echo -e "* INFO : - STATUS            : ${GET_EnforcementStatus}\n         - PRODUCTION ACCESS : ${GET_ProductionAccessEnabled}\n         - LIMIT             : ${GET_Max24HourSend}"
            echo "${aws_cred} - STATUS : ${GET_EnforcementStatus} - PRODUCTION ACCESS : ${GET_ProductionAccessEnabled} - LIMIT : ${GET_Max24HourSend}" >> aws_good.txt
        fi
    else
    	echo "[ BAD ] - ${aws_cred}"
    fi
done