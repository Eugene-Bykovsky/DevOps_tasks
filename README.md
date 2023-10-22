# Simple REST API with Python and Flask

This is a simple REST API built with Python and Flask using a MongoDB database. It supports the following HTTP methods:

* GET: Returns the value of the object with the specified key.
* POST: Creates a new object.
* PUT: Updates the value of the object with the specified key.

## Usage

To use the API, you can send HTTP requests to the following endpoint:

```bash
http://localhost:8080/<key>
```

Where <key> is the key of the object you want to create, read, or update.

For example, to create a new object with the key my-key and the value my-value, you would send the following POST request:

```bash
curl -X POST http://localhost:8080/my-key -H "Content-Type: application/json" -d '{ "key": "my-key", "value": "my-value" }'
```

This would return the following response:

```json
{
  "key": "my-key",
  "message": "Object created successfully."
}
```

To read the value of the object with the key my-key, you would send the following GET request:

```bash
curl -X GET http://localhost:8080/my-key
```

This would return the following response:

```json
{
  "value": "my-value"
}
```

To update the value of the object with the key my-key, you would send the following PUT request:

```bash
curl -X PUT http://localhost:8080/my-key -H "Content-Type: application/json" -d '{ "value": "new-value" }'
```

This would return the following response:

```json
{
  "key": "my-key",
  "message": "Object created or updated successfully."
}
```

## Docker
To run the API using Docker, you can use the following 

```bash
docker-compose up --build -d 
```