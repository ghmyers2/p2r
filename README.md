# Alfred Schedule

## <u> __production_main.py__ - Runs Production communications </u>

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

## __maintenance_main.py__ - Cleans up and deletes files from production

<ins>Daily Functions:</ins>
* __dc.move_file_older_x(log_dir, log_archive, 5)__ - repo.directory_clean_up
  * Clean up log dir
* __dc.delete_file_older_x(log_dir + 'archive/', 90)__ - repo.directory_clean_up
  * Delete log files
* __dc.delete_file_older_x(config.shared_directory['data_file_pickup'] + 'Processed/', 30)__ - repo.directory_clean_up
  * Delete archived log files
* __sort_ss.sort_ss_rows(sheet_name_or_id='5704624016516996', col_name='Target_DropDate')__ - repo.smartsheet_repo.sort_rows
  * Sort Smartsht
* __ss_backup.backup_smartsheet()__ - smartsheet_api_defs.back_up
  * Back up smartsheet
* __rsp.delete_pdf_proofs()__ - sftp_maintenance.remove_sftp_proofs 
  * Remove pdf proofs from sftp

<ins>Friday Functions:</ins>
* __sql_update.add_person_id_to_json()__ - repo.personId_sql_update
   * pulling person id from pdf name in U1C file
* __sql_update.update_floats_in_personid_cid()__ - repo.personId_sql_update
   * float fix in db
* __sll.generate_logo_sample_xml()__ - smartcom_validations.sc_logo_testing
   * Smartcom logo xml process

<ins>Fifteenth Functions:</ins>
* __cu.run()__ - small_coms.clean_up
   * Clean up Small in house Smartsheet

## __email_production_main.py__ - Cleans up and deletes files from production

<ins>Daily Functions:</ins>
* __av.check_success()__ - repo.automation_verification
  * Confirms all other main log files have been written
* __pre.run_2mo()__ - repo.pre_email_repo
 * 2 Month Age-In Pre-Email campaign
* __pre.run_7mo()__ - repo.pre_email_repo
 * 7 Month Age-In Pre-Email campaign
* __pre.run_3mo()__ - repo.pre_email_repo
 * 3 Month Age-In Pre-Email campaign
* __pre.run_4mo()__ - repo.pre_email_repo
 * 4 Month Age-In Pre-Email campaign
* __pre.run_2_3mo_post()__ - repo.pre_email_repo
 * 2 and 3 Month Age-In Post-Email campaign

<ins>Friday Functions:</ins>
* __arwr.run()__ - ardr_email.ardr_weekly_run
  * ARDR email production

<ins>Fifteenth Functions:</ins>
* __aiem.ageIn_6912_Email()__ - AgeIn_b_day_suite.age_in_email_main
  * ARDR email production

## __reporting_main.py__ - Runs Reporting functions (functions that provide metrics on campaigns)

<ins>Daily Functions:</ins>
* __ccr.run()__ - salesforce_integration.client_config_reporting
  * Update Client Implementations in Smartsheet. - Client Implementation Management
* __mr.run()__ - email_campaigns.mc_reporting
 * MC Reporting to Smartsheet
* __ssm.fulfill_pending_requests()__ - ppt_look_up.self_serve.self_serve_main
 * Participant look up, self serve
* __nm.run()__ - nonusps.nonusps_main
 * Imports NON usps files posted from vendor
* __pcdp.main()__ - participant_communication.ParticipantCommunicationsDataProcessing
 * Imports data file to [ProdParticipantCommunication]
* __pre_return.run_presort_return_files()__ - presort_return_mail.presort_main
 * Return/presort import.
* __fund_update.run()__ - funding.update_client_fund_ss
  * Update funding preferences to Smartsheet. - Client_Funding_Status
* __cert_reporting.usps_reporting_run()__ - certified_reporting.main
 * USPS status update of certified, returned certified report to DER
* __mcpm.run_smart_sheet_update()__ - mod_config.mod_config_process_main
 * Updates segment guids in smartsheet with Salesforce configurations
* __mcpm.run_sql_update()__ - mod_config.mod_config_process_main
 * Updates SQL tables with guid configs collected from Smartsheet
* __ncoa.populate_ncoa_tables()__ - NCOA_reports.ncoa_reports
 * Updates NCOA report SQL tables with information gained from those table
* __email_validations.run_db_updates()__ - NCOA_reports.email_validations
 * Updates DB from MC and ZB email validations


<ins>Monday Functions:</ins>
* __wcr.create_weekly_comm_report()__ - weekly_comm_reporting.main
  * Creates weekly com report
* __mc_unsub.run()__ - repo.mail_chimp_api.mailchimp_clicks_unsubs_actions
  * Pulls clicks, opens, and unsubs from MC folders for MAV, Groove, Age-in, and Discover
 * __csm_report.run()__ - csm_client_reporting.CSM_Database_To_File
  * Runs non-mailable report by client, posts to Shared drive
 
<ins>First of Month Functions:</ins>
* __ar_reporting.run_ar_reporting()__ - AR_monthly_reporting.main
  * Emails AR postcard count to FND team
* __amr.run_clients()__ - age_in_monthly_reporting.main
  * Emails previous month's age in counts for specified clients
