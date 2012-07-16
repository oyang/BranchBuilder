#!/bin/bash

echo "Get all from builds_status"
sqlite3 branchBuilder 'select * from builds_status'
echo '======================'
echo '======================'
echo "????Get all from builds"
sqlite3 branchBuilder 'select * from builds'
echo "????Get all status from builds"
sqlite3 branchBuilder 'select task_id, status from builds'

