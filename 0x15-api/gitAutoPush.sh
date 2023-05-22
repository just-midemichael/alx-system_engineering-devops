#!/bin/bash

echo "Enter Commit a message: "
read $message

git add .
git commit $message
git push
echo "Push Successful ✅"
