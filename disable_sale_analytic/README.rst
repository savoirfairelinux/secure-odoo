=====================
Disable Sale Analytic
=====================

In the module sale of Odoo 10.0, there is a file named sale_analytic.py.
This file acts as some sort of binding between analytic lines (from timesheets or invoices)
and sale order lines.

One problem with that feature is its lack of transparency to the final user.
Analytic lines should only be an output of the business logic. It should not be central to the workflow.
This makes the application behavior very hard to understand and predict.

Contributors
------------
* David Dufresne <david.dufresne@savoirfairelinux.com>
