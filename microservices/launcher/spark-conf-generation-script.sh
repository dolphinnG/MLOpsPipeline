#!/bin/bash

# Get the POD_ID environment variable
POD_ID=${POD_ID}

# Generate the dolphin-spark.conf file
cat <<EOL > ./dolphin-spark.conf
# spark-defaults.conf
spark.master                     spark://spark-master-svc:7077
spark.executor.cores             1
spark.driver.host                ${POD_ID}
spark.driver.port                7078
spark.driver.bindAddress         0.0.0.0


EOL

# spark.hadoop.fs.s3a.access.key   minio_user
# spark.hadoop.fs.s3a.secret.key   minio_password
# spark.hadoop.fs.s3a.endpoint      http://minio:9900
# spark.hadoop.fs.s3a.impl          org.apache.hadoop.fs.s3a.S3AFileSystem
# spark.hadoop.fs.s3a.path.style.access true