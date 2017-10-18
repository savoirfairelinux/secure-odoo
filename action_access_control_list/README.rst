==========================
Action Access Control List
==========================

In Odoo, the way permissions to trigger an action are evaluated causes a load of problems.

If the user does not have access to modify and read all objects manipulated by the transaction, it will raise an incomprehensible error message to the user.

Therefore, the user needs to have access to a lot of object just so that he can click on the button.

For example, if you want to restrain a user on read access to analytic entries (because this is sensible data), this will block the user on most operations.


Protected Actions
-----------------
This module adds the possibility to define a 'Protected Action'.

A protected action has 2 fields: the model and the technical name of the action.
The technical name of the action is the name of the python method called on the object.

Once a protected action is declared, every call to this action is controlled by a new type of ACL (action control lists). This type of ACL has 3 fields:

* Action: the protected action
* Group: the user group
* Domain: an optional restriction on the objects.

When the action is triggered, the access will be checked against the action ACL. If the access is granted, any additionnal access will be granted for the rest of the transaction.

For example, a user could validate an invoice without having access to accounting entries.


Standard Methods
----------------
Standard object methods (such as read, write, create, unlink, onchange, copy, etc) are managed differently than custom object methods (actions).

If a standard method is called, the access will be checked only for the model being manipulated.

If a user must have access to see the form of an invoice, it does not mean that he must have access to accounting entries and payments. Therefore, a read on the model invoice must only trigger access checks against invoices.

If when creating a sale order, a sequence number is generated, this does not mean that the user should have access in read/write to sequences.


Contributors
------------
* David Dufresne <david.dufresne@savoirfairelinux.com>
* Istvan Szalai <istvan.szalai@savoirfairelinux.com>
