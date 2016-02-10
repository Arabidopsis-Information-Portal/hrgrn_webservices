# Installation Instructions

This document includes installation instructions for Mac OS X
## Development Environment Configuration

* Install [Homebrew](http://brew.sh/#install)
* Install [Python 2.7.X](http://docs.python-guide.org/en/latest/starting/install/osx/)
* Install [VirtualEnv](http://docs.python-guide.org/en/latest/dev/virtualenvs/#virtualenvironments-ref)

## Initial Development Environment Setup

To interact, and develop for Araport Data Microservces APIs (ADAMA) you would need a user account at Araport, ADAMA API keys, and authentication token. You would need an authentication key to access core ADAMA services, deploy, and validate status of your data API.

###[Create a user account at Araport](https://www.araport.org/user/register)

### Set ADAMA environment variables

```
$  vi  ~/.bash_profile
$ export ARAPORT=https://api.araport.org
$ export ADAMA=$ARAPORT/community/v0.3
$ export USERNAME=<your username at araport.org>
$ export PASSWORD=<your password at araport.org>
```

Source your bash profile to make changes for environment variables effective.

```
$ source  ~/.bash_profile
```

### Get an Authentication Token

You would need obtain a set of API keys using one-time action command. If you already have your API keys, you may skip to the next section. 

### <a name="api-client"></a>Create API client	
Now you will issue a request to the ADAMA server to create API client. The name of the API client is ``hrgrn_cli_app ``.

Please, open your terminal, and run command:
	
```
$ curl -Lk -X POST \
     -u "$USERNAME:$PASSWORD"  \
     -d "clientName=`hrgrn_cli_app" \
     $ARAPORT/clients/v2
```

You should receive a response returned by the ADAMA server (shortened by brevity)

```
{
    "message": "Client created successfully.",
    "result": {
        ...
        "consumerKey": "gTgpCecqtOc6Ao3GmZ_FecVSSV8a",
        "consumerSecret": "hZ_z3f4Hf3CcgvGoMix0aksN4BOD6",
        ...
    },
    "status": "success",
    ...
}
```

Save the fields `consumerKey` and `consumerSecret`. You would need them later to obtain an authentication token.

### <a name="authentication-token"></a>Obtain an Authentication Token

Obtain an authentication token from the OAuth service (please, substitute `consumerKey` and `consumerSecret` with the values returned for your client application ``hrgrn_cli_app`.

```
$ curl -Lk -X POST \
     -u "$CONSUMER_KEY:$CONSUMER_SECRET"  \
     -d "grant_type=password" \
     -d "username=$USERNAME" \
     -d "password=$PASSWORD" \
     -d "scope=PRODUCTION" \
     $ARAPORT/token
```
The returned response received from the OAuth service should look like:

```
{
    "access_token": "de32225c235cf47b9965997270a1496c",
    "expires_in": 14266,
    "refresh_token": "196f45495f6d9d0bc15416f7c55c39a",
    "token_type": "bearer"
}
```

Please, note the value of `access_token` token field. The `access_token` field is the value of the token you will need to use in your development wokflow: deploy your data API, validate the API status, or create an isolated environment on a remote server to interact with your API.

Open your terminal, and save the `access_token` field in the environmment variable `TOKEN`:

```
$export TOKEN=de32225c235cf47b9965997270a1496c
```
Look at your `TOKEN` variable:

```
$echo $TOKEN
de32225c235cf47b9965997270a1496c
```

### <a name="automate-token-updates"></a>Automate Future Token Updates

Here the steps that automate the procedure to refresh an authentication token and save your time.

* Save `consumerKey`, and `consumerKey` you have obtained during [API client creation step](#api-client) in your bash profile to avoid repetitive copy-pasting.
* Add function that would update an authentication token to your .bash_profile
* Edit your bash_profile from the terminal, and copy-past the text below:

```
$ vi ~/.bash_profile
  export CONSUMER_KEY=<actualValueofConsumerKey>
  export CONSUMER_SECRET=<actualValueofConsumerSecret>
  
  function update_token(){
curl -Lk -X POST \
     -u "$CONSUMER_KEY:$CONSUMER_SECRET"  \
     -d "grant_type=password" \
     -d "username=$USERNAME" \
     -d "password=$PASSWORD" \
     -d "scope=PRODUCTION" \
     $ARAPORT/token
}
```
- Source bash profile to make changes effective

```
$ source  ~/.bash_profile
```
* Run in the terminal
 
```
$ update_token
```
Response Received:

```
{
    "access_token": "91584099511ffb3de947bcc3c67c55c",
    "expires_in": 14266,
    "refresh_token": "196f45495f6d9d0bc15416f7c55c39a",
    "token_type": "bearer"
}
```
Export an authentication token as environment variable, and validate the value:

```
$ export TOKEN=91584099511ffb3de947bcc3c67c55c 
$ echo $TOKEN
91584099511ffb3de947bcc3c67c55c
```
**NOTE:**

In the future steps, you will run only 3 commands:

```
$update_token

$export TOKEN=<access_token_value>

$echo $TOKEN
```


## Code Checkout

Check out code from Github:
You may skip this step, if you already done so.

```
$ cd ~
$ mkdir -p ~/git/scienceapps
$ cd ~/git/scienceapps
$ git clone git@github.com:Arabidopsis-Information-Portal/hrgrn_webservices.git
```

If you checked out the code you may retrieve the most recent code updates as:

```
$ cd ~/git/scienceapps/hrgrn_webservices/services/hrgrn_node_details_by_locus
$ git pull
```


Install & Activate Virtual Environment

```
$ cd ~/git/scienceapps/hrgrn_webservices/services/hrgrn_node_details_by_locus
$ virtualenv venv
$ source venv/bin/activate
```
When a virtual environment activated you will see the command line prompt looks like:

```
$(venv)
```

Please, make sure you do any work when your virtual enviroment activated. It will save your time from investigating a number of sporadic errors and keep your main python environmet clean.


Install prerequsite packages:

```
$ pip install -r requirements.txt
```

## Deployment

### [Refresh an Authentication Token](#automate-token-updates)

An authentication token requires reactivation every four hours. You don't need repeat this step if you redeploy the API within token expiration timeframe.  

* Run in the terminal
 
```
$update_token
$export TOKEN=<access_token_value>
$echo $TOKEN
```


### Check access to ADAMA

This step is optional during repetitive deployment session.

```
curl -kL -X GET \
     -H "Authorization: Bearer $TOKEN" \
     $ADAMA/status 
```

If the token and the server are working fine you should see:

```
{
    "api": "Adama v0.3",
    "hash": "6869fde8e2617ab8f8a58c5c09b1512a80185500",
    "status": "success"
}
```

### Create Target Namespace

The namespace allows your code run independently from apis developed by others as well as to group your API as a set of related packages. It is one of components that would uniquely identify the services provided by your API.

The recommended way to create/test/deploy your services is first to publish your service in a developer workspace. Araport naming convention assumes that any developer workspace which ends in *-dev is a development namespace. The development namespace will not visible by default.

**IMPORTANT**: HRGRN API production namespace is ``hrgrn ``. You may not create the duplicate namespace.

Let's assume you will create target development namespace ``hrgrn-dev``.

The rationality behind this step the following. 

First, by default  your development namespace will be active workspace. This will help you to avoid copy-pasting its value into a number of deployment commands.

Second, it will help you avoid accidental deployment into a production environment until you're really ready.

```
$vi ~/.bash_profile
export NS=hrgrn-dev
```
Source bash profile to make changes effective, andvalidate value of the namespace variable:

```
$ source  ~/.bash_profile
$ echo $NS
hrgrn-dev

```

Formal command to create your namespace. We will substitute `namespace-value` with the actual value when we actually run it.

```
 curl -Lk -X POST \
     -F name=<namespace-value> \
     -F description="Namespace description" \
     -H "Authorization: Bearer $TOKEN" \
     $ADAMA/namespaces
```

Run command from the terminal to create ``hrgrn-dev`` namespace

```
 curl -Lk -X POST \
     -F name=hrgrn-dev \
     -F description="HRGRN Dev namespace" \
     -H "Authorization: Bearer $TOKEN" \
     $ADAMA/namespaces
```

You should receive the response with success status for your namespace: hrgrn-dev`

```
{
    "result": "https://api.araport.org/community/v0.3/hrgrn-dev",
    "status": "success"
}
```

### Deploy Node Details by Locus Service

#### Deploy Service

```
$ pwd
$ ~/git/scienceapps/hrgrn_webservices/services/hrgrn_node_details_by_locus
$ echo $NS
hrgrn-dev
$ curl -sk -L -X POST $API/$NS/services -F "git_repository=https://github.com/Arabidopsis-Information-Portal/hrgrn_webservices.git" -F "metadata=services/hrgrn_node_details_by_locus" -H "Authorization: Bearer $TOKEN"
```


Response Received:

```
{
    "message": "registration started",
    "result": {
        "list_url": "https://api.araport.org/community/v0.3/hrgrn-dev/hrgrn_node_details_by_locus_v0.9/list",
        "notification": "",
        "search_url": "https://api.araport.org/community/v0.3/hrgrn-dev/hrgrn_node_details_by_locus_v0.9/search",
        "state_url": "https://api.araport.org/community/v0.3/hrgrn-dev/hrgrn_node_details_by_locus_v0.9"
    },
    "status": "success"
}
```

#### Validate Service Status

```
$ curl -skL -X GET -H "Authorization: Bearer $TOKEN" "$API/$NS/hrgrn_node_details_by_locus_v0.9"
```

Partial Response:

```
{
    "result": {
        "service": {
            "authors": [
                {
                    "email": "bioinfo@noble.org",
                    "name": "Xinbin Dai",
                    "sponsor_organization": "The Samuel Roberts Noble Foundation",
                    "sponsor_uri": "http://plantgrn.noble.org/hrgrn"
                },                
...

},
            "validate_request": false,
            "validate_response": false,
            "version": 0.9,
            "whitelist": {
                "129.114.97.1": {},
                "129.114.97.2": {},
                "129.116.84.203": {},
                "172.17.42.1": {},
                "api.araport.org": {},
                "plantgrn.noble.org": {}
            },
            "workers": [
                "8bed7b162cd5f14ceb57f4f6b19a1558cf0cd94d918d05370faa2f46499a375a"
            ]
        }
    },
    "status": "success"}

```

#### Issue a Search Request

```
$curl -v -H "Authorization: Bearer $TOKEN" https://api.araport.org/community/v0.3/$NS/hrgrn_node_details_by_locus_v0.9/search?locus=AT3G46810
```

Response Received:

```
 < HTTP/1.1 200 OK
< Date: Wed, 10 Feb 2016 18:42:56 GMT
* Server WSO2-PassThrough-HTTP is not blacklisted
< Server: WSO2-PassThrough-HTTP
< Link: https://api.araport.org/community/v0.3/hrgrn-dev/hrgrn_node_details_by_locus_v0.9/prov/0328dda1b05541fcac8d211f570e43ee; rel="http://www.w3.org/ns/prov#has_provenance"
< Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept, Authorization, Content-Range, Range
< Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
< Content-Type: application/json
< Access-Control-Allow-Origin: *
< Access-Control-Allow-Credentials: true
< Connection: close
< Transfer-Encoding: chunked
<
{"result": [
{"nodes": [{"data": {"level": "20", "color": "#000000", "type": "Protein", "border_color": "#ff0000", "zoom": "2", "label": "AT3G46810", "shape": "diamond", "tftr": "PHD", "tips": "AT3G46810, ID=np25574, Protein, chromatin regulator family PHD", "locus": "AT3G46810", "background_color": "#FCFCFC", "id": "np25574"}}], "edges": []}
],
"metadata": {"time_in_main": 0.43668699264526367},
"status": "success"}
* Closing connection 0
```

#### Delete Service (optional, required to redeploy the service of the same version)

```
$
curl -Lk -X DELETE -H "Authorization: Bearer $TOKEN" https://api.araport.org/community/v0.3/$NS/hrgrn_node_details_by_locus_v0.9"
```

Response Received:

```
{
    "status": "success"
}
```

You may repeat deployment steps above as needed.

## Code Testing

To test your code locally you may extend or simply run `main_test.py` from the command line. It has a test code for the search and list endpoints.

```
$cd ~/git/scienceapps/hrgrn_webservices/services/hrgrn_node_details_by_locus
$ python main_test.py
```

Please, make sure your virtual environment is activated.
You should receive the success message for both search and list requests issued. 

Note the results received in your terminal. You may test the webservice endpoints separately by commenting one of them and running thest module from the command line.


## Documentation Building

1. Open your terminal
2. From the root source code directory run:

```
$ cd ~/git/scienceapps/hrgrn_webservices/services/hrgrn_node_details_by_locus
$ ./build_doc.sh
```
3. API documentation is generated in [API Doc Folder.](../../doc/api/node_details_by_locus/toc.html)


Optionally, you may customize the files included, the output format using API doc [configuration file.](doc.config)