# 🐺 PackTravel
[![Build](https://github.com/CSC510-SE-Fall2024/Team82-PackTravel/actions/workflows/build.yml/badge.svg)](https://github.com/CSC510-SE-Fall2024/Team82-PackTravel/actions/workflows/build.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14210493.svg)](https://doi.org/10.5281/zenodo.14210493)
[![codecov](https://codecov.io/gh/CSC510-SE-Fall2024/Team82-PackTravel/branch/main/graph/badge.svg?token=20a750d4-c013-4006-8a38-24bddf824450)](https://codecov.io/gh/CSC510-SE-Fall2024/Team82-PackTravel)
[![Commit Activity](https://img.shields.io/github/commit-activity/w/CSC510-SE-Fall2024/Team82-PackTravel)](https://github.com/CSC510-SE-Fall2024/Team82-PackTravel/pulse)
[![Issues](https://img.shields.io/github/issues/CSC510-SE-Fall2024/Team82-PackTravel?color=red)](https://github.com/CSC510-SE-Fall2024/Team82-PackTravel/issues)
[![Contributors](https://img.shields.io/github/contributors/CSC510-SE-Fall2024/Team82-PackTravel)](https://github.com/CSC510-SE-Fall2024/Team82-PackTravel/graphs/contributors)
[![Discord](https://img.shields.io/discord/1300195209472114780?color=blueviolet&label=Discord%20Discussion%20Chat&cacheBuster=1)](https://discord.gg/UF5Hr2dW)
[![GitHub issues](https://img.shields.io/github/issues/CSC510-SE-Fall2024/Team82-PackTravel)](https://github.com/CSC510-SE-Fall2024/Team82-PackTravel/issues)
[![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/CSC510-SE-Fall2024/Team82-PackTravel)](https://github.com/CSC510-SE-Fall2024/Team82-PackTravel/issues?q=is%3Aissue+is%3Aclosed)
[![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/CSC510-SE-Fall2024/Team82-PackTravel)](https://github.com/CSC510-SE-Fall2024/Team82-PackTravel/pulls?q=is%3Apr+is%3Aclosed)
[![License](https://img.shields.io/github/license/CSC510-SE-Fall2024/Team82-PackTravel)](LICENSE)
![Languages](https://img.shields.io/github/languages/count/TripleS-org/PackTravel_G29)
[![Code Size](https://img.shields.io/github/languages/code-size/CSC510-SE-Fall2024/Team82-PackTravel)](https://github.com/CSC510-SE-Fall2024/Team82-PackTravel)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE-OF-CONDUCT.md)
[![Repo Size](https://img.shields.io/github/repo-size/CSC510-SE-Fall2024/Team82-PackTravel)](https://github.com/CSC510-SE-Fall2024/Team82-PackTravel/)

<a href="https://github.com/CSC510-SE-Fall2024/Team82-PackTravel/network"><img alt="GitHub forks" src="https://img.shields.io/github/forks/CSC510-SE-Fall2024/Team82-PackTravel?cacheBuster=1"></a>
<a href="https://github.com/CSC510-SE-Fall2024/Team82-PackTravel/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/CSC510-SE-Fall2024/Team82-PackTravel?cacheBuster=1"></a>

PackTravel is a web-application that connects people who want to carpool, share a cab or ride a bus together. Users can offer rides with their own vehicles, or travel together as a group in a cab or a bus. PackTravel helps you stay on a budget by reducing your travel expenses so that you don't have to miss out on that concert you've been wanting to attend 😉.

## 💎 Features
*   Users can create rides - personal vehicle, cab or taxi
*   Autocomplete for source and destination points
*   Users can send requests to join rides, cancel a ride request
*   Ride owners can accept requests from other riders to join rides, ride owners can delete their own rides
*   Forum for every ride to discuss logistics
*   Integration with Google Maps to show ride route , distance and duration.
*   Users can now get an estimated cab fare predicted with machine learning using date and time of the ride as attribute.
*   Users can set preferences in their profile
*   Created a feedback system for future analysis


## Watch the Demo Video

[Watch the video](https://github.com/TripleS-org/PackTravel_G29/raw/main/images/VIDEO-2024-11-01-20-28-18.mp4)




## 👥 Audience
Any person who is looking to reduce spending on their commute expenditure can use our application.

## ⚒️ Deployment and Installation
*   PackTravel is built using MongoDB Atlas database, Django (Python) for backend-services, and HTML/CSS/JS/Bootstrap for the front-end.
*   The application can be deployed on any web-server running on premise or in the cloud. See [django deployment](https://docs.djangoproject.com/en/4.1/howto/deployment/) to setup django on a VM.
*   See [developer environment setup](INSTALL.md#--developer-environment-setup) to setup your development server.
*   Common issues faced by users while setting up the developer environment are listed [here](INSTALL.md#debugging).

## Scaling PackTravel
![Scale PackTravel](images/scale-PackTravel.png "Scale PackTravel")
*   It is possible to scale PackTravel horizontally because of how we designed the application.
*   All APIs are stateless (REST); Therefore, any application server in a cluster can handle a request.
*   We can use a CDN such as Amazon S3, Cloudflare to serve static assets (images). This enables quicker load time as CDN servers are spread across geographic regions.
*   The bottleneck in PackTravel is the email sending feature. If we use a message queue such as Kafka to offload the task of sending an email to a different application (Kafka consumer), it will free our application server's resources quickly.
*   MongoDB is designed to handle large amounts of data and high levels of throughput. It can distribute data across multiple servers and process it in parallel. It has built-in support for sharding and this makes it easy to scale MongoDB horizontally by adding more servers as needed to handle the increased load.

## 🎯 Proposed Enhancements
*   Enable viewing of ride history in user account
*   Enable notifications if request is received accepted
*   Enable higher account security using 2FA

## 📨 Help and Troubleshooting
For any help or assistance regarding the software, please e-mail any of the developers with the query or a detailed description. Additionally, please use issues on GitHub for any software related issues, bugs or questions.

*   skulkar6@ncsu.edu
*   spustak@ncsu.edu
*   sakre@ncsu.edu
