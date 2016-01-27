BuildNumber.io
==============

Centralized build numbers for your apps and libraries. <https://www.buildnumber.io/>

Usage
-----

Complete usage documentation is provided at <https://www.buildnumber.io/#examples>.

Deployment
----------

Make sure your public key is on the `buildnumber.io` instance, then:

```
$ brew install ansible
$ ansible-galaxy install Datadog.datadog
$ ansible-playbook -i hosts create-servers.yml
```