request_secrets() {
    #!/bin/sh

    lumos request --app "8156588a-2c42-2785-a437-f6aebc7a6197" --permission-like $1 --length 14400 --reason $2 --for-me --wait
    echo "Waiting for role to be created..."
    sleep 25
    secrets $1
}

secrets() {
    #!/bin/sh
    username=$(lumos whoami --username | awk -F '@' '{print $1}')
    
    arn=""
    # check if arn is empty
    while [ "" = "$arn" ]; do
        query=$(aws iam list-roles --query "Roles[?contains(Arn, '$username-$1')]")
        if [ "[]" = "$query" ]; then
            echo "Still waiting for role to be created..."
            sleep 10
            continue
        fi

        arn=$(echo $query | grep -o '"Arn": *"[^"]*"' | cut -d'"' -f4)
        roleName=$(echo $query | grep -o '"RoleName": *"[^"]*"' | cut -d'"' -f4)
    done
    
    echo -e "\e[1A\e[KGot role: $roleName"
    
    original_dir=$(pwd)

    echo Updating AWS config
    cd ~/.aws
    echo "\n\n[profile $roleName]" >> config
    echo "sso_start_url = https://d-92675d34df.awsapps.com/start#" >> config
    echo "sso_region = us-west-2" >> config
    echo "sso_account_name = lumos" >> config
    echo "sso_account_id = 134185523792" >> config
    echo "sso_role_name = $roleName" >> config
    echo "region = us-west-2" >> config
    echo "output = json" >> config

    secret=$(aws secretsmanager list-secrets --query "SecretList[?Name == '/prod/$1']")
    secret_name=$(echo $secret | grep -o '"Name": *"[^"]*"' | cut -d'"' -f4)

    secret_value=$(aws secretsmanager get-secret-value --secret-id $secret_name --query SecretString --output text)

    echo -e '\e[1A\e[KRestoring AWS config'
    total_lines=$(wc -l < config)
    lines_to_keep=$((total_lines - 10))
    head -n "$lines_to_keep" config > temp.txt
    mv temp.txt config

    secret_file_name="${secret_name//\//_}"
    secret_file_name="${secret_file_name//\\/}"
    secret_file_name="${secret_file_name//./_}.txt"

    cd $original_dir
    echo $secret_value >> "./$secret_file_name"
    secret_header="************** $secret_name **************"
    echo -e "\e[1A\e[K$secret_header"
    echo "${secret_value:0:10}... saved to $secret_file_name"

    for (( i=0; i<${#secret_header}; i++ )); do
        echo -n "*"
    done
    echo
}
