## Production Link


# 1. EC2 Launch Template
## user data
```
#!/bin/bash 
sudo yum update -y
sudo yum install git -y
sudo yum install -y python3
git clone https://github.com/kmsarabu/oktankAB3.git
cd oktankAB3
sudo pip3 install -r requirements.txt
export DATABASE_HOST="xyz.rds.amazonaws.com"
export DATABASE_USER="oktadmin"
export DATABASE_PASSWORD='xyz'
export DATABASE_DB_NAME="oktank"
export DATABASE_PORT=5432
python3 app.py
```

# 2. Load Tests
## apache benchmark
```
ab -n 100000 <url>
ab -c 300 -n 500 -t 300 <url>/products/fashion/
```

# 3. Latency
## Cloudfront
```
curl -s -w '\nLookup Time:\t%{time_namelookup}\nConnect time:\t%{time_connect}\nPreXfer time:\t%{time_pretransfer}\nStartXfer time:\t%{time_starttransfer}\n\nTotal time:\t%{time_total}\n' -o /dev/null http://<elb-url>.elb.amazonaws.com/products/fashion?page=1/
```

- ALB (DNS)

## Cloudfront
```
curl -s -w '\nLookup Time:\t%{time_namelookup}\nConnect time:\t%{time_connect}\nPreXfer time:\t%{time_pretransfer}\nStartXfer time:\t%{time_starttransfer}\n\nTotal time:\t%{time_total}\n' -o /dev/null http://<url>/products/fashion?page=1/

curl -s -w '\nTotal Time:\t%{time_total}\n' -o /dev/null http://<url>/ 

```


# Appendix

## PostgreSQL/RDS PostgreSQL/Aurora PostgreSQL -> Import Data
```
psql -h <host> -p <port> -U <user> -d <dbname> < pgdata/oktank_pgdata.sql > dump.out 2>&1
```

## Docker Build
```
sudo docker build -t octankretail:1.0 .
```

## Docker Run
```
sudo docker run \
	-e DATABASE_HOST="xyz.us-east-1.rds.amazonaws.com" \	# Database Host
	-e DATABASE_USER="oktadmin" \				# User Name
	-e DATABASE_PASSWORD='xyz' \				# User Password
	-e DATABASE_DB_NAME="oktank" \				# Database Name
	-e DATABASE_PORT=5432 \					# Database Port
        -e ECHOST="host:port,host:port" \ 			# ElastiCache
	octankretail:1.0
```
