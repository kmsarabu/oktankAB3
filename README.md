## Production Link
http://k-octank.shop/

# 1. EC2 Launch Template
## user data
```
#!/bin/bash 
sudo yum update -y
sudo yum install git -y
sudo yum install -y python3
git clone https://github.com/cjk0604/k-octank-fashion.git
cd k-octank-fashion
sudo pip3 install -r requirements.txt
export DATABASE_HOST="rds-apg.cluster-ct3fprli4uqj.us-east-1.rds.amazonaws.com"
export DATABASE_USER="oktadmin"
export DATABASE_PASSWORD=''
export DATABASE_DB_NAME="oktank"
export DATABASE_PORT=5432
python3 app.py
```

# 2. Load Tests
## apache benchmark
```
ab -n 100000 http://k-octank.shop/
ab -c 300 -n 500 -t 300 http://k-octank.shop/products/fashion/
```

# 3. Latency
## Cloudfront
```
curl -s -w '\nLookup Time:\t%{time_namelookup}\nConnect time:\t%{time_connect}\nPreXfer time:\t%{time_pretransfer}\nStartXfer time:\t%{time_starttransfer}\n\nTotal time:\t%{time_total}\n' -o /dev/null http://k-octank-vpc-alb-2-1616693628.us-east-1.elb.amazonaws.com/products/fashion?page=1/
```
- ALB (DNS)

## Cloudfront
```
curl -s -w '\nLookup Time:\t%{time_namelookup}\nConnect time:\t%{time_connect}\nPreXfer time:\t%{time_pretransfer}\nStartXfer time:\t%{time_starttransfer}\n\nTotal time:\t%{time_total}\n' -o /dev/null http://k-octank.shop/products/fashion?page=1/

curl -s -w '\nTotal Time:\t%{time_total}\n' -o /dev/null http://k-octank.shop/ 

```
- dynamic hosting

# 4. Bastion Host Connect
## Bastion at the Host Private Subnet EC2 (How to Connect)
1. Bastion (Connect to the host)
```
ssh -i "koctank.pem" -N -L 33321:10.10.11.200:22 ec2-user@3.81.174.50 
```

2. Open a new terminal and copy the code below
```
ssh -i koctank.pem -p 33321 ec2-user@localhost 
```

3. RDS/Aurora PostgreSQL DB Connect
```
mysql -h koctankdbcluster.cmctwgljftes.us-east-1.rds.amazonaws.com -P 3306 -u admin -p
```

table
```
show tables;
```

query something from tables
```
select name, price from fashion limit 10;
```

참고: https://boomkim.github.io/2019/12/20/bastion-host-port-forwarding/

# 5. 로그 분석 및 시각화
## Athena에서 CloudFront_access log S3 연결
```
Create database octank
```

table 만들기
```
CREATE EXTERNAL TABLE IF NOT EXISTS octank.cloudfront_logs (
  `date` DATE,
  time STRING,
  location STRING,
  bytes BIGINT,
  request_ip STRING,
  method STRING,
  host STRING,
  uri STRING,
  status INT,
  referrer STRING,
  user_agent STRING,
  query_string STRING,
  cookie STRING,
  result_type STRING,
  request_id STRING,
  host_header STRING,
  request_protocol STRING,
  request_bytes BIGINT,
  time_taken FLOAT,
  xforwarded_for STRING,
  ssl_protocol STRING,
  ssl_cipher STRING,
  response_result_type STRING,
  http_version STRING,
  fle_status STRING,
  fle_encrypted_fields INT,
  c_port INT,
  time_to_first_byte FLOAT,
  x_edge_detailed_result_type STRING,
  sc_content_type STRING,
  sc_content_len BIGINT,
  sc_range_start BIGINT,
  sc_range_end BIGINT
)
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY '\t'
LOCATION 's3://octank-cloudfront-standard-log/'
TBLPROPERTIES ( 'skip.header.line.count'='2' )
```

## Test Query
```
SELECT DISTINCT * 
FROM cloudfront_logs 
LIMIT 10;
```

# 5.1 Quicksight 연결 및 대시보드 생성
## 인기 페이지 대시보그 생성
## QuickSight Embed
https://learnquicksight.workshop.aws/en/anonymous-embedding.html

# Appendix
## PostgreSQL.db -> RDS PostgreSQL, Import Data
psql -h <host> -p <port> -U <user> -d <dbname> < dump_pg.sql > dump.out 2>&1

For MySQL:
  sudo mysql -h koctankdbcluster.cmctwgljftes.us-east-1.rds.amazonaws.com -u admin -P 3306 -p koctank < dump.sql
