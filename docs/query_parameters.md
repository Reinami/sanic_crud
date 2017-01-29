# Query Parameters

You can use query parameters on a get request with a collection resource to filter out or in specific records.
You would do this with something like `http://127.0.0.1:8000/person?id__gte=10` and get all ids greater than or
equal to 10.

Here is the list of these query parameters and what they do:

  * `startswith`: field starts with the desired value
  * `contains`: field contains the desired value
  * `lt`: field is less than the value
  * `lte`: field is less than or equal to the value
  * `gt`: field is greater than the value
  * `gte`: field is greater than or equal to the value
  * `null`: field is null
  * `=`: field equals value, this is done with just `?id=10`
  * `in`: field is in list of comma separated values
  * `notin`: field is not in list of comma separated values
