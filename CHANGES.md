# Changelog
All notable changes to this project will be documented in this file.

### 0.3.0 - 2018-03-16
* Fixed XFS UUID set on restore
* Added '-d' option to fsbackup to hide log timestamps


### 0.2.2 - 2015-09-18
* Changed partition backup to maintain backwards compatibility with sfdisk (This caused some restores to fail)


### 0.2.1 - 2015-05-05
* Fixed bug in backup where snapshot LV is not mounted read-only. Could cause
  errors and backups to fail.


### 0.2.0 - 2015-05-01
* Fixed bug in ext2 creation during 'tune2fs' command with empty options
* Fixed bug in grub install that didn't include --recheck option
* Fixed bug where commands waiting for user input caused restore to hang
* Fixed bug where swap system doesn't get the correct UUID on restore
* Added ability to retry command during restore
* Added continuous mode to restore script


### 0.1.3 - 2014-12-18
* Added automatic image file verification to check for corrupt backup files


### 0.1.2a - 2014-11-16
* Added better error logging when executed commands fail during backup


### 0.1.2 - 2014-11-11
* Migrated to new JSON-formatted backup config file
* Improved exception handling to give more information on unexpected errors
* Added options to include/exclude volume group and logical volumes on the command line (-G, -V, -X, -x)
* Added a couple sanity checks to backup & restore scripts


### 0.1.1 - 2014-11-10
* Initial release
