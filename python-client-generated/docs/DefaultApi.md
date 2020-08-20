# swagger_client.DefaultApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**v1_drivers_fatigue_post**](DefaultApi.md#v1_drivers_fatigue_post) | **POST** /v1/drivers/fatigue | фиксировани усталости водителй
[**v1_drivers_on_order_post**](DefaultApi.md#v1_drivers_on_order_post) | **POST** /v1/drivers/on_order | Получение информации \&quot;на заказе\&quot; для группы водителей
[**v1_drivers_online_hourly_post**](DefaultApi.md#v1_drivers_online_hourly_post) | **POST** /v1/drivers/online/hourly | Получение информации \&quot;на линии\&quot; (online) для группы водителей.
[**v1_drivers_online_quater_hourly_post**](DefaultApi.md#v1_drivers_online_quater_hourly_post) | **POST** /v1/drivers/online/quater_hourly | Получение информации \&quot;на линии\&quot; (online) для группы водителей

# **v1_drivers_fatigue_post**
> v1_drivers_fatigue_post(body)

фиксировани усталости водителй

приём (запись) данных о времени \"на линии\" и время на заказе для каждого водителя из заданного подможества

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
body = swagger_client.FatigueBody() # FatigueBody | 

try:
    # фиксировани усталости водителй
    api_instance.v1_drivers_fatigue_post(body)
except ApiException as e:
    print("Exception when calling DefaultApi->v1_drivers_fatigue_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FatigueBody**](FatigueBody.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **v1_drivers_on_order_post**
> QuartersResponse v1_drivers_on_order_post(body)

Получение информации \"на заказе\" для группы водителей

были ли водители на заказе в течение часа с момента __timestamp__

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
body = swagger_client.TimeRequest() # TimeRequest | 

try:
    # Получение информации \"на заказе\" для группы водителей
    api_response = api_instance.v1_drivers_on_order_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->v1_drivers_on_order_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TimeRequest**](TimeRequest.md)|  | 

### Return type

[**QuartersResponse**](QuartersResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **v1_drivers_online_hourly_post**
> HourResponse v1_drivers_online_hourly_post(body)

Получение информации \"на линии\" (online) для группы водителей.

были ли водители на линии в течение часа с момента __timestamp__

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
body = swagger_client.TimeRequest() # TimeRequest | 

try:
    # Получение информации \"на линии\" (online) для группы водителей.
    api_response = api_instance.v1_drivers_online_hourly_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->v1_drivers_online_hourly_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TimeRequest**](TimeRequest.md)|  | 

### Return type

[**HourResponse**](HourResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **v1_drivers_online_quater_hourly_post**
> QuartersResponse v1_drivers_online_quater_hourly_post(body)

Получение информации \"на линии\" (online) для группы водителей

были ли водители на линии в течение часа с момента __timestamp__ с информацией на каждые 15 мин

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
body = swagger_client.TimeRequest() # TimeRequest | 

try:
    # Получение информации \"на линии\" (online) для группы водителей
    api_response = api_instance.v1_drivers_online_quater_hourly_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->v1_drivers_online_quater_hourly_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TimeRequest**](TimeRequest.md)|  | 

### Return type

[**QuartersResponse**](QuartersResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

