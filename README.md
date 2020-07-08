# Demo
A demo for Flask with Celery and GraphQL

## Testing GraphQL
Go to http://localhost:5000/graphql to try GraphQL.
### Adding a New Patient
```
mutation {
  createPatient(name: "abc", email: "hello@abc.com", username: "abc") {
    patient {
      id,
      name,
      email,
      username
    }
    ok
  }
}
```
### Getting All Patient List
```
{
  allPatients {
    edges {
      node {
        name,
        email,
        username
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
