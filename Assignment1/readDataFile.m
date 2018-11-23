function shoppinglist = readDataFile

fid = fopen('groceries.txt');
shoppinglist = cell(0);
while ~feof(fid)
    line = fgetl(fid);
    shoppinglist{end+1} = strsplit(line(1:end-1),',');
end
fclose(fid);
shoppinglist = shoppinglist';
