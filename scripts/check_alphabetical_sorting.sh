# Returns a non-zero exit code if the data sites are not alphabetically sorted.

grep 'domain:' _data/sites.yml | grep -v '512kb.club' | tr '[:upper:]' '[:lower:]' | sort -c
