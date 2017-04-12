=================
Secure Accounting
=================

This module prevents any user from deleting analytic lines bound to a posted general accounting entry.
It prevents writing inside legal fields of a confirmed accounting entry.
It also prevents writing in legal fields of an invoice or deleting invoice lines or taxes of a validated invoice.

Known Issues
------------

This module is not compatible with a subpart of the sale module.
The sale module (odoo 10.0) does fuzzy operations with analytic lines after they are created
to apply some sort of reflection of the analytic lines on the sale order lines.
One solution to have both secure_account and sale to work together is to install the module disable_sale_analytic.

Contributors
------------
* David Dufresne <david.dufresne@savoirfairelinux.com>
* Jérome Boisvert-Chouinard <jerome.boisvertchouinard@savoirfairelinux.com>
