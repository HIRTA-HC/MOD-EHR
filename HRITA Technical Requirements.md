# HRITA Technical Requirements

## Overall Concept

1. **Lyft and Via Middleware**: An application that receives requests (New, Update, Delete trip) from Lyft, transforms and issues request to Via, transforms Via response back to Lyft.
2. **Medical and Transit Dashboard**: A second application that extracts medical appointment information from an electronic health records / electronic medical records (EHR/EMR) data from Epic (or another FHIR compliant system) and matches it against trip information from Via and displays it on a dashboard.
3. **Kiosk**: This is being handled by a separate team right now.

## Overall Architecture

1. Deployed on an AWS Lambda function with supporting infrastructure for API Management (AWS API Gateway), authentication (AWS Cognito), and data store (AWS DynamoDB). Secrets stored on AWS Secrets Manager. Logging will occur on AWS Cloudwatch.
2. AWS Lambda will utilize Python.
3. External Python libraries should be well utilized to reduce exposure to poorly managed codebases

## Lyft x Via Middleware

0. Cognito + API Gateway to authenticate and route data to a lambda function
1. Create code to receive data with the following endpoint (API gateway should provide indication of which endpoint)
    * POST /v1/tapi/trips
    * PUT /v1/tapi/trips/{trip_id} - TBD need more information on compatibility
    * POST /v1/tapi/trips/{trip_id}/cancel
    * POST /v1/tapi/atms/webhooks - TBD need more info
2. For each end point, transform the incoming data to the appropriate Via structure
3. Issue request to Via:
    * POST /v1/tapi/trips -> POST /trips/request + POST /trips/book
    * PUT /v1/tapi/trips/{trip_id} - TBD need more information on compatibility
    * POST /v1/tapi/trips/{trip_id}/cancel -> POST /trips/cancel
    * POST /v1/tapi/atms/webhooks - TBD need more info
4. For each of the responses, transform the request back what Lyft expects
5. Return data back to Lyft

## Medical and Transit Dashboard

### Python

1. Create an authentication mechanism to connect to:
    * Epic Healthcare (PoC Done)
    * Veradigm/AllScripts (Stretch goal)
2. For a set of known patients with **known** Patient FHIR ID:
    * extract all upcoming appointments information
        * /Appointment using patient=Patient FHIR ID + service-category='appointment'
        * Info needed includes: start time, end time, location
    * With these appointments, find their location
        * /Location/{location_id} - found in the XML tree at Bundle/entry/resource/Appointment/participant
    * The big thing with this dataset is to traverse though the known data and build guard rails so that we test  against the likely variations of data that's coming through.,  note that "participants" include patient, medical professional, and facility (and sometime equipment).
    * We may need to search the service-category='surgery'
3. On Via, find any upcoming trips with **known** Via Rider ID's
    * /trips/get using rider_id and trip_status as "CONFIRMED"
        * Alternatively, query all trips with confirmed status, and filter by sub_service "Health_Connector"
4. Using a known mapping between Via Rider ID and Patient FHIR ID, return all appointment data left joined against available upcoming trip information by rider - day (preferably at a time, but travel and appointment time are close but not equal), and display to user
    * This could be as simple as Rider (MRN + Rider ID), date, appointment, trips sorted by time.

Notes:

* All responses from EMR systems follow FHIR standards, which is XML.  I've been using the library untangle to traverse the XML dataset.
* Epic's sandbox dataset: https://fhir.epic.com/Documentation?docId=testpatients
* Epic API documentation: https://fhir.epic.com/Specifications  USE R4
* Via API documentation: https://developer.ridewithvia.com/

### Dashboard

1. Authenticate with API Gateway/Cognito
2. Receive json data from Lambda function
3. Display a table, flagging for appointments without a matching trip.
