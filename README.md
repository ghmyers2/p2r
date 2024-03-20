## Production Timeline

### <u> __production_main.py__ - Runs Production communications </u>

<ins>Daily Functions:</ins>
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

<ins>Wednesday Functions:</ins>
* __remail.run()__ - Remail.remail_main
   * Runs the Funding Forms/Guides
 
<ins>Thursday Functions:</ins>
* __u1c.run()__ - AgeIn_U1C.main
   * U1C Mailing
* __u1c_ifp.run_ifp_u1c()__ - AgeIn_U1C.ifp_u1c_main
   * IFP U1C

<ins>Friday Functions:</ins>
* __non_adequate.run()__ - not_adequate.main
   * Not Adequate mailing

<ins>First of Month Functions:</ins>
* __abds.run()__ - AgeIn_b_day_suite.age_in_b_day_main
   * Age_in B-day comms monthly mailers includes Opers
* __mf.run()__ - monthly_fsid.send_monthly_fsid
   * Monthly production FSIDs
* __sprt.run_sprint_mo()__ - sprint_share.main
   * Sprint Share monthly mailer

<ins>First Through Tenth Functions:</ins>
* __atmr.run()__ - ACH_transition_email.ach_transition_monthly_run
   * Check for ACH and run beginning of the month

<ins>Fifteenth Functions:</ins>
* __abds.run()__ - AgeIn_b_day_suite.age_in_b_day_main
   * Age_in B-day comms monthly mailers includes Opers
* __sup.run_supplemental()__ - supplemental.main 
   * Supplemental
* __lcm.run()__ - AgeIn_b_day_suite.last_chance_main
   * Last Chance email and print -- being replaced by 1_month, being run in abds.run()
* __cfr.post_approved_records_to_vendor()__ - client_funding_requests.main
   * FG Sample requests

<ins>Twentieth Functions:</ins>
* __wm.run()__ - welcome_communication.welcome_main
   * Welcome communications

<ins>Twentyfifth Functions:</ins>
* __cert.run_certified_letters()__ - certified_letters.main
   * Monthly Certified letters

### __maintenance_main.py__ - Cleans up and deletes files from production

<ins>Daily Functions:</ins>
* __dc.move_file_older_x(log_dir, log_archive, 5)__ - 
  * Clean up log dir
* __dc.delete_file_older_x(log_dir + 'archive/', 90)__ - 
  * Delete log files
* __dc.delete_file_older_x(config.shared_directory['data_file_pickup'] + 'Processed/', 30)__ - 
  * Delete archived log files
* __sort_ss.sort_ss_rows(sheet_name_or_id='5704624016516996', col_name='Target_DropDate')__ - 
  * Sort Smartsht
* __ss_backup.backup_smartsheet()__ -
  * Back up smartsheet
* __rsp.delete_pdf_proofs()__ - client_funding_requests.main 
  * Remove pdf proofs from sftp

<ins>Friday Functions:</ins>
* __sql_update.add_person_id_to_json()__ - 
   * pulling person id from pdf name in U1C file
* __sql_update.update_floats_in_personid_cid()__ - 
   * float fix in db
* __sll.generate_logo_sample_xml()__ - 
   * Smartcom logo xml process

<ins>Fifteenth Functions:</ins>
* __cu.run()__ - 
   * Clean up Small in house Smartsheet


