
import sys


def populate(file):
    # create empty dict for return values
    pop_values = {}

    # create dictionary for timezone translation
    tz_dict = {
        "Eastern Standard Time": "America\\New_York",
        "Eastern Daylight Time": "America\\New_York",
        "Central Standard Time": "America\\Chicago",
        "Central Daylight Time": "America\\Chicago",
        "Mountain Standard Time": "America\\Denver",
        "Mountain Daylight Time": "America\\Denver",
        "Pacific Standard Time": "America\\Los_Angeles",
        "Pacific Daylight Time": "America\\Los_Angeles",
    }

    with open(file, 'r') as f:
        lines = f.readlines()

        # GET THE USER
        for line in lines:
            if line.startswith('custadmin'):
                pop_values['user'] = line.replace("custadmin: ", "").strip()
                continue

        # GET THE TIMEZONE
        for line in lines:
            if line.startswith('timezone'):
                raw_timezone = line.replace("timezone: ", "").replace('\\"', '').strip()
                linux_timezone = tz_dict[raw_timezone]
                
                pop_values["timezone"] = linux_timezone
                continue

    if len(pop_values) == 2:
        return pop_values
    else:
        print("\nSome values not found in file\n")
        return None
        
    
    return pop_values