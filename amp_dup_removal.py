import json
import dateutil.parser
from iteration_utilities import duplicates
import os
import requests

# Prompt user for api_key, amp_client_id, amp_group
amp_api_key = input("Enter api_key: ")
amp_client_id = input("Enter amp_client_id: ")
amp_group = input("Enter amp_group: ")
print("api key is:", amp_api_key)
print("amp_client_id is:", amp_client_id)
print("amp_group is:", amp_group)

urls = {'base_url': 'api.amp.cisco.com',
        'amp_device': f"https://api.amp.cisco.com/v1/computers?group_guid%5B%5D={amp_group}&limit=10&offset=0",
        'amp_auth': "https://api.amp.cisco.com/v1/version",
        'amp_event': "https://api.amp.cisco.com/v1/events",
        'amp_groups': "https://api.amp.cisco.com/v1/groups",
        'device_url': f"https://api.amp.cisco.com/v1/computers/"
        }

def checkIfDuplicates(devices):
    ''' Check if device list contains any duplicates '''
    # A set will not count duplicate devices, so if there is a dup the set will be less than actual device list count.
    print("\n==> Checking for duplicate endpoints")
    if len(devices) == len(set(devices)):
        return False
    else:
        return True

def del_endpoints(amp_api_key, amp_client_id, urls, connector_guid):
    """Delete an endpoint registered to Cisco AMP."""
    print("\n==> Deleting endpoint registered to AMP")
    # del_device_url = f"https://api.amp.cisco.com/v1/computers/d286cc74-29ca-4aa8-8153-6dab863e4979"
    print("del_device_url is:", urls['device_url'] + connector_guid)
    response = requests.delete(urls['device_url'] + connector_guid,
                               auth=(amp_client_id, amp_api_key))
    response.raise_for_status()
    del_endpoint_result = response.json()
    return del_endpoint_result

def get_endpoints(amp_api_key, amp_client_id, urls):
    """Get a list of endpoints registered to Cisco AMP."""
    print("\n==> Getting list of endpoints registered to AMP")
    response = requests.get(urls['amp_device'], auth=(amp_client_id, amp_api_key))
    response.raise_for_status()
    device_list = response.json()
    return device_list

response = get_endpoints(amp_api_key, amp_client_id, urls)
device_count = response['metadata']['results']['current_item_count']
print("Number of devices found is:", device_count)

# List of hostnames
devices = [r['hostname'] for r in response['data']]

if checkIfDuplicates(devices):
    print('***** DUPLICATE endpoint(s) found *****')
    duplicates = list(duplicates(devices))
    print("Value of duplicate endpoint(s): ", duplicates)

    # Loop through the device dictionaries in the data list
    for device_dict in response['data']:
        if device_dict['hostname'] in duplicates:
            device_1 = device_dict
            # Removes name from duplicates list so we don't look for it again
            duplicates = set(duplicates) - set([device_dict['hostname']])
            # Loop over response data list for the other duplicate
            for device_with_same_name in response['data']:
                # If the hostname is the same and the connector guid is different - found the dup
                if device_with_same_name['hostname'] == device_1['hostname'] and device_with_same_name['connector_guid'] != device_1['connector_guid']:
                    device_1_last_seen = dateutil.parser.parse(device_1['last_seen'])
                    device_with_same_name_last_seen = dateutil.parser.parse(device_with_same_name['last_seen'])
                    
                    diff = device_1_last_seen - device_with_same_name_last_seen
                    print("Difference in timestamps of devices is:", diff)
                    # Display the duplicate device info to user
                    print(f"Hostname, last seen date, and Guid value of dup devices are:\n \
                        {device_1['hostname']} {device_1['last_seen']} {device_1['connector_guid']} \n \
                        {device_with_same_name['hostname']} {device_with_same_name['last_seen']} {device_with_same_name['connector_guid']}")
                    
                    # if device_1_last_seen > device_with_same_name_last_seen then device_with_same_name is older so needs to be removed
                    # else device_1 needs to be removed
                    delete_this_device = device_with_same_name if device_1_last_seen > device_with_same_name_last_seen else device_1
                    
                    # Indicate the older device to user
                    print("Older device to be removed is: \n", delete_this_device['hostname'], delete_this_device['last_seen'],
                          delete_this_device['connector_guid'])
                    
                    answer = input("Please indicate approval to delete this duplicate endpoint [y/n]")
                    if answer.lower() == 'y':
                        del_response = del_endpoints(amp_api_key, amp_client_id, urls, delete_this_device['connector_guid'])
                        print(f'{json.dumps(del_response, sort_keys=True, indent=4)}')
                        if del_response['data']['deleted']:
                            print("Delete operation PASSED\n")
                        else:
                            print("Delete operation FAILED\n")
                    else:
                        print('Delete operation skipped')
                        print('Checking for next duplicate endpoint')
                    # Stop searching list for dup - already found
                    break    
else:
    print('No duplicates found in list')
    os.system("pause")
    exit(0)

print("No more duplicate endpoints found\n")
os.system("pause")
