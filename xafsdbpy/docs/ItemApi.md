# xafsdbpy.ItemApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_item_list_get**](ItemApi.md#api_v1_item_list_get) | **GET** /api/v1/item/list | Api List Items
[**api_v1_item_upload_post**](ItemApi.md#api_v1_item_upload_post) | **POST** /api/v1/item/upload | Api Upload Item


# **api_v1_item_list_get**
> list[ItemResponseSchema] api_v1_item_list_get(dataset_id)

Api List Items

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
    api_instance = xafsdbpy.ItemApi(api_client)
    dataset_id = 56 # int | 

    try:
        # Api List Items
        api_response = api_instance.api_v1_item_list_get(dataset_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ItemApi->api_v1_item_list_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_id** | **int**|  | 

### Return type

[**list[ItemResponseSchema]**](ItemResponseSchema.md)

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
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_item_upload_post**
> object api_v1_item_upload_post(dataset_id, file)

Api Upload Item

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
    api_instance = xafsdbpy.ItemApi(api_client)
    dataset_id = 56 # int | 
file = '/path/to/file' # file | 

    try:
        # Api Upload Item
        api_response = api_instance.api_v1_item_upload_post(dataset_id, file)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ItemApi->api_v1_item_upload_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_id** | **int**|  | 
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

