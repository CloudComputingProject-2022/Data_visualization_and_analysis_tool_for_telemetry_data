# Cloud-based data visualization and analysis tool for telemetry data
An naive data visualization and analysis tool for F1 on board telemetry data.

<div id="top"></div>


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="client/img/logo_large.png" alt="Logo">
  </a>

  <h3 align="center">Cloud-based data visualization and analysis tool for telemetry data</h3>

  <p align="center">
    <br />
    <a href="anomalyx_demo.gif">View Demo</a>
    ·
    <a href="issues">Report Bug</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contacts">Contacts</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
In both minor motorsport categories and racing e-sports there seems to be no easily accessible tool to collect, visualize and analyze live telemetry data. The user often has to perform complex installation tasks to run these tools on his own machine, which might not be powerful enough to handle real-time data stream analysis. 

This work proposes a possible baseline architecture to implement a data visualization and analysis tool for on-board telemetry data, completely based on cloud technologies and distributed systems. The proposed system falls under the Software-as-a-Service (SaaS) paradigm and relies on Infrastructure-as-a-Service (IaaS) cloud solutions to provide hardware support to its software components.

### Built With

This section lists any major frameworks/libraries used in this project.

Data source and front-end:
* [FastF1](https://github.com/theOehrly/Fast-F1)
* [Streamlit](https://streamlit.io/)

Back-end Apache services:
* [ZooKeeper](https://zookeeper.apache.org/)
* [Kafka](https://kafka.apache.org/) - [KafkaPython](https://github.com/dpkp/kafka-python)
* [Spark](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html) - [PySpark](https://github.com/apache/spark)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

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

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap
These are some of the features we would like to add to this project.

- [x] Add anomaly threshold real-time choice
- [ ] Multidriver support (this involves kafka topics re-organization)
- [ ] Add statefulness to streamlit
    - [ ] Counter variables
    - [ ] Data dict
- [ ] Use MLlib into the Spark SS data analysis module

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->
## Contacts

* Andrea Lombardi - [Linkedin](https://www.linkedin.com/in/andrea-lombardi/)
* Vincenzo Silvio - [Linkedin](https://www.linkedin.com/in/vincenzo-silvio-0413321b8/)
* Ciro Panariello - [Linkedin](https://www.linkedin.com/in/ciro-panariello-57044119b/)
* Vincenzo Capone - [Linkedin](https://www.linkedin.com/feed/)

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
This space lists all the helpful resources we would like to give credit to.

Thanks to O'Reilly books about:
* [ZooKeeper](https://www.oreilly.com/library/view/zookeeper/9781449361297/)
* [Kafka](https://www.oreilly.com/library/view/kafka-the-definitive/9781492043072/)
* [Spark](https://www.oreilly.com/library/view/spark-the-definitive/9781491912201/)

Infrastructure-as-a-Service used for this project:
* [Google Cloud Dataproc](https://cloud.google.com/dataproc)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[product-screenshot]: images/screenshot.png
