# -*- coding: utf-8 -*-
# Copyright 2016 SYLEAM
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

from odoo import http, fields
from odoo.addons.web.controllers.main import ensure_db

from ..exceptions import OauthApiException, OauthInvalidTokenException
from .oauth_mixin import OauthMixin

_logger = logging.getLogger(__name__)


class OauthApiController(OauthMixin):

    @http.route('/oauth2/data',
                type='json',
                auth='none',
                methods=['GET'],
                )
    def data_read(self, access_token, model, domain=None, *args, **kwargs):
        """ Return allowed information about the requested model.

        Args:
            access_token (str): OAuth2 access token to utilize for the
                operation.
            model (str): Name of model to operate on.
            domain (list, optional): Domain to apply to the search, in the
                standard Odoo format. This will be appended to the scope's
                pre-existing filter.
        """
        token = self._validate_token(access_token)
        self._validate_model(model)
        data = token.get_data(model, domain=domain)
        return data

    @http.route('/oauth2/data',
                type='json',
                auth='none',
                methods=['POST'],
                )
    def data_create(self, access_token, model, vals, *args, **kwargs):
        """ Create and return new record. """
        token = self._validate_token(access_token)
        self._validate_model(model)
        record = token.create_record(model, vals)
        return record.read()

    @http.route('/oauth2/data',
                type='json',
                auth='none',
                methods=['PUT'],
                )
    def data_write(self, access_token, model, record_ids, vals,
                   *args, **kwargs):
        if isinstance(record_ids, int):
            record_ids = [record_ids]
        token = self._validate_token(access_token)
        self._validate_model(model)
        record = token.write_record(model, record_ids, vals)
        return record.read()

    @http.route('/oauth2/data',
                type='json',
                auth='none',
                methods=['DELETE'],
                )
    def data_delete(self, access_token, model, record_ids, *args, **kwargs):
        if isinstance(record_ids, int):
            record_ids = [record_ids]
        token = self._validate_token(access_token)
        self._validate_model(model)
        token.delete_record(model, record_ids)
        return True
