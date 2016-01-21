BuildNumber.io
==============

Centralized build numbers for your apps and libraries. <https://www.buildnumber.io/>

Usage
-----

Base URL is `https://api.buildnumber.io`. Append `?token=<API_TOKEN>` to all your requests, or use a basic HTTP authentication with `user=API_TOKEN`, and an empty password.

If you don't have a token yet, you can get one on <https://www.buildnumber.io/>.

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

Deployment
----------

Make sure your public key is on the `buildnumber.io` instance, then:

```
$ brew install ansible
$ ansible-galaxy install Datadog.datadog
$ ansible-playbook -i hosts create-servers.yml
```