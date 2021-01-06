yarn install

for file in ./src/*.mmd
do
    if [[ -f $file ]]; then
        f="$(basename $file)"
        yarn run mmdc -c config/mermaid-config.json -i $file -o ./output/${f/mmd/png}
    fi
done