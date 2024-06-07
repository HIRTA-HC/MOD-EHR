# MOD-EHR

<a name="readme-top"></a>



<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h3 align="center">MOD-EHR</h3>

  <p align="center">
    Documentation for Health Connector's MOD-EHR middleware product.
    <br />
    <a href="https://github.com/HIRTA-HC/MOD-EHR"><strong>Explore the docs »</strong></a>
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">Product Overview</a>
      <ul>
        <li><a href="#focus-of-the-product">Focus of the Product</a></li>
        <li><a href="#dev-community">Dev Community</a></li>
        <li><a href="#stakeholders">Project Stakeholders</a></li>
      </ul>
    </li>
    <li>
      <a href="#product-design">Product Design</a>
      <ul>
        <li><a href="#data-access">Data Access</a></li>
        <li><a href="#data-management">Data Management</a></li>
        <li><a href="#data-storage">Data Storage</a></li>
        <li><a href="#user-interface">User Interface</a></li>
      </ul>
    </li>
    <li><a href="#tech-stack">Tech Stack</a></li>
    <li><a href="#deployment">Deployment</a></li>
      <ul>
        <li><a href="#hardware">Hardware</a></li>
        <li><a href="#cloud-infrastructure">Cloud Infrastructure</a></li>
        <li><a href="#software-environment">Software Environment</a></li>
      </ul>
    <!-- <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li> -->
    <li><a href="#reference-links">Reference Links</a></li>
    <!-- <li><a href="#acknowledgments">Acknowledgments</a></li> -->
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## Product Overview


### Focus of the Product

The Heart of Iowa Regional Transit Agency (HIRTA) was awarded a Phase 2 agreement of the ITS4US Program for its proposed concept “Health Connector for the Most Vulnerable: An Inclusive Mobility Experience from Beginning to End” (Health Connector) by the United States Department of Transportation (USDOT). The goal of this project is to implement a scalable and replicable solution that enables inclusive access to non-emergency medical transportation for all underserved populations and their caregivers by resolving transportation access barriers with the use of advanced technologies

Health Connector is an innovative solution that will address various bottlenecks associated with transportation access to healthcare for HIRTA communities. Some of these challenges are key reasons behind missed appointments or the unacceptable level of preventive or as-needed healthcare in the HIRTA service area. 

The MOD-EHR Middleware is an open-source middleware product that allows data from HIRTA's transportation management system (MOD Platform TMS) and the EHR Software system to be stored, aggregated and displayed in a central location. The purpose of this middleware product is to allow both the transportation provider and healthcare staff to monitor, manage, and ensure all patients have access to transportation to and from medical appointments via a webpage. Currently, the middleware uses an API provided by Via, the MOD Vendor, to gather data from the MOD Platform TMS. A web-based form was developed as to allow users to input healthcare appointment information for travelers, immitating the data that will be collected from an EHR system once implemented by partner healthcare facilities.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Dev Community

The following vendors were involved in the development of this product:

* [Via](https://ridewithvia.com/): Provider of the transportation management software (MOD Platform TMS) used by HIRTA for booking and managing ride operations.
* EHR provider (to be added), such as Epic EHR or Veradigm.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Stakeholders

The intended audience for this middleware product includes, but is not limited to, transit operators, transit funders, healthcare providers, Medicaid, and healthcare transportation providers.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Product Design

The diagram below details the exchange of data between the MOD Platform TMS, EHR API (once available) and the EHR Middleware. Currently, the data flows that are shown coming from the EHR API are collected via a webform built into the EHR middleware product.

![EHR](/images/EHR.png)

### Data Access

The middleware accesses rider and trip data through the MOD Platform TMS API and will access medical appointment data through the EHR API when available. Currently, medical appointment data is entered into the EHR webpage in a format that mimicks what will be expected through the EHR software. Steps to access these APIs and further documentation are described below.

#### Via

The [ViaAPI](https://developer.ridewithvia.com/) is used to book and manage rides (the TMS) received via the middleware and originally from Lyft. The process for gaining access to this API includes:

1. Open a ticket with Via support for credentials for authentication for OAuth2, access to the Via Operations Center (VOC) and Via's Postman collection of the ViaAPI endpoints
2. Authenticate using OAuth2 with ViaAPI.
3. Provide secure URL for webhooks to receive status change updates and set up a listener port for the URL.
4. Get access to the VOC for testing API calls and status updates.

#### EHR

For the MOD-EHR middleware, an administrator is required to generate their own public/private key and share the public key in its application management portal.

1. Epic requires users to load a public key in its application manager portal.
2. Veradigm requires a JWKS to access the public key and the appropriate URL submitted to its application portal.
3. For the MOD-EHR middleware, a user needs to sign a JSON Web Token (JWT) with the user's private key.

### Data Management & Storage

The diagrams below show the data management and storage flows in non-AWS (Flask) and AWS based environments.

![Flask-EHR](/images/Flask-EHR.png)

*Data management and storage flows using a non-AWS (Flask) environment*

![AWS-EHR](/images/AWS-EHR.png)

*Data management and storage flows in the AWS environment*
<!-- ### Data Storage -->

<!-- ### User Interface -->

### User Interface


![EHR-login](/images/EHR_login.PNG)

*Login screen for EHR webpage. Login credentials will be available for HIRTA operations staff and healthcare staff*

![Add Appointment](/images/add-appointment.PNG)

*Form to input healthcare appointment information (mimicking EHR system appointment data)*

![Not Confirmed](/images/not-confirmed.PNG)

*Appointment information appears on webpage indicating that there is no associated ride for the appointment*

![Ride Confirmed](/images/ride-confirmed.PNG)

*Ride information is matched to appointment booking information, indicating patient has transportation to their appointment*

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Tech Stack

Non-AWS Deployment:
* Execution Environment: Python 3.12 running Flask
* Database: Configurable for any relational database that is supported by SQLAlchemy (SQLite, MySQL, Microsoft SQL Server, Oracle) with no specific database dependencies. As built: SQLite
* Storage: Flask: Served from internal storage
* Authentication: Flask-Oauth2 library using OAuth2
* API Management: Flask
* Domain/DNS: N/A

AWS Deployment:

* Execution Environment: AWS Lambda running Python 3.12
* Database: AWS DynamoDB
* Storage: AWS S3 with AWS CloudFront CDN
* Authentication: AWS Cognito
* API Management: AWS API Gateway
* Domain/DNS: AWS Route 53


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Deployment

This specific deployment of the EHR Middleware product utilizes ViaAPI for the MOD Platform TMS endpoints and a custom webpage to mimick the EHR endpoint. The following deployment steps have been generalized to be applicable for use with any TMS and/or EHR provider.

### Cloud Infrastructure

The following tables describes the cloud-based environment and libraries required to deploy the EHR middleware product.

![cloud-services-diagram](/images/cloud-services.png)

### Software Environment

#### Non-AWS installation

1. Generate public/private keys as described under [Data Access](href="#data-access").
2. Install required libraries:
   ```sh
   pip install Flask
   pip install Flask-OAuth
   pip install SQLAlchemy
   pip install Waitress
   ```
   * All of the sub dependencies for these libraries are also required. ‘Requirements_flask.txt’ provides an easy way for an installer to quickly install all required python libraries.
3. The entry point for the Flask application is in the root directory in the filename flask_app.py. Flask should not be directly invoked; rather a production WSGI Web Server should be utilized. Waitress is listed as an option for a production WSGI Web Server. To run the program in Waitress, issue the following command at the root of the codebase:
    ```sh
    waitress-serve flask_app:app
    ```
4. Ensure cybersecurity measures are taken:
* Proper storage of private keys to authenticate against various EHR using FHIR.
* Protecting the python application execution using a reverse proxy such as Apache, Nginx, or IIS.
* Protecting files against unauthorized writes from webserver users.
* Not executing the web server as root or with any elevated permissions.
5. Note: Python expects to read/write into one file: mod_db_v1.db. The middleware uses SQLite, which is performant for the purpose of this project and with a sizable participant size. Modifications could be made to the code to use an existing database. SQLAlchemy supports common databases such as:
* Microsoft SQL Server
* Oracle
* Postgres

#### AWS Installation

1. Using the included AWS Cloud Development Kit (CDK) framework, please refer to [AWS CDK](https://aws.amazon.com/cdk/) for the latest instructions. These middleware products were built using the AWS CDK v2. The following resources are required to proceed with installation:
* AWS Account
* AWS CDK CLI and authentication setup on the machine to execute to AWS CDK commands.
2. Refer to AWS documentation for the latest information on how to setup your computer to interact with your AWS account.
3. To build the AWS environment, navigate to your code directory and execute:
    ```sh
    cdk synth
    cdk deploy app
    ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>





<!-- LICENSE -->
<!-- ## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
 --> 


<!-- CONTACT -->
## Reference Links

HIRTA ITS4US: [https://www.ridehirta.com/its4us](https://www.ridehirta.com/its4us)

Health Connector Site: [https://www.transithealthconnector.org](https://www.transithealthconnector.org)

USDOT ITS4US: [https://www.its.dot.gov/its4us/index.htm](https://www.its.dot.gov/its4us/index.htm)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
[EHR]: images/EHR.png
[AWS-EHR]: images/AWS-EHR.PNG
[Flask-EHR]: images/Flask-EHR.PNG
[EHR-login]: images/AWS_login.PNG
[cloud-services-diagram]: images/cloud-services.png
[Add Appointment]: images/add-appointment.PNG
[Not Confirmed]: images/not-confirmed.PNG
[Ride Confirmed]: images/ride-confirmed.PNG
[python.org]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[python-url]: https://www.python.org/
[aws.amazon.com]: https://img.shields.io/badge/AWS-232F32?style=for-the-badge&logo=AmazonAWS&logoColor=white
[aws-url]: https://aws.amazon.com/
[aws.amazon.com/pm/dynamodb]: https://miro.medium.com/v2/resize:fit:655/1*bjd-Db1gbvIyxcJ8-D1AmA.png
[awsdynamo-url]: https://aws.amazon.com/pm/dynamodb/?gclid=Cj0KCQjw9vqyBhCKARIsAIIcLMFxxPZqEdK938GEeLSrt1DDbhlsak3TGhg7Ysf5AqGRH9Lnw6C5MX0aAmt5EALw_wcB&trk=390f2f77-1064-4521-bd83-27d9213b65c9&sc_channel=ps&ef_id=Cj0KCQjw9vqyBhCKARIsAIIcLMFxxPZqEdK938GEeLSrt1DDbhlsak3TGhg7Ysf5AqGRH9Lnw6C5MX0aAmt5EALw_wcB:G:s&s_kwcid=AL!4422!3!651751060005!p!!g!!dynamo%20storage!19852662209!145019198377
