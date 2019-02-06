#!/usr/bin/env python3

# Import ATC classes
from dataneeded import DataNeeded
from detectionrule import DetectionRule
from enrichments import Enrichments
from loggingpolicy import LoggingPolicy
from triggering import Triggering

# Import ATC Utils
from atcutils import ATCutils

# Others
import glob
import sys
import traceback
import os


class PopulateConfluence:
    """Desc"""

    def __init__(self, auth, lp=False, dn=False, dr=False, en=False, tg=False,
                 auto=False, art_dir=False, atc_dir=False, lp_path=False,
                 dn_path=False, dr_path=False, en_path=False, tg_path=False):
        """Desc"""

        self.auth = auth

        ATCconfig = ATCutils.read_yaml_file("config.yml")

        self.space = ATCconfig.get('confluence_space_name')

        # Assign default if there is no space specified
        if not self.space:
            self.space = "SOC"

        self.apipath = ATCconfig.get('confluence_rest_api_url')
        self.root_name = ATCconfig.get('confluence_name_of_root_directory')

        # Check if atc_dir provided
        if atc_dir:
            self.atc_dir = atc_dir

        else:
            self.atc_dir = '../Atomic_Threat_Coverage/'

        # Check if art_dir provided
        if art_dir:
            self.art_dir = art_dir

        else:
            self.art_dir = '../triggering/atomic-red-team/'

        # Main logic
        if auto:
            self.logging_policy(lp_path)
            self.data_needed(dn_path)
            self.triggering(tg_path)
            self.detection_rule(dr_path)

        if lp:
            self.logging_policy(lp_path)

        if dn:
            self.data_needed(dn_path)

        if dr:
            self.detection_rule(dr_path)

        if en:
            self.enrichment(en_path)

        if tg:
            self.triggering(tg_path)

    def triggering(self, tg_path):
        """Populate triggering"""

        print("Populating Triggering..")
        if tg_path:
            tg_list = glob.glob(tg_path + '*.yml')
        else:
            tg_list = glob.glob('../triggering/atomic-red-team/' +
                                'atomics/T*/*.yaml')

        for tg_file in tg_list:
            try:
                tg = Triggering(tg_file)
                tg.render_template("confluence")
                confluence_data = {
                    "title": tg.fields["attack_technique"],
                    "spacekey": self.space,
                    "parentid": str(ATCutils.confluence_get_page_id(
                        self.apipath, self.auth, self.space, "Triggering")),
                    "confluencecontent": tg.content,
                }

                ATCutils.push_to_confluence(confluence_data, self.apipath,
                                            self.auth)

            except Exception as err:
                print(tg_file + " failed")
                print("Err message: %s" % err)
                print('-' * 60)
                traceback.print_exc(file=sys.stdout)
                print('-' * 60)
        print("Triggering populated!")

    def logging_policy(self, lp_path):
        """Desc"""

        print("Populating Logging Policies..")
        if lp_path:
            lp_list = glob.glob(lp_path + '*.yml')
        else:
            lp_list = glob.glob('../loggingpolicies/*.yml')

        for lp_file in lp_list:
            try:
                lp = LoggingPolicy(lp_file)
                lp.render_template("confluence")
                confluence_data = {
                    "title": lp.fields["title"],
                    "spacekey": self.space,
                    "parentid": str(ATCutils.confluence_get_page_id(
                        self.apipath, self.auth, self.space,
                        "Logging+Policies")),
                    "confluencecontent": lp.content,
                }

                ATCutils.push_to_confluence(confluence_data, self.apipath,
                                            self.auth)
            except Exception as err:
                print(lp_file + " failed")
                print("Err message: %s" % err)
        print("Logging Policies populated!")

    def data_needed(self, dn_path):
        """Desc"""

        print("Populating Data Needed..")
        if dn_path:
            dn_list = glob.glob(dn_path + '*.yml')
        else:
            dn_list = glob.glob('../dataneeded/*.yml')

        for dn_file in dn_list:
            try:
                dn = DataNeeded(dn_file, apipath=self.apipath, auth=self.auth,
                                space=self.space)
                dn.render_template("confluence")
                confluence_data = {
                    "title": dn.dn_fields["title"],
                    "spacekey": self.space,
                    "parentid": str(ATCutils.confluence_get_page_id(
                        self.apipath, self.auth, self.space, "Data+Needed")),
                    "confluencecontent": dn.content,
                }

                ATCutils.push_to_confluence(confluence_data, self.apipath,
                                            self.auth)

            except Exception as err:
                print(dn_file + " failed")
                print("Err message: %s" % err)
                print('-' * 60)
                traceback.print_exc(file=sys.stdout)
                print('-' * 60)
        print("Data Needed populated!")

    def detection_rule(self, dr_path):
        """Desc"""

        print("Populating Detection Rules..")
        if dr_path:
            dr_list = glob.glob(dr_path + '*.yml')
        else:
            dr_list = glob.glob('../detectionrules/*.yml')

        for dr_file in dr_list:
            try:
                dr = DetectionRule(dr_file, apipath=self.apipath,
                                   auth=self.auth, space=self.space
                                   )
                dr.render_template("confluence")

                base = os.path.basename(dr_file)

                confluence_data = {
                    "title": base,
                    "spacekey": self.space,
                    "parentid": str(ATCutils.confluence_get_page_id(
                        self.apipath, self.auth, self.space,
                        "Detection+Rules")), "confluencecontent": dr.content,
                }

                ATCutils.push_to_confluence(confluence_data, self.apipath,
                                            self.auth)
            except Exception as err:
                print(dr_file + " failed")
                print("Err message: %s" % err)
                print('-' * 60)
                traceback.print_exc(file=sys.stdout)
                print('-' * 60)
        print("Detection Rules populated!")

    def enrichment(self, en_path):
        """Nothing here yet"""

        pass
