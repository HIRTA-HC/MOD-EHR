# MOD-EHR

<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

<!-- [![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url] -->



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <!-- <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a> -->

  <h3 align="center">MOD-EHR</h3>

  <p align="center">
    Documentation for Health Connector's MOD-EHR middleware product.
    <br />
    <a href="https://github.com/HIRTA-HC/MOD-EHR"><strong>Explore the docs »</strong></a>
    <br />
    <!-- <br />
    <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a> -->
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
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## Product Overview

<!-- [![Medicaid][medicaid-diagram](https://example.com) -->


### Focus of the Product

The Heart of Iowa Regional Transit Agency (HIRTA) was awarded a Phase 2 agreement of the ITS4US Program for its proposed concept “Health Connector for the Most Vulnerable: An Inclusive Mobility Experience from Beginning to End” (Health Connector) by the United States Department of Transportation (USDOT). The goal of this project is to implement a scalable and replicable solution that enables inclusive access to non-emergency medical transportation for all underserved populations and their caregivers by resolving transportation access barriers with the use of advanced technologies

Health Connector is an innovative solution that will address various bottlenecks associated with transportation access to healthcare for HIRTA communities. Some of these challenges are key reasons behind missed appointments or the unacceptable level of preventive or as-needed healthcare in the HIRTA service area. 

The MOD-Medicaid Middleware is an open-source middleware product developed as part of Health Connector that allows data exchange between the HIRTA's transportation management system (MOD Platform TMS) and the State of Iowa Medicaid broker system. The Medicaid broker system uses Access2Care, which provides Non-Emergency Medical Transportation (NEMT) services to Medicaid and Medicare members, allowing Medicaid-funded trips to be provided through HIRTA's Health Connector for eligible Travelers. The middleware utilizes  bi-directional APIs provided by Via in the MOD Platform TMS and the Medicaid broker through Access2Care, who’s data is accessible via an API provided by Lyft. A translation engine is used at both API end points to translate data available from the APIs to a standardized data schema, enabling the data exchange by the middleware application. 

The MOD-EHR Middleware is an open-source middleware product that allows data from HIRTA's transportation management system (MOD Platform TMS) and the EHR Software system to be stored, aggregated and displayed in a central location. The purpose of this middleware product is to allow both the transportation provider and healthcare staff to monitor, manage, and ensure all patients have access to transportation to and from medical appointments. The middleware will use the bi-directional APIs provided by Via as part of the MOD Platform TMS and an EHR software provider, such as Epic, to implement the data flows described below. A translation engine is used at both API end points to translate data available from the APIs to a standardized data schema.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Dev Community

The following vendors were involved in the development of this product:

* [Via](https://ridewithvia.com/): Provider of the transportation management software (TMS) used by HIRTA for booking and managing ride operations.
* EHR provider (to be added), such as Epic EHR or Allscripts/Veradigm

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Stakeholders

The intended audience for this middleware product includes, but is not limited to, transit operators, transit funders, healthcare providers, Medicaid, and healthcare transportation providers.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Product Design

The diagram below details the exchange of data between the TMS (provided by Via)
 and the Medicaid broker's trip API (provided by Lyft).

![EHR](/images/EHR.png)

### Data Access

The middleware accesses rider and trip data through the MOD Platform TMS API (Via) and will access medical appointment data through the EHR API when available. Currently, medical appointment data is entered into the EHR webpage in a format that mimicks what will be expected through the EHR software. Steps to access these APIs and further documentation are described below.

#### Via

The [ViaAPI](https://developer.ridewithvia.com/) is used to book and manage rides (the TMS) received via the middleware and originally from Lyft. The process for gaining access to this API includes:

1. Open a ticket with Via support for credentials for authentication for OAuth2, access to the Via Operations Center (VOC) and Via's Postman collection of the ViaAPI endpoints
2. Authenticate using OAuth2 with ViaAPI.
3. Provide secure URL for webhooks to receive status change updates and set up a listener port for the URL.
4. Get access to the VOC for testing API calls and status updates.

### Data Management & Storage

The diagram below details how data is managed and stored in AWS.

![aws-ehr-diagram](/images/AWS-EHR.png)
<!-- ### Data Storage -->

<!-- ### User Interface -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Tech Stack

This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.

* Execution Environment: AWS Lambda running Python 3.12
* Database: AWS DynamoDB
* Storage: AWS S3 with AWS CloudFront CDN
* Authentication: AWS Cognito
* API Management: AWS API Gateway
* Domain/DNS AWS Route 53



<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Deployment

This specific deployment of the EHR Middleware product utilizes ViaAPI for the MOD Platform TMS endpoints and a custom webpage for the EHR endpoint. The following deployment steps have been generalized to be applicable for use with any TMS and/or EHR provider.

### Hardware

_Insert required hardware_

### Cloud Infrastructure

The following tables describes the cloud-based environment and libraries required to deploy the Medicaid middleware product.

![cloud-services-diagram](/images/cloud-services.png)

### Software Environment

_Update steps below for specific deployment of each codebase_

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
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
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[EHR]: images/EHR.png
[aws-ehr-diagram]: images/AWS-EHR.png
[cloud-services-diagram]: images/cloud-services.png
[python.org]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[python-url]: https://www.python.org/
[aws.amazon.com]: https://img.shields.io/badge/AWS-232F32?style=for-the-badge&logo=AmazonAWS&logoColor=white
[aws-url]: https://aws.amazon.com/
[aws.amazon.com/pm/dynamodb]: https://miro.medium.com/v2/resize:fit:655/1*bjd-Db1gbvIyxcJ8-D1AmA.png
[awsdynamo-url]: https://aws.amazon.com/pm/dynamodb/?gclid=Cj0KCQjw9vqyBhCKARIsAIIcLMFxxPZqEdK938GEeLSrt1DDbhlsak3TGhg7Ysf5AqGRH9Lnw6C5MX0aAmt5EALw_wcB&trk=390f2f77-1064-4521-bd83-27d9213b65c9&sc_channel=ps&ef_id=Cj0KCQjw9vqyBhCKARIsAIIcLMFxxPZqEdK938GEeLSrt1DDbhlsak3TGhg7Ysf5AqGRH9Lnw6C5MX0aAmt5EALw_wcB:G:s&s_kwcid=AL!4422!3!651751060005!p!!g!!dynamo%20storage!19852662209!145019198377
