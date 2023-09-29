#!/bin/bash
while getopts r:t:s: flag
do
    case "${flag}" in
        r) github_repo_link=${OPTARG};;
        t) token=${OPTARG};;
        s) run_as_service=${OPTARG};;
    esac

done 

if [ -d actions-runner ]
then
    if [ -f actions-runner/run.sh ]
    then 
        echo "running action-runner, already exist"
        cd actions-runner
        ./config.sh --url $github_repo_link --token $token

    else
        cd actions-runner
        echo "changing directory to actions-runner"
        curl -o actions-runner-linux-x64-2.309.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.309.0/actions-runner-linux-x64-2.309.0.tar.gz
        echo "2974243bab2a282349ac833475d241d5273605d3628f0685bd07fb5530f9bb1a  actions-runner-linux-x64-2.309.0.tar.gz" | shasum -a 256 -c
        tar xzf ./actions-runner-linux-x64-2.309.0.tar.gz
        ./config.sh --url $github_repo_link --token $token

        echo "successfully configured"

    fi

else
    echo "making new dir"
    mkdir actions-runner && cd actions-runner
    echo "created action-runner and cd to actions-runner"
    curl -o actions-runner-linux-x64-2.309.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.309.0/actions-runner-linux-x64-2.309.0.tar.gz
    echo "2974243bab2a282349ac833475d241d5273605d3628f0685bd07fb5530f9bb1a  actions-runner-linux-x64-2.309.0.tar.gz" | shasum -a 256 -c
    tar xzf ./actions-runner-linux-x64-2.309.0.tar.gz
    ./config.sh --url $github_repo_link --token $token

fi

if [ $run_as_service == 'yes' ]
then
    echo "starting svc"
	sudo bash svc.sh install
    sudo bash svc.sh start
else
	bash run.sh
fi

