sudo docker run \
	-e DATABASE_HOST="rds-apg.cluster-ct3fprli4uqj.us-east-1.rds.amazonaws.com" \
	-e DATABASE_USER="oktadmin" \
	-e DATABASE_PASSWORD='kr!shna' \
	-e DATABASE_DB_NAME="oktank" \
	-e DATABASE_PORT=5432 \
	-p 8443:8443 \
	octankretail:1.0
