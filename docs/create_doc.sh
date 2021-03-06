# generate doc
echo 'create documentation'
python3 -m pdoc --html -o . --template-dir ./config --force ../prettypyplot

mv prettypyplot/cmaps/* ./cmaps/
rmdir prettypyplot/cmaps

mv prettypyplot/* .
rmdir prettypyplot

# replace MPL_DOC with link
sed -i -e 's/MPL_DOC/https:\/\/matplotlib.org\/api\/_as_gen\/matplotlib/g' *.html
echo ''

# generate figures in gallery
cd ../
echo 'recreate gallery figures:'
for file in $(find ./gallery/ -name '*.py')
do
    echo '   exec: '$file
    python3 $file
done

cd docs
