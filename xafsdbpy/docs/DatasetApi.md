# xafsdbpy.DatasetApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_dataset_create_post**](DatasetApi.md#api_v1_dataset_create_post) | **POST** /api/v1/dataset/create | Api Create Dataset
[**api_v1_dataset_get_get**](DatasetApi.md#api_v1_dataset_get_get) | **GET** /api/v1/dataset/get | Api Get Dataset
[**api_v1_dataset_list_get**](DatasetApi.md#api_v1_dataset_list_get) | **GET** /api/v1/dataset/list | Api List Datasets
[**api_v1_dataset_preview_upload_post**](DatasetApi.md#api_v1_dataset_preview_upload_post) | **POST** /api/v1/dataset/preview/upload | Api Upload Preview
[**api_v1_dataset_update_put**](DatasetApi.md#api_v1_dataset_update_put) | **PUT** /api/v1/dataset/update | Api Update Dataset


# **api_v1_dataset_create_post**
> object api_v1_dataset_create_post(data_set_create_schema)

Api Create Dataset

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
    api_instance = xafsdbpy.DatasetApi(api_client)
    data_set_create_schema = xafsdbpy.DataSetCreateSchema() # DataSetCreateSchema | 

    try:
        # Api Create Dataset
        api_response = api_instance.api_v1_dataset_create_post(data_set_create_schema)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DatasetApi->api_v1_dataset_create_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_set_create_schema** | [**DataSetCreateSchema**](DataSetCreateSchema.md)|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**500** | Internal Server Error |  -  |
**201** | Created |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_dataset_get_get**
> object api_v1_dataset_get_get(dataset_id)

Api Get Dataset

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
    api_instance = xafsdbpy.DatasetApi(api_client)
    dataset_id = 56 # int | 

    try:
        # Api Get Dataset
        api_response = api_instance.api_v1_dataset_get_get(dataset_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DatasetApi->api_v1_dataset_get_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_id** | **int**|  | 

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
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_dataset_list_get**
> object api_v1_dataset_list_get()

Api List Datasets

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
    api_instance = xafsdbpy.DatasetApi(api_client)
    
    try:
        # Api List Datasets
        api_response = api_instance.api_v1_dataset_list_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DatasetApi->api_v1_dataset_list_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_dataset_preview_upload_post**
> object api_v1_dataset_preview_upload_post(dataset_id, file)

Api Upload Preview

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
    api_instance = xafsdbpy.DatasetApi(api_client)
    dataset_id = 56 # int | 
file = '/path/to/file' # file | 

    try:
        # Api Upload Preview
        api_response = api_instance.api_v1_dataset_preview_upload_post(dataset_id, file)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DatasetApi->api_v1_dataset_preview_upload_post: %s\n" % e)
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
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_dataset_update_put**
> object api_v1_dataset_update_put(dataset_id, data_set_update_schema)

Api Update Dataset

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
    api_instance = xafsdbpy.DatasetApi(api_client)
    dataset_id = 56 # int | 
data_set_update_schema = xafsdbpy.DataSetUpdateSchema() # DataSetUpdateSchema | 

    try:
        # Api Update Dataset
        api_response = api_instance.api_v1_dataset_update_put(dataset_id, data_set_update_schema)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DatasetApi->api_v1_dataset_update_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_id** | **int**|  | 
 **data_set_update_schema** | [**DataSetUpdateSchema**](DataSetUpdateSchema.md)|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**500** | Internal Server Error |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

