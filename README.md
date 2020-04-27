# Peter's Take-Home

This repository contains my submission for a take-home test. This README was written some time after the interview process, I got permission from my interviewer to include this publicly on my Github as part of my portofolio but it I have not included the company name in the README or in the code out of professional courtesy as they don't want their name to be included.
The deliverables as well as requirements. assumptions, tradeoffs, .. etc. are documented here as well.
**NOTE:** If you're reviewing this for 100% code quality or complete philosophical correctness, or complete consistency with my other public projects, please keep in mind that this was not the purpose of this project. Instead, the purpose was to demonstrate as many skills as possible in the shortest time possible (the span of 8 hours of work spread over multiple days, a great deal of which went into research). I will try to document as many of the known issues as possible but remember to keep an open mind since I'm writing this months after my original submission `^_^`.


# Deliverables
The exact deliverables text can be found in this screenshot, (I cropped out names and emails).

![Exact Deliverables Test](https://peters-publicly-shared-stuff.s3.us-east-2.amazonaws.com/Screen+Shot+2020-04-27+at+9.39.19+AM.png)

# Summary of Design Choices

 - For the web framework, this was not optional so I went with Django.
 - For the architectural persistence model, I went with the active record pattern because there was not a requirement to maintain maintain an audit log of all changes to data and it was the simplest for the purpose of this demo.
 - For the testing framework, I went with the standard django tests.
 - For Infrastructure as Code (IaC), I chose Cloudformation.
 - For authentication mechanism, this was not optional, so I went with a Bearer Token with the token type being a JWT.
 - I chose Elastic Beanstalk as a PaaS to make my life easier.
 - For storing static assets, I chose Amazon S3.
 - For the documentation, I went with Swagger 2.0 that would be automatically generated from the Django code.
 - For dependency management, I went with [poetry](https://python-poetry.org/).
 - I did not adopt a specific well-known layered architecture like repository, infrastructure, application, ...etc. in order to finish this demo as fast as possible though I have used these patterns in other projects where I find them appropriate.

# Installation Instructions

 1. Install Python, at least version 3.7. Detailed instructions on this are found [here](https://realpython.com/installing-python/).
 2. Install Poetry. Detailed instructions can be found [here](https://python-poetry.org/docs/).
 3. Install dependencies by typing `poetry install`.
 4. (Optional) You can run tests by typing `make test`.
 5. You can run the project by typing `make run`.
 6. To checkout the automated API docs, go to `/redoc/` after running the project.


# Cloud Architecture
For the purpose of this small demo project, I went with a simple AWS architecture.

![Architecture Diagram](https://peters-publicly-shared-stuff.s3.us-east-2.amazonaws.com/_Blank+AWS+%282019%29+diagram.png)

# Known Issues and Potential Improvements

 - Secrets should not be stored in the repository or even in environments variables. Alternatively, maybe I would use SSM Parameter Store or AWS Secrets Manager to take advantage of automated secret rotation.
 - Test coverage was included but I did not add a minimum required acceptance coverage because I did not have the time to write tests for everything. The purpose was to demonstrate that I know how to write tests and that I know the importance of measuring test coverage. Therefore, I only included some end-to-end tests.
 - I wanted to showcase how swagger documentation can be generated automatically by analyzing django assets, so I used a library that does this and added some helpers to make the generated docs as accurate as possible, but swagger (OAS 2.0), which was to be generated automatically, did not exactly support the type of authentication I was using (Bearer Authentication), and getting around that would have been seriously time consuming given that this was a demo so the authentication part in the docs is inaccurate.
 - I also know that the admin page representations and API nested presentations and paginations are not the prettiest as this was done in the quickest way possible, but for the record, if this was a real project I would have
	 - Made the admin pages prettier and added filters and search parameters.
	 - I would have added nested representations when necessary but I wouldn't have overdone it because that would have impacted performance so this would have had to be based on use cases and a tradeoff between wanting to minimize the number of requests hitting the APIs and wanting to also minimize the time it takes to service a single request.
	 - Introduced limit-offset pagination; I believe that this pagination style is the most effective in almost 100% of situations because it mitigates the problem of race conditions when paginating data that is constantly changing.
 - Here are other stuff I would have added if this was a real project
	 - I would have added a CI/CD pipeline to automate running tests and deployments.
	 - I would have added all sorts of dashboards, metrics, and logged everything I could think of.
	 - I would have written more tests, not just end-to-end tests but would have added unit tests and integration tests when suitable and would have set a minimum required coverage percentage.