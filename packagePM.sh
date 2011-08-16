#! /bin/bash
cd passwordMgmt
rm -r  .project .settings .pydevproject
find . -name "*.pyc" | xargs rm -r
find . -name ".svn" | xargs rm -r
find . -name "*.sql" | xargs rm -r
cd ..
tar -czf pm1.0.0.tar.gz passwordMgmt


