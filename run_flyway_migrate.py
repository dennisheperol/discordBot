import os

os.system('docker run --rm -v $PWD/flyway/sql:/flyway/sql -v $PWD/flyway/conf:/flyway/conf --network="host" flyway/flyway migrate')
