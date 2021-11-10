# Demo
A basic Flask application with Celery, GraphQL, ans SQLAlchemy

## Running The Application
### Linux
```
gunicorn -w 1 -b 5000 application:flask_app
celery -A application worker -l info
```
### Windows
Good luck with Windows!
- gunicorn is not supported on Windows currently.
- waitress is a good alternative for gunicorn on Windows.
- python and flask commands are working as normal.
- using flask command requires setting the application,something like 'SET FLASK_APP=application:flask_app'.
- celery 4 on Windows requires adding the parameter --pool=solo.
```
python run.py or flask run
celery -A application worker --pool=solo -l info
```
## Testing GraphQL
Go to http://localhost:5000/graphql to try GraphQL.
### Adding a New Patient
```
mutation {
  createPatient(name: "hammad", email: "hammad@abc.com", username: "hammad", mobile: "7418529632") {
    patient {
        id
        name
        email
        username
        mobile
    }
    ok
  }
}
```
### Adding a New Claim
The following query will not work from GraphiQL interface as it doesn't allow to upload files or use multipart requests. This is just for reference.
```
mutation ($claimFile: Upload!) {
  createClaim(reason: "test claim", submissionDate: "2020-07-12T15:38:27", totalValue: 542.5, username:"hammad", claimFile: $claimFile) {
    claim { 
        id 
        reason 
        submissionDate 
        totalValue 
        fileName 
        patient {
            name
            email
            username
            mobile
        }
    }
    ok
  }
}

{
  "claimFile": "fake file path"
}
```
Adding a new claim query will be executed using curl request from the terminal, or using insomnia or postman.
```
curl http://localhost:5000/graphql \
  -F operations='{"query": "mutation ($claimFile: Upload!) { createClaim(reason: \"test claim\", submissionDate: \"2020-07-12T15:38:27\", totalValue: 542.5, username:\"hammad\", claimFile: $claimFile) { claim { id reason submissionDate totalValue fileName patient{ name email username mobile } } ok } }", "variables": { "claimFile": null }}' \
  -F map='{ "0": ["variables.claimFile"]}' \
  -F 0=@/home/hammad/English.txt

curl --url http://localhost:5000/graphql ^
  --form 'operations={"query": "mutation ($claimFile: Upload!) { createClaim(reason: \"test claim\", submissionDate: \"2020-07-12T15:38:27\", totalValue: 542.5, username:\"hammad\", claimFile: $claimFile) { claim { id reason submissionDate totalValue fileName patient{ name email username mobile } } ok } }", "variables": { "claimFile": null }}' ^
  --form 'map={ "0": ["variables.claimFile"]}' ^
  --form 0=@D:\\English.txt
```
For simplicity, I prefer to use insomnia. insomnia request for creating a new claim is included in the project root directory.
### Getting All Patients
```
{
  allPatients {
    edges {
      node {
        id
        name
        email
        username
        mobile
      }
    }
  }
}
```
### Getting All Claims 
```
{
  allClaims {
    edges {
      node {
        id
        totalValue
        submissionDate
        reason
        patient {
          id
          username
        }
      }
    }
  }
}
```
### Finding All Claims for a Patient Username
```
{
  findPatientClaim(username: "hammad") {
    id
    username
    claims {
      edges {
        node {
          id
          reason
          submissionDate
          totalValue
        }
      }
    }
  }
}
```
