# Demo
A demo for Flask with Celery and GraphQL

## Testing GraphQL
Go to http://localhost:5000/graphql to try GraphQL.
### Adding a New Patient
```
mutation {
  createPatient(name: "abc", email: "hello@abc.com", username: "abc", mobile: "01150802020") {
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
```
mutation ($claim: Upload!) {
  createPatient(name: "abc", email: "hello@abc.com", username: "abc", claim: $claim) {
    patient {
      id
      name
      email
      username
    }
    ok
  }
}

{
  "claim": "fake file path"
}
```
```
curl http://localhost:5000/graphql \
  -F operations='{"query": "mutation ($claim: Upload!) { createPatient(name: \"abc\", email: \"hello@abc.com\", username: \"abc\", claim: $claim) { patient { id name email username } ok } }", "variables": { "claim": null }}' \
  -F map='{ "0": ["variables.claim"]}' \
  -F 0=@/home/hammad/English.txt
```
### Getting All Patient List
```
{
  allPatients {
    edges {
      node {
        id,
        name,
        email,
        username,
        mobile
      }
    }
  }
}
```
### Finding a Patient with Username
```
{
  findPatient(username: "abc") {
    id,
    name,
    email
  }
}
```
