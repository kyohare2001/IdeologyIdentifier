# IdeologyIdentifier 

Web application that scores user ideological identity by using their social media posts

### Key Technological stacks 
    BackEnd
        - Python (Data Collection , Data Cleaning , Categorize user posts by NLP , scoring model creation)
        - FastAPI
        - Google storage (storing Model files)
        - Google Runs

        libraries: atproto

    FrontEnd
        - React 

    APIs
        - Twitter (Reddit)

### Description

Web application that scores user ideological identity by using their social media posts. 

- need to have 4 api request 
1. Java Script allow to return user's id and python script must send request of it and catch the response / JS Create Response
2. based on 1. user id python script must send request to gather user's posts information (up to 100), then catch the response (JSON.file)
/ Python Create Request 1 then Create Response for 3
3. based on 2's json file, system must score on each text, so that, the system must send request to ChatGPT api and that script must return the response. / Python Create Request from 2 then Create Response for 4
4. based on 3's responses, apply some alogirth to unify user score and create upload on HTTP server
/ Python Create Request from 3 then Create Response to unify with front end. 

the java script must catch 4's response and show the data on front end. 
