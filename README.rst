===========
Secure Odoo
===========

A vanilla Odoo instance is very permissive, even for basic user profiles.
Sometimes, it can be easily managed with ACL entries and rules. Sometimes, it
can only be fixed in python code.

This series of modules is intended to fix some issues with access rights on the most
popular Odoo modules (accounting, timesheets, projects, etc).
It does not ensure that your Odoo instance is safe from security threats.

Every issues handled by these modules should be universal. For example, there is no
logical explaination why an analytic line should be deleted if the accounting entry is posted.

If you want to contribute to this project, feel free to propose merge requests.

Contributors
------------
* David Dufresne <david.dufresne@savoirfairelinux.com>
