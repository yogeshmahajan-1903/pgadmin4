##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2025, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import json
import uuid

from pgadmin.browser.server_groups.servers.databases.schemas.tests import \
    utils as schema_utils
from pgadmin.browser.server_groups.servers.databases.tests import utils as \
    database_utils
from pgadmin.utils.route import BaseTestGenerator
from regression import parent_node_dict
from regression.python_test_utils import test_utils as utils
from . import utils as domain_cons_utils
from unittest.mock import patch


class DomainConstraintDeleteMultipleTestCase(BaseTestGenerator):
    """ This class will add new domain constraint under schema node. """

    scenarios = utils.generate_scenarios('domain_constraint_multiple_delete',
                                         domain_cons_utils.test_cases)

    def setUp(self):
        self.db_name = parent_node_dict["database"][-1]["db_name"]
        schema_info = parent_node_dict["schema"][-1]
        self.schema_id = schema_info["schema_id"]
        self.schema_name = schema_info["schema_name"]
        self.server_id = schema_info["server_id"]
        self.db_id = schema_info["db_id"]
        self.domain_name = "domain_%s" % (str(uuid.uuid4())[1:8])
        self.domain_con_names = ["test_domain_con_delete_%s" %
                                 (str(uuid.uuid4())[1:8]),
                                 "test_domain_con_delete_%s" %
                                 (str(uuid.uuid4())[1:8])]

        self.domain_info = domain_cons_utils.create_domain(self.server,
                                                           self.db_name,
                                                           self.schema_name,
                                                           self.schema_id,
                                                           self.domain_name)
        self.domain_constraint_ids = []
        self.domain_constraint_ids.append(
            domain_cons_utils.create_domain_constraints(
                self.server,
                self.db_name,
                self.schema_name,
                self.domain_name,
                self.domain_con_names[0]))
        self.domain_constraint_ids.append(
            domain_cons_utils.create_domain_constraints(
                self.server, self.db_name, self.schema_name,
                self.domain_name, self.domain_con_names[1]))

    def delete_multiple(self, data):
        """
        This function returns multiple domain constraint delete response
        :param data: domain constraint ids to delete
        :return: domain constraint delete response
        """
        return self.tester.delete(
            self.url + str(utils.SERVER_GROUP) + '/' + str(
                self.server_id) + '/' +
            str(self.db_id) + '/' + str(self.schema_id) + '/' +
            str(self.domain_id) + '/',
            content_type='html/json',
            data=json.dumps(data),
            follow_redirects=True,
        )

    def runTest(self):
        """ This function will add domain constraint under test database. """
        db_con = database_utils.connect_database(self, utils.SERVER_GROUP,
                                                 self.server_id, self.db_id)
        if not db_con['data']["connected"]:
            raise Exception("Could not connect to database.")
        schema_response = schema_utils.verify_schemas(self.server,
                                                      self.db_name,
                                                      self.schema_name)
        if not schema_response:
            raise Exception("Could not find the schema.")

        self.domain_id = self.domain_info[0]
        domain_name = self.domain_info[1]

        domain_response = domain_cons_utils.verify_domain(
            self.server,
            self.db_name,
            self.schema_id,
            domain_name)
        if not domain_response:
            raise Exception("Could not find the domain.")

        domain_cons_response = domain_cons_utils.verify_domain_constraint(
            self.server, self.db_name,
            self.domain_con_names[0])
        if not domain_cons_response:
            raise Exception("Could not find domain constraint.")
        data = {'ids': self.domain_constraint_ids}
        if self.is_positive_test:
            response = self.delete_multiple(data)

        actual_response_code = response.status_code
        expected_response_code = self.expected_data['status_code']
        self.assertEqual(actual_response_code, expected_response_code)

    def tearDown(self):
        # Disconnect database to delete it
        database_utils.disconnect_database(self, self.server_id, self.db_id)
