# xafsdbpy.FileApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_file_download_get**](FileApi.md#api_v1_file_download_get) | **GET** /api/v1/file/download | Api Download File
[**api_v1_file_get_get**](FileApi.md#api_v1_file_get_get) | **GET** /api/v1/file/get | Api Get File Metadata
[**api_v1_file_list_get**](FileApi.md#api_v1_file_list_get) | **GET** /api/v1/file/list | Api List Files Metadata
[**api_v1_file_upload_post**](FileApi.md#api_v1_file_upload_post) | **POST** /api/v1/file/upload | Api Upload File


# **api_v1_file_download_get**
> object api_v1_file_download_get(file_id)

Api Download File

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
    api_instance = xafsdbpy.FileApi(api_client)
    file_id = 56 # int | 

    try:
        # Api Download File
        api_response = api_instance.api_v1_file_download_get(file_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FileApi->api_v1_file_download_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_id** | **int**|  | 

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
**500** | Internal Server Error |  -  |
**404** | Not Found |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_file_get_get**
> FileResponseSchema api_v1_file_get_get(file_id)

Api Get File Metadata

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
    api_instance = xafsdbpy.FileApi(api_client)
    file_id = 56 # int | 

    try:
        # Api Get File Metadata
        api_response = api_instance.api_v1_file_get_get(file_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FileApi->api_v1_file_get_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_id** | **int**|  | 

### Return type

[**FileResponseSchema**](FileResponseSchema.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**500** | Internal Server Error |  -  |
**404** | Not Found |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_file_list_get**
> list[FileResponseSchema] api_v1_file_list_get()

Api List Files Metadata

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
    api_instance = xafsdbpy.FileApi(api_client)
    
    try:
        # Api List Files Metadata
        api_response = api_instance.api_v1_file_list_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FileApi->api_v1_file_list_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[FileResponseSchema]**](FileResponseSchema.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_file_upload_post**
> object api_v1_file_upload_post(file)

Api Upload File

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
    api_instance = xafsdbpy.FileApi(api_client)
    file = '/path/to/file' # file | 

    try:
        # Api Upload File
        api_response = api_instance.api_v1_file_upload_post(file)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FileApi->api_v1_file_upload_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **file**|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**500** | Internal Server Error |  -  |
**201** | Created |  -  |
**400** | Bad Request |  -  |
**409** | Conflict |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

