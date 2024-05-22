# Common Errors

## Bad Character Encoding Error

<ins>Error Message:</ins>
'charmap' codec can't decode byte 0x81 in position 41445

<ins>Usual Cause of Error in Code:</ins>
When files contain 'bad characters' (e.g. Estée Lauder or Nestlé), these characters are saved within a data file with a certain encoding. The data file is opened within the automation, potentially with the following code snipits:

`
df = pd.read_csv(original_txt, delimiter=delimiter)
`

or

`
with open(path_file, 'r') as objfile:
`

<ins>Useful Code for Fix:</ins>
The __return_file_encoding()__ function in the __repo.file_encode_detect__ file returns the encoding of a given file. To fix the encoding error, we pass the encoding of the given file into the above code as:

`
original_encod = encod.return_file_encoding(original_txt)
`

`
df = pd.read_csv(original_txt, delimiter=delimiter, encoding=original_encod)
`

or

`
current_encod = encod.return_file_encoding(path_file)
`

`
with open(path_file, 'r', encoding=current_encod) as objfile:
`
## NULL/Null/None Name

<ins>Error Message:</ins>

Possible Error in Automation (when the last name was None):



Possible Error in SmartComms (when the last name was None):

Error: [4078] An error occurred while evaluating the expression 'CurrentParticipant.lastNameFormatted': com.thunderhead.core.exception.LocalisableException: [27032] Error in derived property 'Participant.lastNameFormatted': java.lang.StringIndexOutOfBoundsException: begin 0, end 1, length 0

<ins>Usual Cause of Error in Code:</ins>
When data files which contain names like 'Null' or 'None' are read into automation as a dataFrame, Pandas typically converts the names to the None object in Python (not the strings 'Null' or 'None'). Empty values can cause errors when uploaded to Smartcomms, for instance, as shown above.

<ins>Useful Code for Fix:</ins>
After the data has been read into a dataframe, the none values can be converted to the string of "None" with the following code:

`
column_to_update = 'lastName'
`

`
df[column_to_update] = df[column_to_update].apply(lambda x: "None" if x is None else x)
`
