# MOD-EHR Read Only Webpage

## Technical Requirements
- Python 3.10
- PIP 23.3.2
- virtualenv & virtualenvwrapper (optional)
- AWS CDK

## Setup Instructions
- Install requirements ``pip install -r requirements.txt``

## EPIC Docs
- Authentication - [doc](https://fhir.epic.com/Documentation?docId=oauth2&section=BackendOAuth2Guide)
- Appointments Search R4 - [doc](https://fhir.epic.com/Sandbox?api=10469)
- Locations Read R4 - [doc](https://fhir.epic.com/Sandbox?api=928)
- Appointments Sample Data - [file](samples/epic/appointments_sample_response.xml)
- Locations Sample Data - [file](samples/epic/locations_sample_response.xml)

## Via Docs
- Authentication - [doc](https://developer.ridewithvia.com/docs/via-api/qd9vfctukccv3-authentication-with-via-api)
- Trip Details - [doc](https://developer.ridewithvia.com/docs/via-api/s811ivjkupvsm-list-rides-by-any-criteria-in-the-request)
- Trip Details Sample Data - [file](samples/ridewithvia/trips.json)
