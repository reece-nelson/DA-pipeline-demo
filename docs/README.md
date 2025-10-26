# DA-pipeline-demo
This demo demonstrates the usage of different components for an end to end solution.

### Usage Information:
- install docker desktop on your machine to view logs and build containers, no account necessary. Ensure that docker desktop is open and the engine is running in the lower left of the window.
- To run the pipeline you need to be at the root of the project and run './run.ps1' in the terminal in vs code. This will start the whole pipeline. It should take around 3 minutes from entering './run.ps1' to getting the generated excel file that opens up. You may need to run "Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass" before './run.ps1' if running scripts is disabled for the machine.
- Once the containers are running in docker desktop you can view the postgresql database using this address on a webpage http://localhost:15433/
- The login information can be found in the .env file using the PGADMIN_DEFAULT_EMAIL and PGADMIN_DEFAULT_PASSWORD.
- Once you are logged in you can right click on servers in the top left then - > register - > server.
- In the general section all you need to do is name the server, you can name the server anything you like.
- On the connections tab use the following parameters, then click save:
        hostname/address: postgresdb
        port: 5432
        maintenance database: default_database
        username: username
        password: password
- You can now view the different schemas and tables found in the database on the left hand side panel.


### Architecture Overview:
- I have three images that show the data flow, database design and architecture design. I have created a system that pulls in data using python ingestion from the EIA API and my own API I created for the NHL teams. Then I created a database with medallion architecture to store data, prefect data pipeline to orchestrate, dbt to handle promotion of tables, and docker to isolate the whole system and handle environment. I also created a docker container for pgadmin which is just there to support logging in through the browser. The output of the excel is created via python to display a summary table and line graph.

### Explanation of decisions:
- #### Data sources:
I chose the EIA data source since it had a simple interactive API to use. I also chose the NHL data since it is something of personal interest and also data that could possibly tie back to the locations in the EIA data. NHL teams and electricity sales information do not have much to do with each other but the point of this project is the process of the data pipeline and not so much the data itself. The NHL data is also something simple I could make myself.
- #### Postgres:
I chose postgres because I have used it before and I am familiar with it. It also was straightforward to set up via docker and is easily accessible via python.
- #### Prefect:
I have never used prefect before. When deciding which pipeline technology to use I found out that prefect is very lightweight and simple to use. For a project like this I found this was enough evidence to use Prefect in place of other more capable technologies. It was important to me that since this project needed to be spun up each time using docker, whatever I am using needs to be simple and lightweight. Using large complex libraries and packages is not helpful. The data this project is processing as well is small and doesn't need complex transformations.
- #### Excel Output:
I wanted to create a simple summary of the data being processed in this project. I chose excel since the format of the output can display the summarized table and a line graph in a user friendly way.
### Alternative approaches:
- One thing I spent some time on was deciding which component would get their own container and which would share containers. I gave the database its own container, python and the API. I wanted the API to run in its own isolated container and same for the database. When building out dbt I tried both ways but found it was simpler to just run dbt as part of the python orchestration pipeline. There are multiple ways to build this but I decided this way due to isolating the database, api and any transformations on the data. I also went back and forth between using a .sh .bat or ps1 start scripts. At one point I had all three options created. I chose ps1 because I had the least amount of issues with it. I was trying to get .sh to work since it would work for both mac and windows but in the end it worked the best with ps1.
### Improvements:
- If I had more time I would like to implement logging, test cases and the usage of LLMs. I didn't add any of these because of time. In a system that has very few to zero input changes and data differences in each run, I decided to focus more on the design and seamless running of the end to end system in exchange for better logging and testing when those would have little impact on outcome. I would have liked to introduce LLMs but I did not see a good case for this. I could have forced the usage of LLMs but I didn't want to compromise the goal of this project given the time. I think the solution I built hits the main requirements of this project without compromising too much.
### Scalability:
- This project does have the ability to scale to more tables, more data and more outputs. The data pipeline orchestration that was created had the ability to introduce more steps and a finer detail to transformations. There is a limit to this though since this is all running locally and not on the cloud.  