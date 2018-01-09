# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/gpl).

import logging
from odoo.api import Environment
from odoo.http import request, route
from odoo.addons.web.controllers.main import Action, DataSet


_logger = logging.getLogger(__name__)

EXCLUDED_MODELS = {'res.users'}

BASE_METHODS = {
    'copy',
    'create',
    'default_get',
    'fields_get',
    'fields_view_get',
    'load_views',
    'name_create',
    'name_read',
    'name_search',
    'name_get',
    'onchange',
    'read',
    'read_group',
    'search',
    'search_count',
    'unlink',
    'write',
}


class ProtectedEnvironment(Environment):

    _bypass_access = True
    _bypass_exception = None

    def __call__(self, cr=None, user=None, context=None):
        cr = self.cr if cr is None else cr
        uid = self.uid if user is None else int(user)
        context = self.context if context is None else context
        res = ProtectedEnvironment(cr, uid, context)
        res._bypass_exception = self._bypass_exception
        return res


class DataSetImproved(DataSet):

    def do_search_read(
        self, model, fields=False, offset=0,
        limit=False, domain=None, sort=None
    ):
        if model not in EXCLUDED_MODELS:
            self._bypass_access(exception=model)
        return super(DataSetImproved, self).do_search_read(
            model, fields=fields, offset=offset, limit=limit,
            domain=domain, sort=sort)

    def _call_kw(self, model, method, args, kwargs):
        if model not in EXCLUDED_MODELS:
            if method in BASE_METHODS:
                self._bypass_access(exception=model)
            else:
                self._check_access_action(model, method, args, kwargs)

        return super(DataSetImproved, self)._call_kw(
            model, method, args, kwargs)

    def _check_access_action(self, model, method, args, kwargs):
        user = request.env.user
        action = request.env['ir.action.protected'].sudo().search([
            ('technical_name', '=', method),
            ('model_technical_name', '=', model),
        ])

        if action:
            ids = self._get_record_ids(model, method, args, kwargs)
            action.check_access(user, ids)
            self._bypass_access()

        return action

    def _get_record_ids(self, model, method, args, kwargs):
        if args:
            ids = args[0]
            if (
                not isinstance(ids, list) or
                not all(isinstance(i, (int, long)) for i in ids)
            ):
                return []
            return ids
        return []

    def _bypass_access(self, exception=None):
        env = request.env
        # The context must be different so that the returned environment
        # is not the current environment.
        context = dict(env.context)
        assert '__access_by_pass' not in context
        context['__access_by_pass'] = True
        request._env = ProtectedEnvironment(env.cr, env.uid, context)
        request._env._bypass_exception = exception


class ActionImproved(Action):

    @route('/web/action/load', type='json', auth="user")
    def load(self, action_id, additional_context=None):
        self._check_access_action(action_id, additional_context)
        return super(ActionImproved, self).load(
            action_id=action_id, additional_context=additional_context)

    def _check_access_action(self, action_id, context):
        if not context:
            return

        model = context.get('active_model')
        ids = self._get_record_ids(context)
        user = request.env.user

        action = request.env['ir.action.protected'].sudo().search([
            ('action_id', '=', int(action_id)),
            ('model_technical_name', '=', model),
        ])

        if action:
            action.check_access(user, ids)
            self._bypass_access()

        return action

    def _get_record_ids(self, context):
        active_ids = context.get('active_ids')
        if active_ids is not None:
            return active_ids

        active_id = context.get('active_id')
        if not active_id:
            return
        return [active_id]

    def _bypass_access(self, exception=None):
        env = request.env
        # The context must be different so that the returned environment
        # is not the current environment.
        context = dict(env.context)
        assert '__access_by_pass' not in context
        context['__access_by_pass'] = True
        request._env = ProtectedEnvironment(env.cr, env.uid, context)
        request._env._bypass_exception = exception
