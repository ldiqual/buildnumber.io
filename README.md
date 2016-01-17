BuildNumber.io
--------------

BuildNumber.io generates unique build numbers for you.

Usage
=====

Base URL is `https://buildnumber.io`. Append `?token=<YOUR_TOKEN>` to all your requests. If you don't have a token yet, you can request one here [ HERE ]

### Create a new build

```
POST /com.example.app/builds
 <= {"buildNumber": 245}
```


### Create a new build and return its build number in plain text

```
POST /com.example.app/builds?output=buildNumber
 <= 245
```


### Create a new build with additional information

```
POST /com.example.app/builds
 => {"head": "60b7eca"}
 <= {"buildNumber": 245, "head": "60b7eca"}
```

POST payload is limited to 1024 characters.

### Get the last build

```
GET /com.example.app/builds/last
 <= {"buildNumber": 245, "head": "60b7eca"}
```

### Get information about a build number

```
GET /com.example.app/builds/245
 <= {"buildNumber": 245, "head": "60b7eca"}
```

Examples
--------

### Bash

```
BUILD_NUMBER=$(curl --data '' https://buildnumber.io/com.example.app/newBuildNumber?format=simple&token=ABCDEFGH)
```
