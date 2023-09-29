CNAME=$CONTAINER_NAME
if [ "$(docker ps -qa -f name=$CNAME)" ]; then
    echo ":: Found container - $CNAME"
    if [ "$(docker ps -q -f name=$CNAME)" ]; then
        echo ":: Stopping running container - $CNAME"
        docker stop $CNAME;
    fi
    echo ":: Removing stopped container - $CNAME"
    docker rm $CNAME;
fi
