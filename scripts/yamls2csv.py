import csv
import sys
import getopt
from os import listdir
from os.path import isfile, join

from atcutils import ATCutils
from yaml.scanner import ScannerError
from attack_mapping import te_mapping, ta_mapping

try:
    ATCconfig = ATCutils.load_config("config.yml")
    dr_dir = ATCconfig.get('detection_rules_directory')
except:
    dr_dir = "../detection_rules/"

HELP_MESSAGE = """Usage: python3 yamls2csv.py [OPTIONS]\n\n\n
        Possible options are --detectionrules_path, --dataneeded_path --loggingpolicies path
        Defaults are 
        detectionrules_path = """ + dr_dir + """;
        dataneeded_path = ../data_needed/;
        loggingpolicies_path=../logging_policies/"""

def load_yamls(path):
    yamls = [join(path, f) for f in listdir(path) if isfile(join(path, f)) if f.endswith('.yaml') or f.endswith('.yml')]
    result = []
    for yaml in yamls:
        try:
            result.append(ATCutils.read_yaml_file(yaml))
        except ScannerError:
            raise ScannerError('yaml is bad! %s' % yaml)
    return result, yamls

def main(**kwargs):
    dn_list = load_yamls(kwargs['dn_path'])[0]
    lp_list = load_yamls(kwargs['lp_path'])[0]
    ra_list = load_yamls(kwargs['ra_path'])[0]
    rp_list = load_yamls(kwargs['rp_path'])[0]
    enrichments_list = load_yamls(kwargs['en_path'])[0]
    alerts, path_to_alerts = load_yamls(kwargs['dr_path'])
    pivoting = []
    analytics = []
    result = []


    print("[*] Iterating through Detection Rules")

    # Iterate through alerts and pathes to them
    for alert, path in zip(alerts, path_to_alerts):
        if not isinstance(alert.get('tags'), list):
            continue
        threats = [tag for tag in alert['tags'] if tag.startswith('attack')]
        tactics = [f'{ta_mapping[threat][1]}: {ta_mapping[threat][0]}'  for threat in threats
                   if threat in ta_mapping.keys() ]
        techniques = [threat for threat in threats if threat.startswith('attack.t')]

        enrichments  = [er for er in enrichments_list if er['title'] in alert.get('enrichment', [{'title':'-'}])]
        if len(enrichments) < 1:
            enrichments = [{'title': '-'}]
        dn_titles = ATCutils.main_dn_calculatoin_func(path)
        #print(dn_titles)
        alert_dns = [data for data in dn_list if data['title'] in dn_titles]
        if len(alert_dns) < 1:
            alert_dns = [{'category': '-',
                          'platform': '-',
                          'provider': '-',
                          'type': '-',
                          'channel': '-',
                          'title': '-',
                          'loggingpolicy': ['-']}]
        logging_policies = []
        for dn in alert_dns:
            # If there are logging policies in DN that we havent added yet - add them
            logging_policies.extend([l for l in lp_list if l['title'] in dn['loggingpolicy']
                                     and l not in logging_policies ])
            # If there are no logging policices at all - make an empty one just to make one row in csv
            if not isinstance(logging_policies, list) or len(logging_policies) == 0:
                logging_policies = [{'title': "-", 'eventID': [-1, ]}]

        for tactic in tactics:
            for technique in techniques:
                technique_name = technique.replace('attack.t', 'T') + ': ' +\
                        ATCutils.get_attack_technique_name_by_id(technique.replace('attack.', ''))
                for dn in alert_dns:
                    for lp in logging_policies:
                        for er in enrichments:
                            result.append([tactic, technique_name, alert['title'], dn['category'], dn['platform'],
                                           dn['type'],dn['channel'], dn['provider'], dn['title'],lp['title'],
                                           er['title'], ';'.join(er.get('requirements', [])), '-', '-'])
    print("[*] Iterating through Response Playbooks")
    for rp in rp_list:
        threats = [tag for tag in rp['tags'] if tag.startswith('attack')]
        tactics = [f'{ta_mapping[threat][1]}: {ta_mapping[threat][0]}'
                   for threat in threats if threat in ta_mapping.keys() ]
        techniques = [threat for threat in threats if threat.startswith('attack.t')]
        ras_buf = []
        [ras_buf.extend(l) for l in rp.values() if isinstance(l, list)]
        ras = [ra for ra in ras_buf if ra.startswith('RA')]
        indices = [i for i, x in enumerate(result) if x[0] in tactics or x[1] in techniques]
        if len(indices) < 1:
            for tactic in tactics:
                for technique in techniques:
                    technique_name = technique.replace('attack.t', 'T') + ': ' +\
                        ATCutils.get_attack_technique_name_by_id(technique.replace('attack.', ''))
                    for ra in ras:
                        result.append([tactic,technique_name, '-', '-', '-',
                                      '-', '-', '-','-','-', '-',rp['title'], ra])
        else:
            for i in indices:
                result[i][-2] = rp['title']
                result[i][-1] = ';'.join(ras)



    analytics = []
    print("[*] Iterating through Data Needed")
    for dn in dn_list:
        pivot = [dn['category'], dn['platform'], dn['type'], dn['channel'], dn['provider'], dn['title'], '', '']
        for field in dn['fields']:
            analytics.append([field] + pivot)
    
    print("[*] Iterating through Enrichments")
    for er in enrichments_list:
        for dn in [dnn for dnn in dn_list if dnn['title'] in er.get('data_to_enrich', [])]:
            pivot = [dn['category'], dn['platform'], dn['type'], dn['channel'], dn['provider'], dn['title'],
                     er['title'], ';'.join(er.get('requirements', []))]
            for field in er['new_fields']:
                analytics.append([field] + pivot)

    with open('../analytics.csv', 'w', newline='') as csvfile:
        alertswriter = csv.writer(csvfile, delimiter=',')  # maybe need some quoting
        alertswriter.writerow(['tactic', 'technique', 'detection rule', 'category', 'platform', 'type', 'channel',
                               'provider','data needed','logging policy', 'enrichment',
                               'enrichment requirements','response playbook', 'response action'])
        for row in result:
            alertswriter.writerow(row)
    
    print("[+] Created analytics.csv")
    
    with open('../pivoting.csv', 'w', newline='') as csvfile:
        alertswriter = csv.writer(csvfile, delimiter=',')  # maybe need some quoting
        alertswriter.writerow(['field', 'category', 'platform', 'type', 'channel', 'provider', 'data_needed',
                               'enrichment', 'enrichment requirements'])
        for row in analytics:
            alertswriter.writerow(row)
    
    print("[+] Created pivoting.csv")

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "",
                               ["detectionrules_path=", "dataneeded_path=", "loggingpolicies_path=", "help"])

    # complex check in case '--help' would be in some path
    if len(sys.argv) > 1 and '--help' in sys.argv[1] and len(sys.argv[1]) < 7:
        print(HELP_MESSAGE)
    else:
        opts_dict = dict(opts)
        kwargs = {
            'dr_path': opts_dict.get('--detectionrules_path', dr_dir),
            'dn_path': opts_dict.get('--dataneeded_path', '../data_needed/'),
            'lp_path': opts_dict.get('--loggingpolicies_path', '../logging_policies/'),
            'en_path': opts_dict.get('--enrichments_path', '../enrichments/'),
            'rp_path': opts_dict.get('--response playbooks path', '../response_playbooks/'),
            'ra_path': opts_dict.get('--response actions path', '../response_actions/')
        }
        main(**kwargs)
