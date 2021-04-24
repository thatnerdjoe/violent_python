'''
Virus Total Sample
C. Hosmer, November 2019
'''

import json
import hashlib
from virus_total_apis import PublicApi as VirusTotalPublicApi

# You will need to obtain an API Key from Virus Total
API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

SAMPLE = b"X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
SAMPLE_MD5 = hashlib.md5(SAMPLE).hexdigest()

vt = VirusTotalPublicApi(API_KEY)

response =  vt.get_file_report(SAMPLE_MD5)
print (json.dumps(response, sort_keys=False, indent=4))