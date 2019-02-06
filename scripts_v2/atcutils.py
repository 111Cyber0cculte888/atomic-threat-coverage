#!/usr/bin/env python3

import yaml
import sys
import re
import json
import os
import subprocess
import requests

from os import listdir
from os.path import isfile, join
from requests.auth import HTTPBasicAuth
from jinja2 import Environment, FileSystemLoader
from pprint import pprint

from pdb import set_trace as bp


# ########################################################################### #
# ############################ ATCutils ##################################### #
# ########################################################################### #

class ATCutils:
    """Class which consists of handful methods used throughout the project"""

    def __init__(self):
        """Init method"""

        pass

    @staticmethod
    def read_rule_file(path):
        """Open the file and load it to the variable. Return text"""

        with open(path) as f:
            rule_text = f.read()

        return rule_text

    @staticmethod
    def read_yaml_file(path):
        """Open the yaml file and load it to the variable.
        Return created list"""

        with open(path) as f:
            yaml_fields = yaml.load_all(f.read())

        buff_results = [x for x in yaml_fields]
        if len(buff_results) > 1:
            result = buff_results[0]
            result['additions'] = buff_results[1:]
        else:
            result = buff_results[0]
        return result

    @staticmethod
    def load_yamls(path):
        """Load multiple yamls into list"""

        yamls = [
                 join(path, f) for f in listdir(path) \
                 if isfile(join(path, f)) \
                 if f.endswith('.yaml') \
                 or f.endswith('.yml')
                ]

        result = []

        for yaml in yamls:
            try:
                result.append(ATCutils.read_yaml_file(yaml))

            except ScannerError:
                raise ScannerError('yaml is bad! %s' % yaml)

        return result

    @staticmethod
    def confluence_get_page_id(apipath, auth, space, title):
        """Get confluence page ID based on title and space"""
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
            }

        url = apipath + "content"
        space_page_url = url + '?spaceKey=' + space + '&title=' \
            + title + '&expand=space'
        #print(space_page_url)
        response = requests.request(
           "GET",
           space_page_url,
           headers=headers,
           auth=auth
        )

        response = response.json()
        #print(response)

        # Check if response contains proper information and return it if so
        if response.get('results'):
            if isinstance(response['results'], list):
                if response['results'][0].get('id'):
                    return response['results'][0][u'id']

        # If page not found
        return None

    @staticmethod
    def push_to_confluence(data, apipath, auth):
        """Description"""

        apipath = apipath if apipath[-1] == '/' else apipath+'/'

        url = apipath + "content"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
            }

        alldata = True
        for i in ["title", "spacekey", "parentid", "confluencecontent"]:
            if i not in data.keys():
                alldata = False
        if not alldata:
            raise Exception("Not all data were provided in order " +
                            "to push the content to confluence")

        dict_payload = {
            "title": "%s" % data["title"], # req
            "type": "page", # req
            "space": { # req
                "key": "%s" % data["spacekey"]
                },
            "status": "current",
            "ancestors": [
                {
                  "id": "%s" % data["parentid"] # parent id
                }
                ],
            "body": { # req
                "storage": {
                    "value": "%s" % data["confluencecontent"], 
                    "representation": "storage"
                    }
                }
            }

        payload = json.dumps(dict_payload)

        response = requests.request(
            "POST",
            url,
            data=payload,
            headers=headers,
            auth=auth
            )

        resp = json.loads(response.text)

        #print(resp)

        if "data" in resp.keys():
            if "successful" in resp["data"].keys() \
                    and bool(resp["data"]["successful"]):
                return "Page created"
            else:
                cid = ATCutils.confluence_get_page_id(
                    apipath, auth, data["spacekey"],
                    data["title"]
                    )

            response = requests.request(
                "GET",
                url + "/%s?expand=body.storage" % str(cid),
                data=payload,
                headers=headers,
                auth=auth
                )

            resp = json.loads(response.text)

            current_content = resp["body"]["storage"]["value"]

            if current_content == data["confluencecontent"]:
                return "No update required"

            response = requests.request(
                "GET",
                url + "/%s/version" % str(cid),
                data=payload,
                headers=headers,
                auth=auth
                )

            resp = json.loads(response.text)

            i = 0

            for item in resp["results"]:
                if int(item["number"]) > i:
                    i = int(item["number"])

            i += 1 #update by one

            dict_payload["version"] = {"number": "%s" % str(i)}
            payload = json.dumps(dict_payload)

            response = requests.request(
                "PUT",
                url + "/%s" % str(cid),
                data=payload,
                headers=headers,
                auth=auth
                )

            return "Page updated"

        elif "status" in resp.keys():
            if resp["status"] == "current":
                return "Page created"

        return "Something unexpected happened.."

    @staticmethod
    def sigma_lgsrc_fields_to_names(logsource_dict):
        """Get sigma logsource dict and rename key/values into our model, 
        so we could use it for Data Needed calculation"""

        sigma_to_real_world_mapping = {
            'sysmon': 'Microsoft-Windows-Sysmon/Operational',
            'security': 'Security',
            'system': 'System',
            'product': 'platform',
            'windows': 'Windows',
            'service': 'channel'
            }

        sigma_keys = [*sigma_to_real_world_mapping]

        proper_logsource_dict = {}

        for key, val in logsource_dict.items():
            if key in sigma_keys:
                if val in sigma_keys:
                    # Transalte both key and value
                    proper_logsource_dict.update([
                        (sigma_to_real_world_mapping[key], 
                         sigma_to_real_world_mapping[val])
                        ])
                else:
                    # Translate only key
                    proper_logsource_dict.update([
                        (sigma_to_real_world_mapping[key], val)
                        ])
            else:
                if val in sigma_keys:
                    # Translate only value
                    proper_logsource_dict.update([
                        (key, sigma_to_real_world_mapping[val])
                        ])
                else:
                    # Don't translate anything
                    proper_logsource_dict.update([
                        (key, val)
                        ])

        # @yugoslavskiy: I am not sure about this 
        # list(proper_logsource_dict.items()) loop. but it works -.-
        # I was trying to avoid error "dictionary changed size during iteration"
        # which was triggered because of iteration 
        # over something that we are changing

        """Old Code
        for old_key, old_value in list(proper_logsource_dict.items()):

            for new_key, new_value in sigma_to_real_world_mapping.items():

                if old_key == new_key:
                    # here we do mapping of keys and values
                    new_key_name = sigma_to_real_world_mapping[new_key]
                    new_value_name = sigma_to_real_world_mapping[old_value]
                    proper_logsource_dict[new_key_name] \
                        = proper_logsource_dict.pop(old_key)
                    proper_logsource_dict.update(
                        [(sigma_to_real_world_mapping[new_key], new_value_name)]
                        )
"""
        return proper_logsource_dict

    @staticmethod
    def main_dn_calculatoin_func(dr_file_path):
        """you need to execute this function to calculate DN for DR file"""

        dn_list = ATCutils.load_yamls('../dataneeded')

        # detectionrule \
        # = read_yaml_file("../detectionrules/sigma_win_susp_run_locations.yml")
        detectionrule = ATCutils.read_yaml_file(dr_file_path)

        # no_extra_logsources = bool

        """For every DataNeeded file we do:
        * for every DN_ID in detectionrule check if its in DataNeeded Title
        * if there is no "additions" (extra log sources), make entire alert an
        "addition" (to process it in the same way)
        """

        logsource = {}

        if not detectionrule.get('additions'):

            detectionrule['additions'] = [detectionrule]

            final_list = []

            logsource_optional_fields = [
                'category', 'product', 'service', 'definition',
            ]

            _temp_list = []

            for val in logsource_optional_fields:
                if detectionrule['logsource'].get(val):
                    _temp_list.append(
                        (val, detectionrule['logsource'].get(val))
                    )

            logsource.update(_temp_list)

            # product = detectionrule['logsource']['product']
            # service = detectionrule['logsource']['service']
            # logsource.update([('product', product), ('service', service)])

            """ then we need to collect all eventIDs 
            and calculate Data Needed PER SELECTION
            """

            for _field in detectionrule['detection']:
                dr_dn = {}
              # if it is selection field
                if str(_field) not in ["condition", "timeframe"]:
                    dr_dn.update(detectionrule['detection'][_field])
                    """ we don't check if it's already here 
                    we do that in the return statement
                    """

                    final_list += ATCutils.calculate_dn_for_dr(
                                      dn_list, dr_dn, logsource
                                  )  
                     
            return list(set(final_list))

        else:
            """ if there are multiple logsources, let's work with them separately.
            first grab general field from first yaml document (usually, commandline)
            """
            common_fields = []
            final_list = []

            for key in detectionrule['detection'].keys():

                if key in ["condition", "timeframe"]:
                    continue

                for fields in detectionrule['detection'][key]:
                    common_fields.append(fields)

            # then let's calculate Data Needed per different logsources
            for addition in detectionrule['additions']:

                logsource_optional_fields = [
                'category', 'product', 'service', 'definition',
                ]

                _temp_list = []

                for val in logsource_optional_fields:
                    if addition['logsource'].get(val):
                        _temp_list.append(
                            (val, addition['logsource'].get(val))
                        )

                logsource.update(_temp_list)

                """ then we need to collect all eventIDs 
                and calculate Data Needed PER SELECTION
                """

                for _field in addition['detection']:
                # if it is selection field
                    dr_dn = {}
                    if not _field in ["condition", "timeframe"]:

                        dr_dn = addition['detection'][_field]
                        #dr_dn.update(logsource)

                        for field in common_fields:
                            dr_dn.update([(field, 'placeholder')])

                            final_list += ATCutils.calculate_dn_for_dr(
                                              dn_list, dr_dn, logsource
                                          )
                        

        return list(set(final_list))

    @staticmethod
    def calculate_dn_for_dr(dn_list, dr_dn, logsource):
        """Meaning of the fields:

        dn_list - list of dataneeded objects (all dataneeded!)
        dr_dn - dictionary of detection fields from the logsource
        logsource - dictionary of logsource fields

        """

        list_of_DN_matched_by_fields = []
        list_of_DN_matched_by_fields_and_logsource = []
        list_of_DN_matched_by_fields_and_logsource_and_eventid = []

        for dn in dn_list:
            # Will create a list of keys from Detection Rule fields dictionary
            list_of_DR_fields = [*dr_dn] 
            list_of_DN_fields = dn['fields']
            amount_of_fields_in_DR = len(list_of_DR_fields)

            amount_of_intersections_betw_DR_and_DN_fields = len(
                set(list_of_DR_fields).intersection(list(set(list_of_DN_fields)
                )))

            if amount_of_intersections_betw_DR_and_DN_fields \
                    == amount_of_fields_in_DR:
                # if they are equal, do..
                list_of_DN_matched_by_fields.append(dn)
                
        for matched_dn in list_of_DN_matched_by_fields:

            # if dn['title'] == matched_dn:

            # divided into two lines due to char limit
            proper_logsource \
                = ATCutils.sigma_lgsrc_fields_to_names(logsource)

            amount_of_fields_in_logsource = len([*proper_logsource])
            y = matched_dn
            x = proper_logsource
            # превозмогая трудности!
            shared_items \
                = {k: x[k] for k in x if k in y and x[k] == y[k]}
            #bp()
            if len(shared_items) == amount_of_fields_in_logsource:

                # divided into two lines due to char limit
                list_of_DN_matched_by_fields_and_logsource\
                    .append(matched_dn)
        # and only in the last step we check EventID
        if dr_dn.get('EventID'):
            eventID = dr_dn.get('EventID')

            for dn in list_of_DN_matched_by_fields_and_logsource:

                try:
                    eventID_from_title = int(dn['title'].split("_")[2])
                except ValueError:
                    eventID_from_title = "None"

                if eventID_from_title == str(eventID):

                    # divided into two lines due to char limit
                    list_of_DN_matched_by_fields_and_logsource_and_eventid\
                        .append(dn)

            y = list_of_DN_matched_by_fields_and_logsource_and_eventid
            return [x['title'] for x in y if x.get('title')]

        else:
            y = list_of_DN_matched_by_fields_and_logsource
            return [x['title'] for x in y if x.get('title')]

    @staticmethod
    def write_file(path, content, options="w+"):
        """Simple method for writing content to some file"""

        with open(path, options) as file:
            # write content
            file.write(content)

        return True

    @staticmethod
    def populate_tg_markdown(art_dir='../triggering/atomic-red-team/',
            atc_dir='../Atomic_Threat_Coverage/'):
        cmd = ('find \'%satomics/\' -name "T*.md" -exec' +
              ' cp {} \'%sTriggering/\' \;') % (art_dir, atc_dir)
        if subprocess.run(cmd, shell=True, check=True).returncode == 0:
            return True
        else:
            return False


