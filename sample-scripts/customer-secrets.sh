# Using this script
# Run `source customer-secrets.sh` to load the functions

# Run `request_secrets SITENAME REASON` to request secrets
# i.e. `request_secrets lumostester.com "Testing CLI"`
request_secrets() {
    #!/bin/sh

    lumos request --app "8156588a-2c42-2785-a437-f6aebc7a6197" --permission-like $1 --length 14400 --reason $2 --for-me --wait
    echo "Waiting for role to be created..."
    sleep 25
    secrets $(lumos request status --last --id-only)
}

# Run `secrets REQUEST_ID` to get the secrets requested in request ID REQUEST_ID
# i.e. `secrets 8156588a-2c42-2785-a437-f6aebc7a6197`
secrets() {
    #!/bin/sh
    request_id=$1
    if ( [ -z "$request_id" ] ); then
        echo "Request ID: "
        read request_id
    fi

    request_status=$(lumos request status --request-id $request_id --status-only)

    if ( [ "COMPLETED" != "$request_status" ] ); then
        echo "Request not completed. Exiting..."
        return
    fi

    username=$(lumos whoami --username | awk -F '@' '{print $1}')

    permissions_list=$(lumos request status --request-id $request_id --permission-only)
    permissions=("${(@s/; /)permissions_list}")

    for permission in "${permissions[@]}"; do
        secret $username $permission
    done
}

# Run `secret USERNAME SITENAME` to get the secret for USERNAME and SITENAME
# i.e. `secrets niamh lumostester.com`
secret() {

    #!/bin/sh
    username=$1
    permission=$2

    echo "Working on permission [$permission]"
    
    arn=""
    # check if arn is empty
    while [ "" = "$arn" ]; do
        query=$(aws iam list-roles --query "Roles[?contains(Arn, '$username-$permission')]")
        if [ "[]" = "$query" ]; then
            echo "Still waiting for role to be created..."
            sleep 10
            continue
        fi

        arn=$(echo $query | grep -o '"Arn": *"[^"]*"' | cut -d'"' -f4)
        roleName=$(echo $query | grep -o '"RoleName": *"[^"]*"' | cut -d'"' -f4)
        roleName=$(echo ${roleName//AWSReservedSSO_/} | sed 's/_.*//')
    done
    
    echo -e "Got role: $roleName"
    
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

    secret=$(aws secretsmanager list-secrets --profile "$roleName" --query "SecretList[?Name == '/prod/$permission']")
    secret_name=$(echo $secret | grep -o '"Name": *"[^"]*"' | cut -d'"' -f4)

    secret_value=$(aws secretsmanager get-secret-value --secret-id $secret_name --query SecretString --output text --profile "$roleName")

    echo -e '\e[1A\e[KRestoring AWS config'
    total_lines=$(wc -l < config)
    lines_to_keep=$((total_lines - 10))
    head -n "$lines_to_keep" config > temp.txt
    mv temp.txt config

    if [ -z "$secret_value" ]; then
        echo "Secret not found. Exiting..."
        return
    fi

    secret_file_name="${secret_name//\//_}"
    secret_file_name="${secret_file_name//\\/}"
    secret_file_name="${secret_file_name//./_}.json"

    cd $original_dir
    rm -f $secret_file_name
    echo $secret_value >> "./$secret_file_name"
    secret_header="************** $secret_name **************"
    echo $secret_header
    echo "${secret_value:0:10}... saved to $secret_file_name"

    for (( i=0; i<${#secret_header}; i++ )); do
        echo -n "*"
    done
    echo

}
