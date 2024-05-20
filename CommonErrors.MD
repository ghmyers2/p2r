# Common Errors

## Bad Character Encoding Error

<ins>Error Message:</ins>
'charmap' codec can't decode byte 0x81 in position 41445

<ins>Usual Cause of Error in Code:</ins>
When files contain 'bad characters' (e.g. Estée Lauder or Nestlé), these characters are saved within a data file with a certain encoding. The data file is opened within the automation, potentially with the following code snipits:

df = pd.read_csv(original_txt, delimiter=delimiter)

or

with open(path_file, 'r') as objfile:

<ins>Useful Code for Fix:</ins>
The __return_file_encoding()__ function in the __repo.file_encode_detect__ file returns the encoding of a given file. To fix the encoding error, we pass the encoding of the given file into the above code as:

original_encod = encod.return_file_encoding(original_txt)

df = pd.read_csv(original_txt, delimiter=delimiter, encoding=original_encod)

or

with open(path_file, 'r', encoding=current_encod) as objfile:

## Timeout Error
