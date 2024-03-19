secrets() {
    username=$(lumos whoami --username | awk -F '@' '{print $1}')
    lumos request --app 8156588a-2c42-2785-a437-f6aebc7a6197 --permission-like $1 --length 7200 --reason $2 --for-me --wait
    sleep 25
    arn=""
    while $arn == "" ; do
        sleep 5
        query=$(aws iam list-roles --query "Roles[?contains(Arn, '$username-$1')]")
        arn=$(echo $query | grep -o '"Arn": *"[^"]*"' | cut -d'"' -f4)
        roleName=$(echo $query | grep -o '"RoleName": *"[^"]*"' | cut -d'"' -f4)
    done
}
