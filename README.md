# GitHub-Miner
The project involves developing API endpoints for GitHub GraphQL queries and GitHub REST queries and to integrate these endpoints into the Python Flask framework, enabling the publication of these queries as accessible API endpoints via URLs. We have implemented endpoints for 4 query elements: comment, contributions, profiles and time_range_contributions. Each element contains multiple queries and each query has a separate endpoints for both GraphQL and REST API implemented. Phase 2 of this project involves creating a frontend for this application using ReactJS. 

System Architecture:

![image](https://github.com/user-attachments/assets/415fc0a8-712d-49fa-afc5-5796c25378a2)

This system follows the Model-View-Controller architecture. Frontend is the View with which user will interact. Once user invokes an endpoint, we get to the github_routes file which acts as the controller of the system, which find the appropriate route for the method from the graphql_services which is the model of the system. Once the relevant method is called, model returns the API response to the controller and then this response is finally sent to the view which is our frontend.


The user interface includes the following pages -

Login page - GitHub Oauth is used to authenticate users with GitHub. The user is asked to enter the GitHub username and will be redirected to GitHub for the required permissions to access the data. Once authenticated, the user will be redirected to the profile page.

Profile page - This page contains the user statistics - profile image, bio, number of followers, popular repositories, contribution data, etc. The user can view the statistics of each of the popular repos - number of forks, number of watchers, repository access status, etc. The contribution graph will give insights into the number of contributions on a particular day.

Repositories page - This page will list down all the repositories of an authenticated user.

Time-range contributions - This page will display the statistics of the required user within the desired period of time. The user has to provide the GitHub username, start date, and end date of the user.
Logout - This will log out the user from our application.
