# Common Errors

## Bad Character Encoding

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

* __forms.pull_records_from_db()__ - funding.welcome_pkts_forms
  * Runs the Funding Forms/Guides
* __scl.run_selection_con_letter()__ - selection_confirmation_letter.selection_confirmation
  * Selection Confirmation letters
* __lof.run_loss_funding()__ - loss_of_funding.main
  * Loss of Funding
* __mav_main.mav_auto_begin()__ - mav.mav_main
  * Mav campaigns
* __cfr.collect_smartsheet_requests()__ - client_funding_requests.main
  * Requested Client Funding Guides
* __cfr.in_prod_requests()__ - client_funding_requests.main 
  * Process the zip file from SUN for Client Funding Guides
* __daily_mc_update.run()__ - email_campaigns.daily_mc_update

