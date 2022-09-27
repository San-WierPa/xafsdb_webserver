# xafsdbpy.UserApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_user_change_password_post**](UserApi.md#api_v1_user_change_password_post) | **POST** /api/v1/user/change_password | Api Change Password
[**api_v1_user_disable_post**](UserApi.md#api_v1_user_disable_post) | **POST** /api/v1/user/disable | Api Disable
[**api_v1_user_greet_get**](UserApi.md#api_v1_user_greet_get) | **GET** /api/v1/user/greet | Api Greet
[**api_v1_user_login_post**](UserApi.md#api_v1_user_login_post) | **POST** /api/v1/user/login | Api Login
[**api_v1_user_logout_post**](UserApi.md#api_v1_user_logout_post) | **POST** /api/v1/user/logout | Api Logout
[**api_v1_user_register_post**](UserApi.md#api_v1_user_register_post) | **POST** /api/v1/user/register | Api Register


# **api_v1_user_change_password_post**
> object api_v1_user_change_password_post(current_password, new_password, new_password_repetition)

Api Change Password

### Example

* OAuth Authentication (OAuth2PasswordBearer):
```python
from __future__ import print_function
import time
import xafsdbpy
from xafsdbpy.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = xafsdbpy.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure OAuth2 access token for authorization: OAuth2PasswordBearer
configuration = xafsdbpy.Configuration(
    host = "http://localhost"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with xafsdbpy.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = xafsdbpy.UserApi(api_client)
    current_password = 'current_password_example' # str | 
new_password = 'new_password_example' # str | 
new_password_repetition = 'new_password_repetition_example' # str | 

    try:
        # Api Change Password
        api_response = api_instance.api_v1_user_change_password_post(current_password, new_password, new_password_repetition)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling UserApi->api_v1_user_change_password_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **current_password** | **str**|  | 
 **new_password** | **str**|  | 
 **new_password_repetition** | **str**|  | 

### Return type

**object**

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_user_disable_post**
> object api_v1_user_disable_post(password)

Api Disable

### Example

* OAuth Authentication (OAuth2PasswordBearer):
```python
from __future__ import print_function
import time
import xafsdbpy
from xafsdbpy.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = xafsdbpy.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure OAuth2 access token for authorization: OAuth2PasswordBearer
configuration = xafsdbpy.Configuration(
    host = "http://localhost"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with xafsdbpy.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = xafsdbpy.UserApi(api_client)
    password = 'password_example' # str | 

    try:
        # Api Disable
        api_response = api_instance.api_v1_user_disable_post(password)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling UserApi->api_v1_user_disable_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **password** | **str**|  | 

### Return type

**object**

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_user_greet_get**
> object api_v1_user_greet_get()

Api Greet

### Example

* OAuth Authentication (OAuth2PasswordBearer):
```python
from __future__ import print_function
import time
import xafsdbpy
from xafsdbpy.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = xafsdbpy.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure OAuth2 access token for authorization: OAuth2PasswordBearer
configuration = xafsdbpy.Configuration(
    host = "http://localhost"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with xafsdbpy.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = xafsdbpy.UserApi(api_client)
    
    try:
        # Api Greet
        api_response = api_instance.api_v1_user_greet_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling UserApi->api_v1_user_greet_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_user_login_post**
> TokenSchema api_v1_user_login_post(username, password, grant_type=grant_type, scope=scope, client_id=client_id, client_secret=client_secret)

Api Login

### Example

```python
from __future__ import print_function
import time
import xafsdbpy
from xafsdbpy.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = xafsdbpy.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with xafsdbpy.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = xafsdbpy.UserApi(api_client)
    username = 'username_example' # str | 
password = 'password_example' # str | 
grant_type = 'grant_type_example' # str |  (optional)
scope = '' # str |  (optional) (default to '')
client_id = 'client_id_example' # str |  (optional)
client_secret = 'client_secret_example' # str |  (optional)

    try:
        # Api Login
        api_response = api_instance.api_v1_user_login_post(username, password, grant_type=grant_type, scope=scope, client_id=client_id, client_secret=client_secret)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling UserApi->api_v1_user_login_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **username** | **str**|  | 
 **password** | **str**|  | 
 **grant_type** | **str**|  | [optional] 
 **scope** | **str**|  | [optional] [default to &#39;&#39;]
 **client_id** | **str**|  | [optional] 
 **client_secret** | **str**|  | [optional] 

### Return type

[**TokenSchema**](TokenSchema.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/x-www-form-urlencoded
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_user_logout_post**
> object api_v1_user_logout_post()

Api Logout

### Example

* OAuth Authentication (OAuth2PasswordBearer):
```python
from __future__ import print_function
import time
import xafsdbpy
from xafsdbpy.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = xafsdbpy.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure OAuth2 access token for authorization: OAuth2PasswordBearer
configuration = xafsdbpy.Configuration(
    host = "http://localhost"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with xafsdbpy.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = xafsdbpy.UserApi(api_client)
    
    try:
        # Api Logout
        api_response = api_instance.api_v1_user_logout_post()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling UserApi->api_v1_user_logout_post: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_user_register_post**
> object api_v1_user_register_post(username, password, is_admin=is_admin)

Api Register

### Example

```python
from __future__ import print_function
import time
import xafsdbpy
from xafsdbpy.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = xafsdbpy.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with xafsdbpy.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = xafsdbpy.UserApi(api_client)
    username = 'username_example' # str | 
password = 'password_example' # str | 
is_admin = False # bool |  (optional) (default to False)

    try:
        # Api Register
        api_response = api_instance.api_v1_user_register_post(username, password, is_admin=is_admin)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling UserApi->api_v1_user_register_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **username** | **str**|  | 
 **password** | **str**|  | 
 **is_admin** | **bool**|  | [optional] [default to False]

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

